--
-- **************************
-- ** APPLICATION DATABASE **
-- **************************
--

-- Paolo De Stefani 01.2025

-- This script MUST be executed by postgres user or a postgres like user
-- Connected to a database ("postgres" database is OK)

---------------------------------
-- APPLICATION DB ARCHITECTURE --
---------------------------------

-- * one database {pyAppPgDataBase}
-- * one role that own the database {pyAppPgOwnerRole} without login privilege
-- * one login role {pyAppPgLoginRole} that inherit {pyAppPgOwnerRole} privileges

-- Every database has 4 schemas:
-- * system     for system objects
-- * common     for common objects that are shared with all companies
-- * company    for objects associated with a company
-- * temp       for temporary tables

-- This set of variables will be be resolved before executing the scripts:
-- {pyAppPgOwnerRole}           = PostgresSQL Role that own all db objects without login privilege
-- {pyAppPgDataBase}            = Postgres database name
-- {pyAppPgLoginRole}           = PostgresSQL Role used for standard login users
-- {pyAppPgLoginPassword}       = Password for pyAppPgLoginRole
-- {pyAppName}                  = Python application name
-- {pyAppDescription}           = Python application description
-- {pyAppVersionMajor}          = Application version major number
-- {pyAppVersionMinor}          = Application version minor number
-- {pyAppVersionPatch}          = Application version patch number
-- {pyAppVersionTag}            = Application version tag
-- {pyAppVersionDescription}    = Application version description
-- {pyAppPgDataBaseTS}          = Database table space (MUST be created before script execution)
-- {pyAppPgTablesTS}            = Tables table space (MUST be created before script execution)
-- {pyAppPgIndexesTS}           = Indexes table space (MUST be created before script execution)


----------------------------
-- COMPANY SCHEMA OBJECTS --
----------------------------

SET search_path = company;

--
-- VIEWS
--

-- item availability view
CREATE OR REPLACE VIEW vw_item_availability AS
SELECT 
    e.company_id                AS company_id,
    e.event_id                  AS event_id,
    e.description               AS event_description,
    i.department_id             AS department_id,
    d.description               AS department_description,
    i.item_type                 AS item_type,
    i.item_id                   AS item_id,
    i.description               AS item_description,
    i.customer_description      AS item_customer_description,
    i.is_salable                AS is_salable,
    COALESCE(p.price, 0.00)     AS price,
    COALESCE(i.pos_row, 0)      AS pos_row,
    COALESCE(i.pos_column, 0)   AS pos_column,
	i.normal_text_color         AS normal_text_color,
	i.normal_background_color   AS normal_background_color,
    i.has_inventory_control     AS has_inventory_control,
    i.has_delivered_control     AS has_delivered_control,
    i.has_variants              AS has_variants,
    COALESCE(s.available, 0.00) AS available, -- from items inventory
	i.is_web_available          AS is_web_available,
	i.web_sorting				AS web_sorting,
    CASE i.has_inventory_control
		WHEN true AND s.available > 0 THEN true
		WHEN false THEN true
		ELSE false
	END                         AS is_available
    FROM company.event e
    LEFT JOIN company.item i ON e.company_id = i.company_id
    JOIN company.department d ON i.department_id = d.department_id
	LEFT JOIN company.price_list pl ON pl.price_list_id = e.price_list_id
	LEFT JOIN company.price_list_item p ON p.price_list_id = pl.price_list_id AND p.item_id = i.item_id
    LEFT JOIN (
        -- regular items
        SELECT 
            s.event_id                  AS event,
            i.item_id                   AS item, 
            coalesce(s.available, 0.00) AS available
        FROM company.item i
        LEFT JOIN ( SELECT event_id, item_id, available 
                    FROM company.inventory) s ON  i.item_id = s.item_id
        WHERE i.item_type = 'I'
        UNION 
        -- kit items    
        SELECT 
            t.event		    AS event,
            i.item_id 	    AS item,
            round(min(t.available/ik.quantity), 2) AS available -- quantity is the minimum of each component quantity, link quantity
        FROM company.item i
        JOIN company.item_part ik ON ik.item_id = i.item_id
        JOIN (-- quantity for each child
            SELECT 
                s.event_id  AS event,
                k.part_id   AS item,
                coalesce(s.available, 0.00) AS available
            FROM company.item_part k
            JOIN company.item pi ON k.part_id = pi.item_id
            LEFT JOIN ( SELECT event_id, item_id, available 
                        FROM company.inventory 
                        ) s ON k.part_id = s.item_id
            WHERE pi.has_inventory_control IS true 
                AND pi.is_obsolete IS false
            ) t ON ik.part_id = t.item
        WHERE i.item_type = 'K'
        GROUP BY t.event, i.item_id
        UNION
        -- menu items
        SELECT 
            s.event 		AS event,
            i.item_id		AS item,
            round(min(s.available/im.quantity), 2) AS available -- quantity is the minimum of each component quantity, link quantity
        FROM company.item i
        JOIN company.item_part im ON i.item_id = im.item_id
        JOIN (
            -- regular items
            SELECT 
                s.event_id	   AS event,
                i.item_id      AS item,
                COALESCE(s.available, 0.00) AS available
            FROM company.item i
            LEFT JOIN (	SELECT event_id, item_id, available 
						FROM company.inventory) s ON i.item_id = s.item_id
            WHERE i.item_type = 'I'
            UNION 
            -- kit items
            SELECT 
                t.event AS event,
                i.item_id AS item,
                round(min(t.available/ik.quantity), 2) AS available -- available is the minimum of each component quantity, link quantity
            FROM company.item i
            JOIN company.item_part ik ON ik.item_id = i.item_id
            JOIN (-- quantity for each child
                SELECT 
                    s.event_id 	AS event,
                    k.part_id 	AS item,
                    coalesce(s.available, 0.00) AS available
                FROM company.item_part k
                JOIN company.item pi ON k.part_id = pi.item_id
                LEFT JOIN (	SELECT event_id, item_id, available 
                            FROM company.inventory 
                            ) s ON k.part_id = s.item_id
                WHERE pi.has_inventory_control IS true 
                    AND pi.is_obsolete IS false
                ) t ON ik.part_id = t.item
                WHERE i.item_type = 'K'
                GROUP BY t.event, i.item_id
            ) s ON im.part_id = s.item
            WHERE i.item_type = 'M'
            GROUP BY s.event, i.item_id
    ) s ON e.event_id = s.event AND i.item_id = s.item
WHERE i.is_obsolete IS false;

COMMENT ON VIEW vw_item_availability IS 
    'Item detail list with availability';
ALTER VIEW vw_item_availability 
    OWNER TO {pyAppPgOwnerRole};

-- Sales summary view
CREATE OR REPLACE VIEW vw_sales_summary AS
SELECT 
    oh.company_id           AS company_id,
    oh.event_id             AS event_id,
    ev.description          AS event_description,
    ev.start_date           AS start_date,
    ev.end_date             AS end_date,
    oh.stat_order_date      AS order_date,
    count(
        CASE
            WHEN oh.stat_order_day_part = 'L' THEN oh.order_header_id
            ELSE NULL
        END)                AS num_orders_lunch,
    count(
        CASE
            WHEN oh.stat_order_day_part = 'D' THEN oh.order_header_id
            ELSE NULL
        END)                AS num_orders_dinner,
    sum(
        CASE
            WHEN oh.stat_order_day_part = 'L' THEN oh.covers
            ELSE 0
        END)                AS num_covers_lunch,
    sum(
        CASE
            WHEN oh.stat_order_day_part = 'D' THEN oh.covers
            ELSE 0
        END)                AS num_covers_dinner,
    sum(
        CASE
            WHEN oh.delivery = 'A' AND oh.stat_order_day_part = 'L' THEN oh.total_amount
            ELSE 0
        END)                AS take_away_lunch,
    sum(
        CASE
            WHEN oh.delivery = 'A' AND oh.stat_order_day_part = 'D' THEN oh.total_amount
            ELSE 0
        END)                AS take_away_dinner,
    sum(
        CASE
            WHEN oh.delivery = 'T' AND oh.stat_order_day_part = 'L' THEN oh.total_amount
            ELSE 0
        END)                AS table_lunch,
    sum(
        CASE
            WHEN oh.delivery = 'T' AND oh.stat_order_day_part = 'D' THEN oh.total_amount
            ELSE 0
        END)                AS table_dinner,
    sum(
        CASE
            WHEN oh.stat_order_day_part = 'L' THEN oh.total_amount
            ELSE 0
        END)                AS amount_lunch,
    sum(
        CASE
            WHEN oh.stat_order_day_part = 'D' THEN oh.total_amount
            ELSE 0
        END)                AS amount_dinner,
    sum(
        CASE
            WHEN oh.stat_order_day_part = 'L' THEN oh.discount
            ELSE 0
        END)                AS discount_lunch,
    sum(
        CASE
            WHEN oh.stat_order_day_part = 'D' THEN oh.discount
            ELSE 0
        END)                AS discount_dinner,
    sum(
        CASE
            WHEN oh.is_electronic_payment IS true AND oh.stat_order_day_part = 'L' THEN oh.total_amount - oh.discount
            ELSE 0
        END)                AS electronic_lunch,
    sum(
        CASE
            WHEN oh.is_electronic_payment IS true AND oh.stat_order_day_part = 'D' THEN oh.total_amount - oh.discount
            ELSE 0
        END)                AS electronic_dinner,
	sum(
        CASE
            WHEN oh.is_electronic_payment IS false AND oh.stat_order_day_part = 'L' THEN oh.total_amount - oh.discount
            ELSE 0
        END)                AS cash_lunch,
    sum(
        CASE
            WHEN oh.is_electronic_payment IS false AND oh.stat_order_day_part = 'D' THEN oh.total_amount - oh.discount
            ELSE 0
        END)                AS cash_dinner,
	sum(
        CASE
            WHEN oh.stat_order_day_part = 'L' THEN oh.total_amount - oh.discount
            ELSE 0
        END)                AS total_lunch,
	sum(
        CASE
            WHEN oh.stat_order_day_part = 'D' THEN oh.total_amount - oh.discount
            ELSE 0
        END)                AS total_dinner
FROM order_header oh
JOIN event ev ON oh.event_id = ev.event_id
GROUP BY oh.company_id, oh.event_id, ev.description, ev.start_date, ev.end_date, oh.stat_order_date
ORDER BY oh.company_id, ev.description, oh.stat_order_date;

COMMENT ON VIEW vw_sales_summary IS 
    'Sales summary view';
ALTER VIEW vw_sales_summary 
    OWNER TO {pyAppPgOwnerRole};


-- order status view
CREATE OR REPLACE VIEW  vw_order_status
AS
SELECT 
	oh.company_id 	        AS company_id,
	c.description	        AS company_description,
    oh.event_id		        AS event_id,
	e.description	        AS event_description,
	oh.order_header_id	    AS order_header_id,
	oh.order_date	        AS order_date,
    oh.stat_order_date      AS stat_order_date,
	oh.stat_order_day_part  AS stat_order_day_part,
	oh.order_date_time	    AS order_date_time,
	oh.order_number	        AS order_number,
	oh.delivery		        AS delivery,
	oh.table_num	        AS table_number,
	oh.customer_name	    AS customer_name,
	oh.covers		        AS covers,
	oh.status		        AS status,
	oh.fulfillment_date	    AS fulfillment_date,
    oh.cash_desk	        AS cash_desk,
	oh.created_by	        AS user_ins,
	oh.is_from_web	        AS from_web,
	-- department status
	od.dep1			        AS department1,
	od.fulfill1	            AS fulfillment1,
	od.dep2			        AS department2,
	od.fulfill2	            AS fulfillment2,
	od.dep3			        AS department3,
	od.fulfill3	            AS fulfillment3,
	od.dep4			        AS department4,
	od.fulfill4	            AS fulfillment4,
	od.dep5			        AS department5,
	od.fulfill5	            AS fulfillment5,
	od.dep6			        AS department6,
	od.fulfill6	            AS fulfillment6
FROM order_header oh
JOIN system.company c ON oh.company_id = c.company_id
JOIN event e ON oh.event_id = e.event_id
JOIN ( 	-- one row for evey order_header_id
		-- with department data in line
	SELECT
		i.order_header_id AS order_header_id,
		max(CASE i.dn WHEN 1 THEN i.department ELSE Null END) AS dep1,
		max(CASE i.dn WHEN 1 THEN i.fulfillment_date ELSE Null END) AS fulfill1,
		max(CASE i.dn WHEN 2 THEN i.department ELSE Null END) AS dep2,
		max(CASE i.dn WHEN 2 THEN i.fulfillment_date ELSE Null END) AS fulfill2,
		max(CASE i.dn WHEN 3 THEN i.department ELSE Null END) AS dep3,
		max(CASE i.dn WHEN 3 THEN i.fulfillment_date ELSE Null END) AS fulfill3,
		max(CASE i.dn WHEN 4 THEN i.department ELSE Null END) AS dep4,
		max(CASE i.dn WHEN 4 THEN i.fulfillment_date ELSE Null END) AS fulfill4,
		max(CASE i.dn WHEN 5 THEN i.department ELSE Null END) AS dep5,
		max(CASE i.dn WHEN 5 THEN i.fulfillment_date ELSE Null END) AS fulfill5,
		max(CASE i.dn WHEN 6 THEN i.department ELSE Null END) AS dep6,
		max(CASE i.dn WHEN 6 THEN i.fulfillment_date ELSE Null END) AS fulfill6
	FROM (
		SELECT
			ohd.order_header_id,
			ROW_NUMBER () OVER (
							PARTITION BY ohd.order_header_id 
							ORDER BY ohd.order_header_id, d.sorting) AS dn,
			d.description AS department,
			ohd.fulfillment_date
		FROM company.order_header_department ohd
		JOIN company.department d ON ohd.department_id = d.department_id
		) i
	GROUP BY i.order_header_id
	) od ON od.order_header_id = oh.order_header_id;

COMMENT ON VIEW vw_order_status IS 
    'Order status view';
ALTER VIEW vw_order_status 
    OWNER TO {pyAppPgOwnerRole};


-- business intellligence header view
CREATE OR REPLACE VIEW bi_order_header AS
SELECT 
    ev.company_id           	    AS company_id,
    ev.description          	    AS event,
    oh.order_number         	    AS order_number,
    oh.order_date::text  		    AS order_date,
    oh.order_time::text			    AS order_time,
    oh.order_date_time::text      	    AS order_date_time,  
    oh.fulfillment_date::text	    AS fulfillment_date, 
    oh.stat_order_date::text	    AS stat_order_date,
    oh.stat_order_day_part  	    AS stat_order_day_part,
    oh.cash_desk            	    AS cash_desk,
    oh.delivery             	    AS delivery,
    CASE oh.is_electronic_payment 
		WHEN true THEN 'E'
		ELSE 'C'
	END                     	    AS payment,
    oh.is_from_web          	    AS web_order,
    oh.table_num            	    AS table_num,
    oh.customer_name        	    AS customer_name,
    oh.customer_contact     	    AS customer_contact,
    oh.covers               	    AS covers,
    oh.total_amount         	    AS total_amount,
    oh.discount             	    AS discount,
    oh.cash                 	    AS cash
FROM order_header oh
JOIN event ev ON oh.event_id = ev.event_id;

COMMENT ON VIEW bi_order_header IS 
    'Order header for BI analysis view';
ALTER VIEW bi_order_header 
    OWNER TO {pyAppPgOwnerRole};


-- business intellligence detail view
CREATE OR REPLACE VIEW bi_order_line AS
SELECT 
    ev.company_id       		    AS company_id,
    ev.description				    AS event,
    oh.order_number				    AS order_number,
    oh.order_date::text			    AS order_date,
    oh.order_time::text			    AS order_time,
    oh.stat_order_date::text	    AS stat_order_date,
    oh.stat_order_day_part 		    AS stat_order_day_part,
    oh.delivery         		    AS delivery,
    CASE oh.is_electronic_payment 
		WHEN true THEN 'E'
		ELSE 'C'
	END                 		    AS payment,
    oh.table_num        		    AS table_number,
    oh.customer_name    		    AS customer_name,
    de.description      		    AS department,
    it.item_type        		    AS item_type,
    it.description      		    AS item,
    ol.variants         		    AS variants,
    it.description::text || COALESCE(' '::text || ol.variants::text, ''::text) AS item_with_variants,
    ol.quantity         		    AS quantity,
    ol.price            		    AS price,
    ol.amount           		    AS amount
FROM order_line ol
JOIN order_header oh ON ol.order_header_id = oh.order_header_id
JOIN event ev ON oh.event_id = ev.event_id
JOIN item it ON ol.item_id = it.item_id
JOIN department de ON it.department_id = de.department_id
LEFT JOIN price_list pr ON ev.price_list_id = pr.price_list_id
LEFT JOIN price_list_item pri ON pr.price_list_id = pri.price_list_id AND it.item_id = pri.item_id;

COMMENT ON VIEW bi_order_line IS 
    'Order detail for BI analysis view';
ALTER VIEW bi_order_line 
    OWNER TO {pyAppPgOwnerRole};

