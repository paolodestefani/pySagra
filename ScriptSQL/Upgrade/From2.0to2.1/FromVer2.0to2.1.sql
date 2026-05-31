--
-- Upgrade from 2.0. to 2.1 script
--

-- Update companies

DO $$
DECLARE
c text;
sql text;
owner_role text;
BEGIN
SELECT 'pa_owner_role' INTO owner_role; -- *** change if necessary ***
sql := '
-- SETTINGS
ALTER TABLE setting ADD COLUMN IF NOT EXISTS default_payment_type char DEFAULT ''C''; -- Cache or Electronic
UPDATE setting SET default_payment_type = ''C'';
ALTER TABLE setting DROP CONSTRAINT IF EXISTS setting_default_payment_type_check;
ALTER TABLE setting ADD CONSTRAINT setting_default_payment_type_check CHECK (default_payment_type IN (''C'', ''E'')); -- Cache, Electronic

--ORDER HEADER
ALTER TABLE order_header ADD COLUMN IF NOT EXISTS is_electronic_payment boolean NOT NULL DEFAULT false;

-- VIEWS

DROP VIEW IF EXISTS income_summary;
CREATE VIEW income_summary AS
SELECT oh.event,
    ev.description AS event_description,
    oh.stat_order_date AS order_date,
    count(
        CASE
            WHEN oh.stat_order_day_part = ''L'' THEN oh.id
            ELSE NULL
        END) AS num_orders_lunch,
    count(
        CASE
            WHEN oh.stat_order_day_part = ''D'' THEN oh.id
            ELSE NULL
        END) AS num_orders_dinner,
    sum(
        CASE
            WHEN oh.stat_order_day_part = ''L'' THEN oh.covers
            ELSE 0
        END) AS num_covers_lunch,
    sum(
        CASE
            WHEN oh.stat_order_day_part = ''D'' THEN oh.covers
            ELSE 0
        END) AS num_covers_dinner,
    sum(
        CASE
            WHEN oh.delivery = ''A'' AND oh.stat_order_day_part = ''L'' THEN oh.total_amount
            ELSE 0
        END) AS tot_take_away_lunch,
    sum(
        CASE
            WHEN oh.delivery = ''A'' AND oh.stat_order_day_part = ''D'' THEN oh.total_amount
            ELSE 0
        END) AS tot_take_away_dinner,
    sum(
        CASE
            WHEN oh.delivery = ''T'' AND oh.stat_order_day_part = ''L'' THEN oh.total_amount
            ELSE 0
        END) AS tot_table_lunch,
    sum(
        CASE
            WHEN oh.delivery = ''T'' AND oh.stat_order_day_part = ''D'' THEN oh.total_amount
            ELSE 0
        END) AS tot_table_dinner,
    sum(
        CASE
            WHEN oh.is_electronic_payment IS false AND oh.stat_order_day_part = ''L'' THEN oh.total_amount
            ELSE 0
        END) AS tot_cash_lunch,
    sum(
        CASE
            WHEN oh.is_electronic_payment IS false AND oh.stat_order_day_part = ''D'' THEN oh.total_amount
            ELSE 0
        END) AS tot_cash_dinner,
    sum(
        CASE
            WHEN oh.is_electronic_payment IS true AND oh.stat_order_day_part = ''L'' THEN oh.total_amount
            ELSE 0
        END) AS tot_electronic_lunch,
    sum(
        CASE
            WHEN oh.is_electronic_payment IS true AND oh.stat_order_day_part = ''D'' THEN oh.total_amount
            ELSE 0
        END) AS tot_electronic_dinner,
    sum(
        CASE
            WHEN oh.stat_order_day_part = ''L'' THEN oh.total_amount
            ELSE 0
        END) AS amount_lunch,
    sum(
        CASE
            WHEN oh.stat_order_day_part = ''D'' THEN oh.total_amount
            ELSE 0
        END) AS amount_dinner,
    sum(
        CASE
            WHEN oh.stat_order_day_part = ''L'' THEN oh.discount
            ELSE 0
        END) AS discount_lunch,
    sum(
        CASE
            WHEN oh.stat_order_day_part = ''D'' THEN oh.discount
            ELSE 0
        END) AS discount_dinner,
    sum(
        CASE
            WHEN oh.stat_order_day_part = ''L'' THEN oh.total_amount - oh.discount
            ELSE 0
        END) AS cash_lunch,
    sum(
        CASE
            WHEN oh.stat_order_day_part = ''D'' THEN oh.total_amount - oh.discount
            ELSE 0
        END) AS cash_dinner
   FROM order_header oh
   JOIN event ev ON oh.event = ev.id
   GROUP BY oh.event, ev.description, oh.stat_order_date
   ORDER BY ev.description, oh.stat_order_date;
COMMENT ON VIEW income_summary IS ''Sales summary view'';
ALTER VIEW income_summary OWNER TO *pyAppPgOwnerRole*;


DROP VIEW IF EXISTS bi_order_header;
CREATE VIEW bi_order_header AS
SELECT oh.event AS "ID Evento",
    ev.description AS "Evento",
    pr.description AS "Listino",
    oh.order_number AS "Num.Ordine",
    oh.order_date AS "Data",
    oh.order_time AS "Ora",
    oh.stat_order_date AS "Data Statistica",
    CASE oh.stat_order_day_part
        WHEN ''D'' THEN ''C''
        WHEN ''L'' THEN ''P''
        ELSE ''--''
    END AS "Pranzo/Cena",
    oh.delivery AS "Consegna",
    CASE oh.is_electronic_payment 
		WHEN true THEN ''E''
		ELSE ''C''
	END AS "Pagamento",
    oh.table_num AS "Tavolo",
    oh.customer_name AS "Nome cliente",
    oh.covers AS "Coperti",
    oh.total_amount AS "Importo ordine",
    oh.discount AS "Sconto",
    oh.cash AS "Incasso",
    oh.change AS "Resto"
FROM order_header oh
JOIN event ev ON oh.event = ev.id
LEFT JOIN price_list pr ON ev.price_list = pr.id;
COMMENT ON VIEW bi_order_header IS ''Order header for BI analysis view'';
ALTER VIEW bi_order_header OWNER TO *pyAppPgOwnerRole*;


DROP VIEW IF EXISTS bi_order_detail;
CREATE VIEW bi_order_detail AS
SELECT oh.event AS "ID Evento",
    ev.description AS "Evento",
    pr.description AS "Listino",
    oh.order_number AS "Num.Ordine",
    oh.order_date AS "Data",
    oh.order_time AS "Ora",
    oh.stat_order_date AS "Data Statistica",
    CASE oh.stat_order_day_part
        WHEN ''D'' THEN ''C''
        WHEN ''L'' THEN ''P''
        ELSE ''--''
    END AS "Pranzo/Cena",
    oh.delivery AS "Consegna",
    CASE oh.is_electronic_payment 
		WHEN true THEN ''E''
		ELSE ''C''
	END AS "Pagamento",
    oh.table_num AS "Tavolo",
    oh.customer_name AS "Nome cliente",
    de.description AS "Reparto",
    it.item_type AS "Tipo Articolo",
    it.description AS "Articolo",
    od.variants AS "Varianti",
    it.description::text || COALESCE('' ''::text || od.variants::text, ''''::text) AS "Articolo+Varianti",
    prd.price AS "Prezzo di Listino",
    od.quantity AS "Quantità",
    od.price AS "Prezzo Ordine",
    od.amount AS "Importo"
FROM order_detail od
JOIN order_header oh ON od.id_header = oh.id
JOIN event ev ON oh.event = ev.id
JOIN item it ON od.item = it.id
JOIN department de ON it.department = de.id
LEFT JOIN price_list pr ON ev.price_list = pr.id
LEFT JOIN price_list_detail prd ON pr.id = prd.id_price_list AND it.id = prd.item;
COMMENT ON VIEW bi_order_detail IS ''Order betail for BI analysis view'';
ALTER VIEW bi_order_detail OWNER TO *pyAppPgOwnerRole*;';

FOR c IN SELECT DISTINCT company_schema FROM system.company
	LOOP
		sql := replace(sql, '*pyAppPgOwnerRole*', owner_role);
		PERFORM set_config('search_path', c, false);
		EXECUTE sql;
	END LOOP;
END;
$$
language plpgsql;


-- Update script for new created companies

DELETE FROM system.sql_script 
WHERE script_group = 'new_company_schema'AND sorting = 1;

INSERT INTO system.sql_script (script_group, description, sorting, sql_script)
VALUES ('new_company_schema', 'New company schema definition', 1,
$script$

--
-- NEW COMPANY SCHEMA'S TABLES DEFINITION
--

-- this must be set before setting because the latter refers to the first
-- table: printer class
DROP TABLE IF EXISTS printer_class CASCADE;
CREATE TABLE printer_class (
    id integer GENERATED BY DEFAULT AS IDENTITY,
    description text NOT NULL,
    --
    user_ins text NOT NULL,
    date_ins timestamptz(3) NOT NULL,
    user_upd text NOT NULL,
    date_upd timestamptz(3) NOT NULL,
    row_timestamp timestamp NOT NULL,
    --
    CONSTRAINT printer_class_pkey PRIMARY KEY (id) USING INDEX TABLESPACE *pyAppPgIndexesTS*,
    CONSTRAINT printer_class_unique_description UNIQUE (description)
	
) TABLESPACE *pyAppPgTablesTS*;
COMMENT ON TABLE printer_class IS 'Printer classes definition table';
ALTER TABLE printer_class OWNER TO *pyAppPgOwnerRole*;

CREATE TRIGGER update_company_user_date BEFORE INSERT OR UPDATE ON printer_class  FOR EACH ROW EXECUTE PROCEDURE system.update_company_user_date();


-- table: printer class printer
DROP TABLE IF EXISTS printer_class_printer CASCADE;
CREATE TABLE printer_class_printer (
    id integer GENERATED BY DEFAULT AS IDENTITY,
    class_id int NOT NULL,
    computer text NOT NULL,
    printer text NOT NULL,
    --
    user_ins text NOT NULL,
    date_ins timestamptz(3) NOT NULL,
    user_upd text NOT NULL,
    date_upd timestamptz(3) NOT NULL,
    row_timestamp timestamp NOT NULL,
    --
    CONSTRAINT printer_class_printer_pkey PRIMARY KEY (id) USING INDEX TABLESPACE *pyAppPgIndexesTS*,
    CONSTRAINT printer_class_printer_class_fkey FOREIGN KEY (class_id) REFERENCES printer_class (id)
        MATCH SIMPLE ON UPDATE NO ACTION ON DELETE CASCADE,
    CONSTRAINT printer_class_printer_unique UNIQUE (class_id, computer)
) TABLESPACE *pyAppPgTablesTS*;
COMMENT ON TABLE printer_class_printer IS 'Printer classes printer definition table';
ALTER TABLE printer_class_printer OWNER TO *pyAppPgOwnerRole*;

CREATE TRIGGER update_company_user_date BEFORE INSERT OR UPDATE ON printer_class_printer  FOR EACH ROW EXECUTE PROCEDURE system.update_company_user_date();


-- company settings
CREATE TABLE setting (
    id boolean NOT NULL DEFAULT True,
    lunch_start_time integer NOT NULL DEFAULT 11,
    dinner_start_time integer NOT NULL DEFAULT 18,
	order_entry_ui integer NOT NULL DEFAULT 0,
    normal_background_color char(7) DEFAULT '#4141c5',
    normal_text_color char(7) DEFAULT '#FFFFFF',
    warning_background_color char(7) DEFAULT '#F0F032',
    warning_text_color char(7) DEFAULT '#000000',
    warning_stock_level int NOT NULL DEFAULT 10,
    critical_background_color char(7) DEFAULT '#C80000',
    critical_text_color char(7) DEFAULT '#FFFFFF',
    critical_stock_level int NOT NULL DEFAULT 5,
    disabled_background_color char(7) DEFAULT '#CBCBCB',
    disabled_text_color char(7) DEFAULT '#000000',
    default_delivery_type char(1) DEFAULT 'T',
    default_payment_type char(1) DEFAULT 'C', -- Cache or Electronic
    order_list_tab_position char NOT NULL DEFAULT 'N',
    order_list_rows int NOT NULL DEFAULT 4,
    order_list_columns int NOT NULL DEFAULT 4,
    order_list_spacing int NOT NULL DEFAULT 8,
    order_list_font_family varchar(60) NOT NULL DEFAULT 'Arial',
    order_list_font_size integer NOT NULL DEFAULT 12,
    print_customer_copy boolean NOT NULL DEFAULT False,
    print_department_copy boolean NOT NULL DEFAULT False,
    print_cover_copy boolean NOT NULL DEFAULT False,
    customer_copies int DEFAULT 1,
    department_copies int DEFAULT 1,
    cover_copies int DEFAULT 1,
    customer_report varchar(48),
    department_report varchar(48),
    cover_report varchar(48),
    customer_printer_class int,
    cover_printer_class int,
    max_covers integer NOT NULL DEFAULT 12,
	manage_order_progress boolean NOT NULL DEFAULT False,
    automatic_show_variants boolean NOT NULL DEFAULT False,
    always_show_stock_inventory boolean NOT NULL DEFAULT False,
    mandatory_table_number boolean NOT NULL DEFAULT True,
    use_table_list boolean NOT NULL DEFAULT True,
    table_list_rows int NOT NULL DEFAULT 8,
    table_list_columns int NOT NULL DEFAULT 8,
    table_list_spacing int NOT NULL DEFAULT 8,
    table_list_font_family varchar(60) NOT NULL DEFAULT 'Arial',
    table_list_font_size integer NOT NULL DEFAULT 12,
    check_inactivity boolean NOT NULL DEFAULT True,
    inactivity_time int NOT NULL DEFAULT 180,
    stock_unload_automatic_update boolean NOT NULL DEFAULT False,
    stock_unload_update_interval int NOT NULL DEFAULT 0,
    print_stock_unload_report boolean NOT NULL DEFAULT False,
	stock_unload_copies int DEFAULT 1,
    stock_unload_report varchar(48),
    stock_unload_printer_class int,
    num_orders_for_start_stock_unload int DEFAULT 30,
    num_orders_for_next_stock_unload int DEFAULT 10,
	quantity_decimal_places int NOT NULL DEFAULT 0,
	currency_symbol varchar(3) NOT NULL DEFAULT '€',
    --
    user_ins text NOT NULL,
    date_ins timestamptz(3) NOT NULL,
    user_upd text NOT NULL,
    date_upd timestamptz(3) NOT NULL,
    row_timestamp timestamp NOT NULL,
    --
    CONSTRAINT setting_pkey PRIMARY KEY (id) USING INDEX TABLESPACE *pyAppPgIndexesTS*,
    CONSTRAINT setting_check_pkey CHECK (id is True),
    CONSTRAINT setting_tab_position CHECK (order_list_tab_position IN ('N', 'S', 'E', 'W')),
    CONSTRAINT setting_customer_printer_class_fkey FOREIGN KEY (customer_printer_class) REFERENCES printer_class (id)
        MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION,
    CONSTRAINT setting_covers_printer_class_fkey FOREIGN KEY (cover_printer_class) REFERENCES printer_class (id)
        MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION,
    --CONSTRAINT setting_stock_unload_report_fkey FOREIGN KEY (stock_unload_report) REFERENCES system.report (id)
    --    MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION,
    CONSTRAINT setting_stock_unload_printer_class_fkey FOREIGN KEY (stock_unload_printer_class) REFERENCES printer_class (id)
        MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION,
    CONSTRAINT setting_default_delivery_type_check CHECK (default_delivery_type IN ('T', 'A')), -- Table, take-Away
    CONSTRAINT setting_default_payment_type_check CHECK (default_payment_type IN ('C', 'E')) -- Cache, Electronic

) TABLESPACE *pyAppPgTablesTS*;
COMMENT ON TABLE setting IS 'Company specific application settings';
ALTER TABLE setting OWNER TO *pyAppPgOwnerRole*;

CREATE TRIGGER update_company_user_date BEFORE INSERT OR UPDATE ON setting FOR EACH ROW EXECUTE PROCEDURE system.update_company_user_date();

INSERT INTO setting (id) VALUES (True); -- create one record filled with all default values


-- departments table
DROP TABLE IF EXISTS department CASCADE;
CREATE TABLE department (
    id integer GENERATED BY DEFAULT AS IDENTITY,
    description text NOT NULL,
    sorting int NOT NULL DEFAULT 1,
    printer_class int,
    is_obsolete boolean NOT NULL DEFAULT false,
    is_not_managed boolean NOT NULL DEFAULT false, -- used only in customer order copy
    is_for_takeaway boolean NOT NULL DEFAULT true,
    --
    user_ins text NOT NULL,
    date_ins timestamptz(3) NOT NULL,
    user_upd text NOT NULL,
    date_upd timestamptz(3) NOT NULL,
    row_timestamp timestamp NOT NULL,
    --
    CONSTRAINT department_pkey PRIMARY KEY (id) USING INDEX TABLESPACE *pyAppPgIndexesTS*,
    CONSTRAINT department_printer_class_fkey FOREIGN KEY (printer_class) REFERENCES printer_class (id)
        MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION,
	CONSTRAINT department_description_unique UNIQUE (description)

) TABLESPACE *pyAppPgTablesTS*;
COMMENT ON TABLE department IS 'Departments definition table';
ALTER TABLE department OWNER TO *pyAppPgOwnerRole*;

CREATE TRIGGER update_company_user_date BEFORE INSERT OR UPDATE ON department FOR EACH ROW EXECUTE PROCEDURE system.update_company_user_date();
   
   
-- numbered tables table
DROP TABLE IF EXISTS numbered_table CASCADE;
CREATE TABLE numbered_table (
    id integer GENERATED BY DEFAULT AS IDENTITY,
    table_code varchar(48) NOT NULL,
    pos_row integer NOT NULL,
    pos_column integer NOT NULL,
    text_color varchar(48) NOT NULL DEFAULT '#000000',
    background_color varchar(48) NOT NULL DEFAULT '#6ad59e',
    is_obsolete boolean NOT NULL DEFAULT true,
    --
    user_ins text NOT NULL,
    date_ins timestamptz(3) NOT NULL,
    user_upd text NOT NULL,
    date_upd timestamptz(3) NOT NULL,
    row_timestamp timestamp NOT NULL,
    --
    CONSTRAINT numbered_table_pkey PRIMARY KEY (id) USING INDEX TABLESPACE *pyAppPgIndexesTS*,
    CONSTRAINT numbered_table_unique UNIQUE (table_code),
    CONSTRAINT numbered_table_grid_position UNIQUE (pos_row, pos_column)

) TABLESPACE *pyAppPgTablesTS*;
COMMENT ON TABLE numbered_table IS 'Numbered table list';
ALTER TABLE numbered_table OWNER TO *pyAppPgOwnerRole*;

CREATE TRIGGER update_company_user_date BEFORE INSERT OR UPDATE ON numbered_table FOR EACH ROW EXECUTE PROCEDURE system.update_company_user_date();


-- items table
DROP TABLE IF EXISTS item CASCADE;
CREATE TABLE item (
    id integer GENERATED BY DEFAULT AS IDENTITY,
    item_type char NOT NULL DEFAULT 'I',
    description text NOT NULL,
    customer_description text NOT NULL,
    department integer NOT NULL,
    sorting integer NOT NULL DEFAULT 1,
    pos_row integer,
    pos_column integer,
	normal_background_color char(7) DEFAULT '#4141c5',
    normal_text_color char(7) DEFAULT '#FFFFFF',
    -- price numeric(12, 2) NOT NULL DEFAULT 0,
    has_variants boolean NOT NULL DEFAULT false,
    has_stock_control boolean NOT NULL DEFAULT true,
    has_unload_control boolean NOT NULL DEFAULT false,
    is_kit_part boolean NOT NULL DEFAULT false,
    is_menu_part boolean NOT NULL DEFAULT false,
    is_salable boolean NOT NULL DEFAULT false, -- = present in order dialog
	is_web_available boolean NOT NULL DEFAULT false, -- = present in web order
	web_sorting integer NOT NULL DEFAULT 0,
    is_obsolete boolean NOT NULL DEFAULT false,
    --
    user_ins text NOT NULL,
    date_ins timestamptz(3) NOT NULL,
    user_upd text NOT NULL,
    date_upd timestamptz(3) NOT NULL,
    row_timestamp timestamp NOT NULL,
    --
    CONSTRAINT item_pkey PRIMARY KEY (id) USING INDEX TABLESPACE *pyAppPgIndexesTS*,
    CONSTRAINT item_type_check CHECK (item_type IN ('I', 'K', 'M')),
    CONSTRAINT item_department_fkey FOREIGN KEY (department) REFERENCES department (id)
        MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION,
	CONSTRAINT item_description_unique UNIQUE (description),
	CONSTRAINT item_customer_description_unique UNIQUE (customer_description)

) TABLESPACE *pyAppPgTablesTS*;
COMMENT ON TABLE item IS 'Item table';
ALTER TABLE item OWNER TO *pyAppPgOwnerRole*;

CREATE UNIQUE INDEX item_grid_position ON item(department, pos_row, pos_column) WHERE is_salable IS true;

CREATE TRIGGER update_company_user_date BEFORE INSERT OR UPDATE ON item FOR EACH ROW EXECUTE PROCEDURE system.update_company_user_date();
   
   
-- item variations table
DROP TABLE IF EXISTS item_variant CASCADE;
CREATE TABLE item_variant (
    id integer GENERATED BY DEFAULT AS IDENTITY,
    item integer NOT NULL,
    variant_description text NOT NULL,
    sorting integer NOT NULL DEFAULT 1,
    price_delta numeric(12, 2) NOT NULL DEFAULT 0,
    --
    user_ins text NOT NULL,
    date_ins timestamptz(3) NOT NULL,
    user_upd text NOT NULL,
    date_upd timestamptz(3) NOT NULL,
    row_timestamp timestamp NOT NULL,
    --
    CONSTRAINT item_variant_pkey PRIMARY KEY (id) USING INDEX TABLESPACE *pyAppPgIndexesTS*,
    CONSTRAINT item_variant_item_fkey FOREIGN KEY (item) REFERENCES item (id)
        MATCH SIMPLE ON UPDATE NO ACTION ON DELETE CASCADE

) TABLESPACE *pyAppPgTablesTS*;
COMMENT ON TABLE item_variant IS 'Item variation table definition';
ALTER TABLE item_variant OWNER TO *pyAppPgOwnerRole*;

CREATE TRIGGER update_company_user_date BEFORE INSERT OR UPDATE ON item_variant FOR EACH ROW EXECUTE PROCEDURE system.update_company_user_date();
   
   
-- item parts for kit and menu
DROP TABLE IF EXISTS item_part CASCADE;
CREATE TABLE item_part (
    id integer GENERATED BY DEFAULT AS IDENTITY,
    item_type char NOT NULL,
    item integer NOT NULL,
    part integer NOT NULL,
    quantity numeric(12, 2) NOT NULL DEFAULT 1,
    --
    user_ins text NOT NULL,
    date_ins timestamptz(3) NOT NULL,
    user_upd text NOT NULL,
    date_upd timestamptz(3) NOT NULL,
    row_timestamp timestamp NOT NULL,
    --
    CONSTRAINT item_part_pkey PRIMARY KEY (id) USING INDEX TABLESPACE *pyAppPgIndexesTS*,
    CONSTRAINT item_part_item_type_check CHECK (item_type IN ('K', 'M')),
    CONSTRAINT item_part_item_fkey FOREIGN KEY (item) REFERENCES item (id)
        MATCH SIMPLE ON UPDATE NO ACTION ON DELETE CASCADE,
    CONSTRAINT item_part_part_fkey FOREIGN KEY (part) REFERENCES item (id)
        MATCH SIMPLE ON UPDATE NO ACTION ON DELETE CASCADE

) TABLESPACE *pyAppPgTablesTS*;
COMMENT ON TABLE item_part IS 'Item part table definition';
ALTER TABLE item_part OWNER TO *pyAppPgOwnerRole*;

CREATE TRIGGER update_company_user_date BEFORE INSERT OR UPDATE ON item_part FOR EACH ROW EXECUTE PROCEDURE system.update_company_user_date();


-- price list
DROP TABLE IF EXISTS price_list CASCADE;
CREATE TABLE price_list (
    id integer GENERATED BY DEFAULT AS IDENTITY,
	description text NOT NULL,
    --
    user_ins text NOT NULL,
    date_ins timestamptz(3) NOT NULL,
    user_upd text NOT NULL,
    date_upd timestamptz(3) NOT NULL,
    row_timestamp timestamp NOT NULL,
    --
    CONSTRAINT price_list_pkey PRIMARY KEY (id) USING INDEX TABLESPACE *pyAppPgIndexesTS*
		
) TABLESPACE *pyAppPgTablesTS*;
COMMENT ON TABLE price_list IS 'Price list table';
ALTER TABLE price_list OWNER TO *pyAppPgOwnerRole*;

CREATE TRIGGER update_company_user_date BEFORE INSERT OR UPDATE ON price_list FOR EACH ROW EXECUTE PROCEDURE system.update_company_user_date();


DROP TABLE IF EXISTS price_list_detail CASCADE;
CREATE TABLE price_list_detail (
    id integer GENERATED BY DEFAULT AS IDENTITY,
	id_price_list int,
    item integer NOT NULL,
    price numeric(12, 2) NOT NULL DEFAULT 0,
    --
    user_ins text NOT NULL,
    date_ins timestamptz(3) NOT NULL,
    user_upd text NOT NULL,
    date_upd timestamptz(3) NOT NULL,
    row_timestamp timestamp NOT NULL,
    --
    CONSTRAINT price_list_detail_pkey PRIMARY KEY (id) USING INDEX TABLESPACE *pyAppPgIndexesTS*,
	CONSTRAINT price_list_detail_id_price_list_fkey FOREIGN KEY (id_price_list) REFERENCES price_list (id)
        MATCH SIMPLE ON UPDATE NO ACTION ON DELETE CASCADE,
	CONSTRAINT price_list_detail_unique UNIQUE (id_price_list, item),
	CONSTRAINT price_list_detail_item_fkey FOREIGN KEY (item) REFERENCES item (id)
        MATCH SIMPLE ON UPDATE NO ACTION ON DELETE CASCADE
		
) TABLESPACE *pyAppPgTablesTS*;
COMMENT ON TABLE price_list_detail IS 'Price list prices';
ALTER TABLE price_list_detail OWNER TO *pyAppPgOwnerRole*;

CREATE TRIGGER update_company_user_date BEFORE INSERT OR UPDATE ON price_list_detail FOR EACH ROW EXECUTE PROCEDURE system.update_company_user_date();


-- event table 
DROP TABLE IF EXISTS event CASCADE;
CREATE TABLE event (
    id integer GENERATED BY DEFAULT AS IDENTITY,
    description text NOT NULL,
    date_start timestamptz(3) NOT NULL DEFAULT now(),
    date_end timestamptz(3) NOT NULL DEFAULT now(),
	price_list int NULL,
    image bytea,
    --
    user_ins text NOT NULL,
    date_ins timestamptz(3) NOT NULL,
    user_upd text NOT NULL,
    date_upd timestamptz(3) NOT NULL,
    row_timestamp timestamp NOT NULL,

    CONSTRAINT event_pkey PRIMARY KEY (id) USING INDEX TABLESPACE *pyAppPgIndexesTS*,
    CONSTRAINT event_check CHECK (date_end >= date_start),
    CONSTRAINT event_exclude_date_overlap EXCLUDE USING gist (tstzrange(date_start, date_end, '[]') WITH && ),
	CONSTRAINT event_price_list_fkey FOREIGN KEY (price_list) REFERENCES price_list (id)
		MATCH SIMPLE ON UPDATE NO ACTION ON DELETE SET NULL

) TABLESPACE *pyAppPgTablesTS*;
COMMENT ON TABLE event IS 'Event definition table';
ALTER TABLE event OWNER TO *pyAppPgOwnerRole*;

CREATE TRIGGER update_company_user_date BEFORE INSERT OR UPDATE ON event  FOR EACH ROW EXECUTE PROCEDURE system.update_company_user_date();


-- document numbers
DROP TABLE IF EXISTS numbering CASCADE;
CREATE TABLE numbering (
    id integer GENERATED BY DEFAULT AS IDENTITY,
    sequence_type varchar(48) NOT NULL,
    event integer NOT NULL,
    event_date date NULL,
    day_part CHAR NULL,
    current_value integer NOT NULL DEFAULT 0,
    --
    CONSTRAINT sequential_number_pkey PRIMARY KEY (id ) USING INDEX TABLESPACE *pyAppPgIndexesTS*,
    CONSTRAINT sequential_number_event_fkey FOREIGN KEY (event) REFERENCES event (id)
        MATCH SIMPLE ON UPDATE NO ACTION ON DELETE CASCADE,
    CONSTRAINT sequential_number_day_part CHECK (day_part IN ('L', 'D')) -- (L)unch / (D)inner

) TABLESPACE *pyAppPgTablesTS*;
COMMENT ON TABLE numbering IS 'This table stores current numbering for order';
ALTER TABLE numbering OWNER TO *pyAppPgOwnerRole*;


-- order header table
DROP TABLE IF EXISTS order_header CASCADE;
CREATE TABLE order_header (
    id integer GENERATED BY DEFAULT AS IDENTITY,
    event integer NOT NULL,
    date_time timestamptz(3) NOT NULL DEFAULT now(),
    order_number integer NOT NULL,
    order_date date NOT NULL,
    order_time time NOT NULL,
    stat_order_date date NOT NULL,
    stat_order_day_part CHAR NOT NULL,
	cash_desk text NOT NULL,
    delivery char(1) NOT NULL,
    is_electronic_payment boolean NOT NULL DEFAULT false,
    table_num varchar(10),
    customer_name varchar(60),
    covers integer,
    total_amount numeric(12, 2) NOT NULL DEFAULT 0,
    discount numeric(12, 2) NOT NULL DEFAULT 0,
    cash numeric(12, 2) NOT NULL DEFAULT 0,
    change numeric(12, 2) NOT NULL DEFAULT 0,
	status char NOT NULL DEFAULT 'A',
	fulfillment_date timestamptz(3) NULL,
    --
    user_ins text NOT NULL,
    date_ins timestamptz(3) NOT NULL,
    user_upd text NOT NULL,
    date_upd timestamptz(3) NOT NULL,
    row_timestamp timestamp NOT NULL,
    --
    CONSTRAINT order_header_pkey PRIMARY KEY (id ) USING INDEX TABLESPACE *pyAppPgIndexesTS*,
    CONSTRAINT order_header_delivery CHECK (delivery IN ('T', 'A')), -- (T)able or take(A)way
    CONSTRAINT order_header_payment CHECK (payment IN ('C', 'E')), -- (C)ache or (E)lectronic
    CONSTRAINT order_header_day_part CHECK (stat_order_day_part IN ('L', 'D')), -- (L)unch / (D)inner
	CONSTRAINT order_header_status CHECK (status IN ('A', 'I', 'P')), -- (A)quired, (I)in progress, (P)rocessed
    CONSTRAINT order_header_event_fkey FOREIGN KEY (event) REFERENCES event (id)
        MATCH SIMPLE ON UPDATE NO ACTION ON DELETE CASCADE,
    CONSTRAINT order_header_unique_docnum UNIQUE (event, order_number, order_date)

) TABLESPACE *pyAppPgTablesTS*;
COMMENT ON TABLE order_header IS 'Order headers table';
ALTER TABLE order_header OWNER TO *pyAppPgOwnerRole*;

CREATE TRIGGER update_numbering AFTER INSERT OR UPDATE ON order_header FOR EACH ROW EXECUTE PROCEDURE *pyAppCompanyCommonSchema*.update_numbering_table();
CREATE TRIGGER update_company_user_date BEFORE INSERT OR UPDATE ON order_header FOR EACH ROW EXECUTE PROCEDURE system.update_company_user_date();


-- order header department table
DROP TABLE IF EXISTS order_header_department CASCADE;
CREATE TABLE order_header_department (
    id integer GENERATED BY DEFAULT AS IDENTITY,
    id_header integer NOT NULL,
    department integer NOT NULL,
    note text,
    other_departments text,
	fulfillment_date timestamptz(3) NULL,
    --
    user_ins text NOT NULL,
    date_ins timestamptz(3) NOT NULL,
    user_upd text NOT NULL,
    date_upd timestamptz(3) NOT NULL,
    row_timestamp timestamp NOT NULL,
    --
    CONSTRAINT order_header_department_pkey PRIMARY KEY (id) USING INDEX TABLESPACE *pyAppPgIndexesTS*,
    CONSTRAINT order_header_department_id_header_fkey FOREIGN KEY (id_header) REFERENCES order_header (id)
        MATCH SIMPLE ON UPDATE NO ACTION ON DELETE CASCADE,
    CONSTRAINT order_header_department_department_fkey FOREIGN KEY (department) REFERENCES department (id)
        MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION

) TABLESPACE *pyAppPgTablesTS*;
COMMENT ON TABLE order_header_department IS 'Order headers table';
ALTER TABLE order_header_department OWNER TO *pyAppPgOwnerRole*;

CREATE TRIGGER update_order_header_status AFTER UPDATE ON order_header_department FOR EACH ROW EXECUTE PROCEDURE *pyAppCompanyCommonSchema*.order_header_status_update();
CREATE TRIGGER update_company_user_date BEFORE INSERT OR UPDATE ON order_header_department FOR EACH ROW EXECUTE PROCEDURE system.update_company_user_date();


-- order detail table (for customer)
DROP TABLE IF EXISTS order_detail CASCADE;
CREATE TABLE order_detail (
    id integer GENERATED BY DEFAULT AS IDENTITY,
    id_header integer NOT NULL,
    item integer NOT NULL,
    variants text,
    quantity numeric(12, 2) NOT NULL DEFAULT 1,
    price numeric(12, 2) NOT NULL DEFAULT 0,
    amount numeric(12, 2) NOT NULL DEFAULT 0,
    --
    user_ins text NOT NULL,
    date_ins timestamptz(3) NOT NULL,
    user_upd text NOT NULL,
    date_upd timestamptz(3) NOT NULL,
    row_timestamp timestamp NOT NULL,
    --
    CONSTRAINT order_detail_pkey PRIMARY KEY (id) USING INDEX TABLESPACE *pyAppPgIndexesTS*,
    CONSTRAINT order_detail_id_header_fkey FOREIGN KEY (id_header) REFERENCES order_header (id)
        MATCH SIMPLE ON UPDATE NO ACTION ON DELETE CASCADE,
    CONSTRAINT order_detail_item_fkey FOREIGN KEY (item) REFERENCES item (id)
        MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION

) TABLESPACE *pyAppPgTablesTS*;
COMMENT ON TABLE order_detail IS 'Order details table';
ALTER TABLE order_detail OWNER TO *pyAppPgOwnerRole*;

CREATE TRIGGER update_company_user_date BEFORE INSERT OR UPDATE ON order_detail FOR EACH ROW EXECUTE PROCEDURE system.update_company_user_date();


-- order detail department table (required for menu item that are present only in customer order but exploded in department order)
DROP TABLE IF EXISTS order_detail_department CASCADE;
CREATE TABLE order_detail_department (
    id integer GENERATED BY DEFAULT AS IDENTITY,
    id_header integer NOT NULL,
    event integer NOT NULL, -- for inventory trigger 
    event_date date NOT NULL, -- for unload trigger
    day_part CHAR NOT NULL, -- for unload trigger 
    department integer NOT NULL,
    item integer NOT NULL,
    variants text,
    quantity numeric(12, 2) NOT NULL DEFAULT 1,
    --
    user_ins text NOT NULL,
    date_ins timestamptz(3) NOT NULL,
    user_upd text NOT NULL,
    date_upd timestamptz(3) NOT NULL,
    row_timestamp timestamp NOT NULL,
    --
    CONSTRAINT order_detail_department_pkey PRIMARY KEY (id) USING INDEX TABLESPACE *pyAppPgIndexesTS*,
    CONSTRAINT order_detail_department_id_header_fkey FOREIGN KEY (id_header) REFERENCES order_header (id)
        MATCH SIMPLE ON UPDATE NO ACTION ON DELETE CASCADE,
    CONSTRAINT order_detail_department_event_fkey FOREIGN KEY (event) REFERENCES event (id)
        MATCH SIMPLE ON UPDATE NO ACTION ON DELETE CASCADE,
    CONSTRAINT order_detail_department_day_part CHECK (day_part IN ('L', 'D')), -- (L)unch / (D)inner
    CONSTRAINT order_detail_department_department_fkey FOREIGN KEY (department) REFERENCES department (id)
        MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION,
    CONSTRAINT order_detail_department_item_fkey FOREIGN KEY (item) REFERENCES item (id)
        MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION

) TABLESPACE *pyAppPgTablesTS*;
COMMENT ON TABLE order_detail_department IS 'Order detail departments table';
ALTER TABLE order_detail_department OWNER TO *pyAppPgOwnerRole*;

CREATE TRIGGER update_company_user_date BEFORE INSERT OR UPDATE ON order_detail_department FOR EACH ROW EXECUTE PROCEDURE system.update_company_user_date();

CREATE TRIGGER order_detail_to_unloaded AFTER INSERT OR UPDATE OR DELETE ON order_detail_department 
    FOR EACH ROW EXECUTE PROCEDURE *pyAppCompanyCommonSchema*.order_detail_to_unloaded();
-- CREATE TRIGGER order_to_unload_stock_unload AFTER INSERT OR UPDATE OR DELETE ON order_detail_department
    -- FOR EACH ROW EXECUTE PROCEDURE *pyAppCompanyCommonSchema*.order_to_unload_stock_unload();

    
-- stocks inventory table, record are manually inserted, this trigger only update records already present in table
DROP TABLE IF EXISTS stock_inventory CASCADE;
CREATE TABLE stock_inventory (
    id integer GENERATED BY DEFAULT AS IDENTITY,
    event integer NOT NULL,
    item integer NOT NULL,
    loaded numeric(12, 2) NOT NULL DEFAULT 0,
    unloaded numeric(12, 2) NOT NULL DEFAULT 0,
    balance numeric(12, 2) NOT NULL DEFAULT 0,
    --
    user_ins text NOT NULL,
    date_ins timestamptz(3) NOT NULL,
    user_upd text NOT NULL,
    date_upd timestamptz(3) NOT NULL,
    row_timestamp timestamp NOT NULL,
    --
    CONSTRAINT stock_inventory_pkey PRIMARY KEY (id) USING INDEX TABLESPACE *pyAppPgIndexesTS*,
    CONSTRAINT stock_inventory_event_fkey FOREIGN KEY (event) REFERENCES event (id)
        MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION,
    CONSTRAINT stock_inventory_item_fkey FOREIGN KEY (item) REFERENCES item (id)
        MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION,
    CONSTRAINT stock_inventory_unique_event_item UNIQUE (event, item)

) TABLESPACE *pyAppPgTablesTS*;
COMMENT ON TABLE stock_inventory IS 'Stocks summary table';
ALTER TABLE stock_inventory OWNER TO *pyAppPgOwnerRole*;

CREATE TRIGGER stock_inventory_balance AFTER INSERT OR UPDATE OF loaded, unloaded ON stock_inventory FOR EACH ROW EXECUTE PROCEDURE *pyAppCompanyCommonSchema*.stock_inventory_balance();
CREATE TRIGGER update_company_user_date BEFORE INSERT OR UPDATE ON stock_inventory  FOR EACH ROW EXECUTE PROCEDURE system.update_company_user_date();


-- stock unload report table
DROP TABLE IF EXISTS stock_unload CASCADE;
CREATE TABLE stock_unload (
    id integer GENERATED BY DEFAULT AS IDENTITY,
    event integer NOT NULL,
    event_date date NULL,
    day_part CHAR NULL,
    item integer NOT NULL,
    unloaded numeric(12, 2) DEFAULT 0,
    --
    CONSTRAINT stock_unload_pkey PRIMARY KEY (id) USING INDEX TABLESPACE *pyAppPgIndexesTS*,
    CONSTRAINT stock_unload_event_fkey FOREIGN KEY (event) REFERENCES event (id)
        MATCH SIMPLE ON UPDATE NO ACTION ON DELETE CASCADE,
    CONSTRAINT stock_unload_day_part CHECK (day_part IN ('L', 'D')),
    CONSTRAINT stock_unload_item_fkey FOREIGN KEY (item) REFERENCES item (id)
        MATCH SIMPLE ON UPDATE NO ACTION ON DELETE CASCADE,
    CONSTRAINT stock_unload_unique_record UNIQUE (event, event_date, day_part, item)

) TABLESPACE *pyAppPgTablesTS*;
COMMENT ON TABLE stock_unload IS 'Item  for stock unload report';
ALTER TABLE stock_unload OWNER TO *pyAppPgOwnerRole*;


-- web order header table
DROP TABLE IF EXISTS web_order_header CASCADE;
CREATE TABLE web_order_header (
    id integer GENERATED BY DEFAULT AS IDENTITY,
    date_time timestamptz(3) NOT NULL DEFAULT now(),
    delivery char NOT NULL,
    table_num varchar(10),
    customer_name varchar(60),
    covers integer,
    total_amount numeric(12, 2) NOT NULL DEFAULT 0,
	processed boolean NOT NULL DEFAULT false,
    --
    CONSTRAINT web_order_header_pkey PRIMARY KEY (id ) USING INDEX TABLESPACE *pyAppPgIndexesTS*,
    CONSTRAINT web_order_header_delivery CHECK (delivery IN ('T', 'A')) -- (T)able or take(A)way

) TABLESPACE *pyAppPgTablesTS*;
COMMENT ON TABLE web_order_header IS 'web order headers table';
ALTER TABLE web_order_header OWNER TO *pyAppPgOwnerRole*;


-- web order detail table (for customer)
DROP TABLE IF EXISTS web_order_detail CASCADE;
CREATE TABLE web_order_detail (
    id integer GENERATED BY DEFAULT AS IDENTITY,
    id_header integer NOT NULL,
    item integer NOT NULL,
    quantity numeric(12, 2) NOT NULL DEFAULT 1,
    price numeric(12, 2) NOT NULL DEFAULT 0,
    --
    CONSTRAINT web_order_detail_pkey PRIMARY KEY (id) USING INDEX TABLESPACE *pyAppPgIndexesTS*,
    CONSTRAINT web_order_detail_id_header_fkey FOREIGN KEY (id_header) REFERENCES web_order_header (id)
        MATCH SIMPLE ON UPDATE NO ACTION ON DELETE CASCADE,
    CONSTRAINT web_order_detail_item_fkey FOREIGN KEY (item) REFERENCES item (id)
        MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION

) TABLESPACE *pyAppPgTablesTS*;
COMMENT ON TABLE web_order_detail IS 'Web order details table';
ALTER TABLE web_order_detail OWNER TO *pyAppPgOwnerRole*;

--
-- VIEWS
--

-- item availability view
-- this could be placed in common schema BUT create and mantain this view in common result like a pain in ass...

CREATE OR REPLACE VIEW item_availability_detail AS
SELECT e.id AS event,
    e.description AS event_description,
    i.department AS department,
    d.description AS department_description,
    i.item_type AS item_type,
    i.id AS item,
    i.description AS item_description,
    i.is_salable AS salable,
    COALESCE(p.price, 0.00) AS price,
    COALESCE(i.pos_row, 0) AS pos_row,
    COALESCE(i.pos_column, 0) AS pos_column,
	i.normal_text_color,
	i.normal_background_color,
    i.has_stock_control AS stock_control,
    i.has_variants AS variants,
    COALESCE(s.quantity, 0.00) AS quantity, -- from stock_inventory
	i.is_web_available AS web_available,
	i.web_sorting
    FROM event e
    CROSS JOIN item i
    JOIN department d ON i.department = d.id
	LEFT JOIN price_list pl ON pl.id = e.price_list
	LEFT JOIN price_list_detail p ON p.id_price_list = pl.id AND p.item = i.id
    LEFT JOIN (
        -- regular items
        SELECT s.event AS event,
            i.id AS item, 
            COALESCE(s.balance, 0.00) AS quantity
        FROM item i
        LEFT JOIN (SELECT event, item, balance FROM stock_inventory) s ON  i.id = s.item
        WHERE i.item_type = 'I'
        UNION 
        -- kit items    
        SELECT t.event AS event,
            i.id AS item,
            round(min(t.quantity/ik.quantity), 2) AS quantity -- quantity is the minimum of each component quantity, link quantity
        FROM item i
        JOIN item_part ik ON ik.item = i.id
        JOIN (-- quantity for each child
            SELECT s.event AS event,
                k.part AS item,
                COALESCE(s.balance, 0.00) AS quantity
            FROM item_part k
            JOIN item pi ON k.part = pi.id
            LEFT JOIN (SELECT event,
                        item,
                        balance 
                   FROM stock_inventory 
                   ) s ON k.part = s.item
            WHERE pi.has_stock_control IS true AND pi.is_obsolete IS false
            ) t ON ik.part = t.item
        WHERE i.item_type = 'K'
        GROUP BY t.event, i.id
        UNION
        -- menu items
        SELECT s.event AS event,
            i.id AS item,
            round(min(s.quantity/im.quantity), 2) AS quantity -- quantity is the minimum of each component quantity, link quantity
        FROM item i
        JOIN item_part im ON i.id = im.item
        JOIN (
            -- regular items
            SELECT s.event AS event,
                i.id AS item,
                COALESCE(s.balance, 0.00) AS quantity
            FROM item i
            LEFT JOIN (SELECT event, item, balance FROM stock_inventory) s ON i.id = s.item
            WHERE i.item_type = 'I'
            UNION 
            -- kit items
            SELECT t.event AS event,
            i.id AS item,
            round(min(t.quantity/ik.quantity), 2) AS quantity -- quantity is the minimum of each component quantity, link quantity
            FROM item i
            JOIN item_part ik ON ik.item = i.id
            JOIN (-- quantity for each child
                SELECT s.event AS event,
                    k.part AS item,
                    COALESCE(s.balance, 0.00) AS quantity
                FROM item_part k
                JOIN item pi ON k.part = pi.id
                LEFT JOIN (SELECT event,
                            item,
                            balance 
                            FROM stock_inventory 
                            ) s ON k.part = s.item
                WHERE pi.has_stock_control IS true AND pi.is_obsolete IS false
                ) t ON ik.part = t.item
                WHERE i.item_type = 'K'
                GROUP BY t.event, i.id
            ) s ON im.part = s.item
            WHERE i.item_type = 'M'
            GROUP BY s.event, i.id
    ) s ON e.id = s.event AND i.id = s.item
WHERE i.is_obsolete IS false;
COMMENT ON VIEW item_availability_detail IS 'Item detail list with availability';
ALTER VIEW item_availability_detail OWNER TO *pyAppPgOwnerRole*;


CREATE OR REPLACE VIEW income_summary AS
SELECT oh.event,
    ev.description AS event_description,
    oh.stat_order_date AS order_date,
    count(
        CASE
            WHEN oh.stat_order_day_part = 'L' THEN oh.id
            ELSE NULL
        END) AS num_orders_lunch,
    count(
        CASE
            WHEN oh.stat_order_day_part = 'D' THEN oh.id
            ELSE NULL
        END) AS num_orders_dinner,
    sum(
        CASE
            WHEN oh.stat_order_day_part = 'L' THEN oh.covers
            ELSE 0
        END) AS num_covers_lunch,
    sum(
        CASE
            WHEN oh.stat_order_day_part = 'D' THEN oh.covers
            ELSE 0
        END) AS num_covers_dinner,
    sum(
        CASE
            WHEN oh.delivery = 'A' AND oh.stat_order_day_part = 'L' THEN oh.total_amount
            ELSE 0
        END) AS tot_take_away_lunch,
    sum(
        CASE
            WHEN oh.delivery = 'A' AND oh.stat_order_day_part = 'D' THEN oh.total_amount
            ELSE 0
        END) AS tot_take_away_dinner,
    sum(
        CASE
            WHEN oh.delivery = 'T' AND oh.stat_order_day_part = 'L' THEN oh.total_amount
            ELSE 0
        END) AS tot_table_lunch,
    sum(
        CASE
            WHEN oh.delivery = 'T' AND oh.stat_order_day_part = 'D' THEN oh.total_amount
            ELSE 0
        END) AS tot_table_dinner,
    sum(
        CASE
            WHEN oh.is_electronic_payment IS false AND oh.stat_order_day_part = 'L' THEN oh.total_amount
            ELSE 0
        END) AS tot_cash_lunch,
    sum(
        CASE
            WHEN oh.is_electronic_payment IS false AND oh.stat_order_day_part = 'D' THEN oh.total_amount
            ELSE 0
        END) AS tot_cash_dinner,
    sum(
        CASE
            WHEN oh.is_electronic_payment IS true AND oh.stat_order_day_part = 'L' THEN oh.total_amount
            ELSE 0
        END) AS tot_electronic_lunch,
    sum(
        CASE
            WHEN oh.is_electronic_payment IS true AND oh.stat_order_day_part = 'D' THEN oh.total_amount
            ELSE 0
        END) AS tot_electronic_dinner,
    sum(
        CASE
            WHEN oh.stat_order_day_part = 'L' THEN oh.total_amount
            ELSE 0
        END) AS amount_lunch,
    sum(
        CASE
            WHEN oh.stat_order_day_part = 'D' THEN oh.total_amount
            ELSE 0
        END) AS amount_dinner,
    sum(
        CASE
            WHEN oh.stat_order_day_part = 'L' THEN oh.discount
            ELSE 0
        END) AS discount_lunch,
    sum(
        CASE
            WHEN oh.stat_order_day_part = 'D' THEN oh.discount
            ELSE 0
        END) AS discount_dinner,
    sum(
        CASE
            WHEN oh.stat_order_day_part = 'L' THEN oh.total_amount - oh.discount
            ELSE 0
        END) AS cash_lunch,
    sum(
        CASE
            WHEN oh.stat_order_day_part = 'D' THEN oh.total_amount - oh.discount
            ELSE 0
        END) AS cash_dinner
   FROM order_header oh
   JOIN event ev ON oh.event = ev.id
   GROUP BY oh.event, ev.description, oh.stat_order_date
   ORDER BY ev.description, oh.stat_order_date;
COMMENT ON VIEW income_summary IS 'Sales summary view';
ALTER VIEW income_summary OWNER TO *pyAppPgOwnerRole*;


CREATE OR REPLACE VIEW bi_order_header AS
SELECT oh.event AS "ID Evento",
    ev.description AS "Evento",
    pr.description AS "Listino",
    oh.order_number AS "Num.Ordine",
    oh.order_date AS "Data",
    oh.order_time AS "Ora",
    oh.stat_order_date AS "Data Statistica",
    CASE oh.stat_order_day_part
        WHEN 'D' THEN 'C'
        WHEN 'L' THEN 'P'
        ELSE '--'
    END AS "Pranzo/Cena",
    oh.delivery AS "Consegna",
    CASE oh.is_electronic_payment 
		WHEN true THEN 'E'
		ELSE 'C'
	END AS "Pagamento",
    oh.table_num AS "Tavolo",
    oh.customer_name AS "Nome cliente",
    oh.covers AS "Coperti",
    oh.total_amount AS "Importo ordine",
    oh.discount AS "Sconto",
    oh.cash AS "Incasso",
    oh.change AS "Resto"
FROM order_header oh
JOIN event ev ON oh.event = ev.id
LEFT JOIN price_list pr ON ev.price_list = pr.id;
COMMENT ON VIEW bi_order_header IS 'Order header for BI analysis view';
ALTER VIEW bi_order_header OWNER TO *pyAppPgOwnerRole*;


CREATE OR REPLACE VIEW bi_order_detail AS
SELECT oh.event AS "ID Evento", 
    ev.description AS "Evento",
    pr.description AS "Listino",
    oh.order_number AS "Num.Ordine",
    oh.order_date AS "Data",
    oh.order_time AS "Ora",
    oh.stat_order_date AS "Data Statistica",
    CASE oh.stat_order_day_part
        WHEN 'D' THEN 'C'
        WHEN 'L' THEN 'P'
        ELSE '--'
    END AS "Pranzo/Cena",
    oh.delivery AS "Consegna",
    CASE oh.is_electronic_payment 
		WHEN true THEN 'E'
		ELSE 'C'
	END AS "Pagamento",
    oh.table_num AS "Tavolo",
    oh.customer_name AS "Nome cliente",
    de.description AS "Reparto",
    it.item_type AS "Tipo Articolo",
    it.description AS "Articolo",
    od.variants AS "Varianti",
    it.description::text || COALESCE(' '::text || od.variants::text, ''::text) AS "Articolo+Varianti",
    prd.price AS "Prezzo di Listino",
    od.quantity AS "Quantità",
    od.price AS "Prezzo Ordine",
    od.amount AS "Importo",
FROM order_detail od
JOIN order_header oh ON od.id_header = oh.id
JOIN event ev ON oh.event = ev.id
JOIN item it ON od.item = it.id
JOIN department de ON it.department = de.id
LEFT JOIN price_list pr ON ev.price_list = pr.id
LEFT JOIN price_list_detail prd ON pr.id = prd.id_price_list AND it.id = prd.item;
COMMENT ON VIEW bi_order_detail IS 'Order betail for BI analysis view';
ALTER VIEW bi_order_detail OWNER TO *pyAppPgOwnerRole*;

-- END
$script$);

-- Update database version
SELECT 
system.pa_setting_set('inst_version', '02.01.00'),
system.pa_setting_set('inst_date', now()::text);

-- END --


