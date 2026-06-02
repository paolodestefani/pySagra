--
-- Execute in the new database after restore the schema of the company to be imported
-- 
-- This is for bidasio company, "bidasio" schema, new company code 30
-- Execute one table at a time
--
-- 1 Clean previous import
-- 2 Create users (in script) from user_ins of order_header
-- 3 Create a specific company (in script) number 30
-- 4 Set default profile/medu/toolbar to all user for the company 30
-- 5 Import data disabling triggers for faster execution
-- 6 Update inventory, ordered delivered and numbering
-- 7 Reindex tables

SET search_path = system, common, company;

DO $$ BEGIN RAISE NOTICE '% Set path', clock_timestamp(); END; $$;

--
-- DELETE PREVIOUS IMPORT
--

-- Drop company, also disable triggers and rebuild/reindex

DO $$ BEGIN RAISE NOTICE '% BEGIN Drop company 30', clock_timestamp(); END; $$;

SELECT system.pa_company_drop(30);

DO $$ BEGIN RAISE NOTICE '% END Drop company 30', clock_timestamp(); END; $$;

-- delete users from importing company
DELETE FROM system.app_user
WHERE user_code IN (
	SELECT DISTINCT
		user_ins
	FROM bidasio.order_header
	WHERE user_ins NOT IN ('postgres', 'system', 'utente')
	);

DO $$ BEGIN RAISE NOTICE '% Deleted users', clock_timestamp(); END; $$;


--
-- BEGIN COMPANY IMPORT
--

--
-- create users from order_header
--

INSERT INTO system.app_user (
	user_code,
	description,
	user_password,
	is_admin,
	l10n,
	is_system_object)
SELECT
	u.user_ins AS code,
	u.user_ins AS description,
	system.crypt(u.user_ins, system.gen_salt('bf')) AS user_password, -- password is set as user_name
	false AS is_admin,
	'it_IT' AS l10n,
	False AS is_system_object
FROM (
	SELECT DISTINCT
		user_ins
	FROM bidasio.order_header
	WHERE user_ins NOT IN ('postgres', 'system', 'utente')
	) u
ON CONFLICT DO NOTHING;

DO $$ BEGIN RAISE NOTICE '% Imported users', clock_timestamp(); END; $$;


--
-- create company
--

SELECT system.pa_company_create(30, 'Bidasio', false, Null);

DO $$ BEGIN RAISE NOTICE '% Created new company 30', clock_timestamp(); END; $$;


--
-- Set default profile/menu/toolbar to all imported users for company 30
--

INSERT INTO system.app_user_company (
	app_user_code,
	company_id, 
	profile_code,
	menu_code,
	toolbar_code)
SELECT 
	u.user_ins,
	30,
	'default',
	'm_default_it',
	't_default_it'
FROM (
	SELECT DISTINCT
		user_ins
	FROM bidasio.order_header
	WHERE user_ins NOT IN ('postgres', 'system', 'utente')
	) u
ON CONFLICT DO NOTHING;
-- set profile/menu/toolbar for system user
INSERT INTO system.app_user_company (
	app_user_code,
	company_id, 
	profile_code,
	menu_code,
	toolbar_code)
VALUES ('system', 30, 'full', 'm_full_en', 't_full_en')
ON CONFLICT DO NOTHING;

DO $$ BEGIN RAISE NOTICE '% Set profile/menu/toolbar for users on company 30', clock_timestamp(); END; $$;


--
-- DISABLE TRIGGERS AND REINDEX
--

DO $$ 
DECLARE
s text;
t text;
n text;
BEGIN 
	-- disable trigger
	-- can't use DISABLE TRIGGER ALL because is available only for superuser
	FOR s, t, n IN
		SELECT DISTINCT trigger_schema, event_object_table, trigger_name
		FROM information_schema.triggers
		WHERE trigger_catalog = current_database() 
			AND trigger_schema = 'company'
	LOOP
		EXECUTE format('ALTER TABLE %s.%s DISABLE TRIGGER %s', s, t, n);
	END LOOP;

	-- re-index
	FOR s, t IN 	
		SELECT table_schema, table_name
		FROM information_schema.tables
		WHERE table_catalog = current_database() 
			AND table_type = 'BASE TABLE'
			AND table_schema = 'company'
	LOOP
		EXECUTE format('REINDEX TABLE %s.%s', s, t);
	END LOOP;
END;
$$;


--
-- Import events
--

INSERT INTO company.event (
	external_code,
	company_id,
	description,
	start_date,
	end_date,
	image,
	created_by,
	created_at,
	updated_by,
	updated_at,
	object_version)
SELECT
	id,				-- external_code
	30,				-- company_id
	description,	-- description
	date_start,		-- date_start
	date_end,		-- date_end
	image,			-- image
	user_ins,		-- created_by
	date_ins, 		-- created_at
	user_upd,		-- updated_by
	date_upd,		-- updated_at
	0				-- object_version
FROM bidasio.event;

DO $$ BEGIN RAISE NOTICE '% Imported events', clock_timestamp(); END; $$;


--
-- Import printer class
--

INSERT INTO company.printer_class (
	external_code,
	company_id,
	description,
	created_by,
	created_at,
	updated_by,
	updated_at,
	object_version)
SELECT 
	id,				-- external_code
	30,				-- company_id
	description,	-- description
	user_ins,		-- created_by
	date_ins,		-- created_at
	user_upd,		-- updated_by
	date_upd,		-- updated_at
	0				-- object_version
FROM bidasio.printer_class;

DO $$ BEGIN RAISE NOTICE '% Imported printer class', clock_timestamp(); END; $$;


--
-- Import printer class printer
--

INSERT INTO company.printer_class_printer (
	external_code,
	company_id,
	printer_class_id,
	computer,
	printer,
	created_by,
	created_at,
	updated_by,
	updated_at,
	object_version)
SELECT 
	b.id,				-- external_code
	30,					-- company_id
	c.printer_class_id,	-- class_id
	b.computer,			-- computer
	b.printer,			-- printer
	b.user_ins,			-- created_by
	b.date_ins,			-- created_at
	b.user_upd,			-- updated_by
	b.date_upd,			-- updated_at
	0					-- object_version
FROM bidasio.printer_class_printer b
JOIN company.printer_class c ON b.class_id = c.external_code AND c.company_id = 30;

DO $$ BEGIN RAISE NOTICE '% Imported printer class printer', clock_timestamp(); END; $$;


--
-- Import settings
--

WITH par AS (
	SELECT 
		30 AS company_id,
		b.lunch_start_time,
		b.dinner_start_time,
		b.normal_background_color,
		b.normal_text_color,
		b.warning_background_color,
		b.warning_text_color,
		b.warning_stock_level,
		b.critical_background_color,
		b.critical_text_color,
		b.critical_stock_level,
		b.disabled_background_color,
		b.disabled_text_color,
		b.default_delivery_type,
		-- b.default_payment_type,
		b.order_list_tab_position,
		b.order_list_rows,
		b.order_list_columns,
		b.order_list_spacing,
		b.order_list_font_family,
		b.order_list_font_size,
		b.print_customer_copy,
		b.print_department_copy,
		b.print_cover_copy,
		b.customer_copies,
		b.department_copies,
		b.cover_copies,
		b.customer_report,
		b.department_report,
		b.cover_report,
		c1.printer_class_id AS customer_printer_class,
		c2.printer_class_id AS cover_printer_class,
		b.max_covers,
		b.manage_order_progress,
		b.automatic_show_variants,
		b.always_show_stock_inventory,
		b.mandatory_table_number,
		b.use_table_list,
		b.table_list_rows,
		b.table_list_columns,
		b.table_list_spacing,
		b.table_list_font_family,
		b.table_list_font_size,
		b.check_inactivity,
		b.inactivity_time,
		b.stock_unload_automatic_update,
		b.stock_unload_update_interval,
		b.print_stock_unload_report,
		b.stock_unload_copies,
		b.stock_unload_report,
		c3.printer_class_id AS stock_unload_printer_class,
		b.num_orders_for_start_stock_unload,
		b.num_orders_for_next_stock_unload,
		b.quantity_decimal_places,
		b.currency_symbol
	FROM bidasio.setting b
	LEFT JOIN company.printer_class c1 ON b.customer_printer_class = c1.external_code AND c1.company_id = 30
	LEFT JOIN company.printer_class c2 ON b.cover_printer_class = c2.external_code AND c2.company_id = 30
	LEFT JOIN company.printer_class c3 ON b.stock_unload_printer_class = c3.external_code AND c3.company_id = 30
	WHERE b.id IS true
)
UPDATE company.setting
SET lunch_start_time = par.lunch_start_time,
	dinner_start_time = par.dinner_start_time,
	--normal_background_color = par.normal_background_color,
	--normal_text_color = par.normal_text_color,
	warning_background_color = par.warning_background_color,
	warning_text_color = par.warning_text_color,
	warning_stock_level = par.warning_stock_level,
	critical_background_color = par.critical_background_color,
	critical_text_color = par.critical_text_color,
	critical_stock_level = par.critical_stock_level,
	disabled_background_color = par.disabled_background_color,
	disabled_text_color = par.disabled_text_color,
	default_delivery_type = par.default_delivery_type,
	-- default_payment_type = par.default_payment_type,
	order_list_tab_position = par.order_list_tab_position,
	order_list_rows = par.order_list_rows,
	order_list_columns = par.order_list_columns,
	order_list_spacing = par.order_list_spacing,
	order_list_font_family = par.order_list_font_family,
	order_list_font_size = par.order_list_font_size,
	print_customer_copy = par.print_customer_copy,
	print_department_copy = par.print_department_copy,
	print_cover_copy = par.print_cover_copy,
	customer_copies = par.customer_copies,
	department_copies = par.department_copies,
	cover_copies = par.cover_copies,
	customer_report = par.customer_report,
	department_report = par.department_report,
	cover_report = par.cover_report,
	customer_printer_class = par.customer_printer_class,
	cover_printer_class = par.cover_printer_class,
	max_covers = par.max_covers,
	manage_order_progress = par.manage_order_progress,
	automatic_show_variants = par.automatic_show_variants,
	always_show_stock_inventory = par.always_show_stock_inventory,
	mandatory_table_number = par.mandatory_table_number,
	use_table_list = par.use_table_list,
	table_list_rows = par.table_list_rows,
	table_list_columns = par.table_list_columns,
	table_list_spacing = par.table_list_spacing,
	table_list_font_family = par.table_list_font_family,
	table_list_font_size = par.table_list_font_size,
	check_inactivity = par.check_inactivity,
	inactivity_time = par.inactivity_time,
	ordered_delivered_automatic_update = par.stock_unload_automatic_update,
	ordered_delivered_update_interval = par.stock_unload_update_interval,
	print_ordered_delivered_report = par.print_stock_unload_report,
	ordered_delivered_copies = par.stock_unload_copies,
	ordered_delivered_report = par.stock_unload_report,
	ordered_delivered_printer_class = par.stock_unload_printer_class,
	quantity_decimal_places = par.quantity_decimal_places,
	currency_symbol = par.currency_symbol
FROM par
WHERE company.setting.company_id = par.company_id; 

DO $$ BEGIN RAISE NOTICE '% Updated settings', clock_timestamp(); END; $$;


--
-- Import departments
--

INSERT INTO company.department (
	external_code,
	company_id,
	description, 
	sorting, 
	printer_class_id, 
	is_obsolete, 
	is_menu_container, 
	is_for_takeaway,
	created_by,
	created_at,
	updated_by,
	updated_at,
	object_version)
SELECT 
	b.id, 				-- external_code
	30,					-- company_id
	b.description,		-- description
	b.sorting,			-- sorting
	p.printer_class_id,	-- printer_class
	b.is_obsolete,		-- is_obsolete
	b.is_not_managed,	-- is_menu_container
	b.is_for_takeaway, 	-- is_for_takeaway
	b.user_ins, 		-- created_by
	b.date_ins,			-- created_at
	b.user_upd,			-- updated_by
	b.date_upd,			-- updated_at
	0					-- object_version
FROM bidasio.department b
JOIN company.printer_class p ON b.printer_class = p.external_code AND p.company_id = 30;

-- add a temporary department used for items that not have a department (happened)
-- set created/delete/etc because trigger are disabled
INSERT INTO company.department (
	company_id, 
	description,
	is_obsolete,
	is_menu_container,
	is_for_takeaway,
	created_by,
	created_at,
	updated_by,
	updated_at,
	object_version)
VALUES (
	30,
	'*** REPARTO MANCANTE ***',
	true,
	false,
	false,
	system.pa_current_user(),
	now(),
	system.pa_current_user(),
	now(),
	0); 

DO $$ BEGIN RAISE NOTICE '% Imported departments', clock_timestamp(); END; $$;


--
-- Import seat map
--

INSERT INTO company.seat_map (
	external_code,
	company_id,
	table_code,
	pos_row,
	pos_column,
	text_color,
	background_color,
	is_obsolete,
	created_by,
	created_at,
	updated_by,
	updated_at,
	object_version)
SELECT
	id,					-- external_code
	30, 				-- company_id
	table_code,			-- table_code
	pos_row,			-- pos_row
	pos_column,			-- pos_column
	text_color,			-- text_color
	background_color,	-- background_color
	is_obsolete,		-- is_obsolete
	user_ins,			-- created_by
	date_ins,			-- created_at
	user_upd,			-- updated_by
	date_upd,			-- updated_at
	0					-- object_version
FROM bidasio.numbered_table;

DO $$ BEGIN RAISE NOTICE '% Imported tables', clock_timestamp(); END; $$;


--
-- Import items
--

INSERT INTO company.item (
	external_code,
	company_id,
	item_type, 
	description, 
	customer_description,
	department_id,
	sorting,
	pos_row,
	pos_column,
	normal_background_color,
	normal_text_color,
	has_variants,
	has_inventory_control,
	has_delivered_control,
	is_kit_part,
	is_menu_part,
	is_salable,
	is_web_available,
	web_sorting,
	is_obsolete,
	created_by,
	created_at,
	updated_by,
	updated_at,
	object_version)
SELECT 
	b.id,						-- external_code
	30, 						-- company_id
	b.item_type,				-- item_type
	b.description,				-- description
	b.customer_description,		-- customer_description
	coalesce(d.department_id, m.department_id),		-- department_id
	b.sorting,					-- sorting
	b.pos_row,					-- pos_row
	b.pos_column,				-- pos_column
	upper(b.normal_background_color),		-- normal_background_color
	upper(b.normal_text_color),				-- normal_text_color
	b.has_variants,				-- has_variants
	b.has_stock_control,		-- has_stock_control
	b.has_unload_control,		-- has_unload_control
	b.is_kit_part,				-- is_kit_part
	b.is_menu_part,				-- is_menu_part
	b.is_salable,				-- is_salable
	b.is_web_available,			-- is_web_available
	b.web_sorting,				-- web_sorting
	b.is_obsolete,				-- is_obsolete
	b.user_ins,					-- created_by
	b.date_ins,					-- created_at
	b.user_upd,					-- updated_by
	b.date_upd,					-- updated_at
	0							-- object_version
FROM bidasio.item b
LEFT JOIN company.department d ON b.department = d.external_code AND d.company_id = 30
CROSS JOIN (
	SELECT department_id
	FROM company.department 
	WHERE company_id = 30 
		AND description = '*** REPARTO MANCANTE ***') m;

DO $$ BEGIN RAISE NOTICE '% Imported items', clock_timestamp(); END; $$;


--
-- Import item variants
--

INSERT INTO company.item_variant (
	external_code,
	company_id,
	item_id, 
	variant_description, 
	sorting, 
	price_delta,
	created_by,
	created_at,
	updated_by,
	updated_at,
	object_version)
SELECT 
	b.id,					-- external_code
	30, 					-- company_id
	i.item_id,					-- item_id
	b.variant_description,	-- variant_description
	b.sorting,				-- sorting
	b.price_delta,			-- price_delta
	b.user_ins,				-- created_by
	b.date_ins,				-- created_at
	b.user_upd,				-- updated_by
	b.date_upd,				-- updated_at
	0						-- object_version
FROM bidasio.item_variant b
LEFT JOIN company.item i ON b.item = i.external_code AND i.company_id = 30;

DO $$ BEGIN RAISE NOTICE '% Imported item variants', clock_timestamp(); END; $$;


--
-- Import item parts
--

INSERT INTO company.item_part (
	external_code,
	company_id,
	item_type, 
	item_id,
	part_id, 
	quantity,
	created_by,
	created_at,
	updated_by,
	updated_at,
	object_version)
SELECT
	b.id,			-- external_code
	30,				-- company_id
	b.item_type,	-- item_type
	i1.item_id,		-- item_id
	i2.item_id,		-- part_id
	b.quantity,		-- quantity
	b.user_ins,		-- created_by
	b.date_ins,		-- created_at
	b.user_upd,		-- updated_by
	b.date_upd,		-- updated_at
	0				-- object_version
FROM bidasio.item_part b
LEFT JOIN company.item i1 ON b.item = i1.external_code AND i1.company_id = 30
LEFT JOIN company.item i2 ON b.part = i2.external_code AND i2.company_id = 30;

DO $$ BEGIN RAISE NOTICE '% Imported item parts', clock_timestamp(); END; $$;


--
-- Import price list
--

INSERT INTO company.price_list (
	external_code,
	company_id,
	description,
	created_by,
	created_at,
	updated_by,
	updated_at,
	object_version)
SELECT
	id,				-- external_code,
	30,				-- company_id,
	description,	-- description
	user_ins,		-- created_by
	date_ins,		-- created_at
	user_upd,		-- updated_by
	date_upd,		-- updated_at
	0				-- object_version
FROM bidasio.price_list;

DO $$ BEGIN RAISE NOTICE '% Imported price list', clock_timestamp(); END; $$;


--
-- Import price list items
--

INSERT INTO company.price_list_item (
	external_code,
	company_id,
	price_list_id, 
	item_id, 
	price,
	created_by,
	created_at,
	updated_by,
	updated_at,
	object_version)
SELECT
    b.id,				-- external_code
	30, 				-- company_id
	l.price_list_id,	-- price_list_id
	i.item_id,	 		-- item_id
    b.price,			-- price
    b.user_ins,			-- created_by
    b.date_ins,			-- created_at
    b.user_upd,			-- updated_by
    b.date_upd,			-- updated_at
    0 					-- object_version
FROM bidasio.price_list_detail b
LEFT JOIN company.price_list l ON b.id_price_list = l.external_code AND l.company_id = 30
LEFT JOIN company.item i ON b.item = i.external_code AND i.company_id = 30;

DO $$ BEGIN RAISE NOTICE '% Imported price list items', clock_timestamp(); END; $$;


--
-- Import inventory
--

INSERT INTO company.inventory (
	external_code,
	company_id,
	event_id, 
	item_id, 
	loaded,
	created_by,
	created_at,
	updated_by,
	updated_at,
	object_version)
SELECT
    b.id,				-- external_code
	30, 				-- company_id
	e.event_id,			-- event_id
	i.item_id,	 		-- item_id
    b.loaded,			-- loaded
    b.user_ins,			-- created_by
    b.date_ins,			-- created_at
    b.user_upd,			-- updated_by
    b.date_upd,			-- updated_at
    0 					-- object_version
FROM bidasio.stock_inventory b
LEFT JOIN company.event e ON b.event = e.external_code AND e.company_id = 30
LEFT JOIN company.item i ON b.item = i.external_code AND i.company_id = 30;

DO $$ BEGIN RAISE NOTICE '% Imported items inventory', clock_timestamp(); END; $$;


-- 
-- Import order header
--

DO $$ BEGIN RAISE NOTICE '% BEGIN Import order headers', clock_timestamp(); END; $$;

INSERT INTO company.order_header (
	external_code,
	company_id,
	event_id,
	date_time,
	order_number,
	order_date,
	order_time,
	stat_order_date,
	stat_order_day_part,
	cash_desk,
	delivery,
	table_num,
	customer_name,
	covers,
	total_amount,
	discount,
	cash,
	change, 
	--is_electronic_payment,
	status,
	fulfillment_date,
	created_by,
	created_at,
	updated_by,
	updated_at,
	object_version)
SELECT 
	b.id, 					-- external_code,
	30, 					-- company_id,
	e.event_id, 			-- event_id,
	b.date_time,			-- date_time
	b.order_number,			-- order_number
	b.order_date,			-- order_date
	b.order_time,			-- order_time
	b.stat_order_date,		-- stat_order_date
	b.stat_order_day_part,	-- stat_order_day_part
	b.cash_desk,			-- cash_desk
	b.delivery,				-- delivery
	b.table_num,			-- table_num
	b.customer_name,		-- customer_name
	b.covers,				-- covers
	b.total_amount,			-- total_amount
	b.discount,				-- discount
	b.cash,					-- cash
	b.change,				-- change
	--is_electronic_payment, -- is_electronic_payment
	b.status,				-- status
	b.fulfillment_date,	-- fulfillment_date
	b.user_ins,				-- created_by
	b.date_ins,				-- created_at
	b.user_upd,				-- updated_by
	b.date_upd,				-- updated_at
	0 						-- object_version
FROM bidasio.order_header b
LEFT JOIN company.event e ON b.event = e.external_code AND e.company_id=30;

DO $$ BEGIN RAISE NOTICE '% END Import order headers', clock_timestamp(); END; $$;


--
-- Import order header department
--

DO $$ BEGIN RAISE NOTICE '% BEGIN Import order header departments', clock_timestamp(); END; $$;

INSERT INTO company.order_header_department (
	external_code,
	company_id,
	order_header_id, 
	department_id,
	note,
	other_departments,
	fulfillment_date,
	created_by,
	created_at,
	updated_by,
	updated_at,
	object_version)
SELECT 
	b.id, 					-- external_code
	30, 					-- company_id
	h.order_header_id,		-- header_id 
	d.department_id, 		-- department_id
	b.note,					-- note
	b.other_departments, 	-- other_departments
	b.fulfillment_date, 	-- fulfillment_date
	b.user_ins,				-- created_by
	b.date_ins,				-- created_at
	b.user_upd,				-- updated_by
	b.date_upd,				-- updated_at
	0						-- object_version
FROM bidasio.order_header_department b
LEFT JOIN company.order_header h ON b.id_header = h.external_code AND h.company_id = 30
LEFT JOIN company.department d ON b.department = d.external_code AND d.company_id = 30;

DO $$ BEGIN RAISE NOTICE '% END Import order header departments', clock_timestamp(); END; $$;


--
-- Import order line
--

DO $$ BEGIN RAISE NOTICE '% BEGIN Import order lines', clock_timestamp(); END; $$;

INSERT INTO company.order_line (
	external_code,
	company_id,
	order_header_id, 
	item_id, 
	variants, 
	quantity, 
	price, 
	amount,
	created_by,
	created_at,
	updated_by,
	updated_at,
	object_version)
SELECT 
	b.id, 				-- external_code
	30,					-- company_id
	h.order_header_id, 	-- header_id
	i.item_id,			-- item_id
	b.variants,			-- variants
	b.quantity,			-- quantity
	b.price,			-- price
	b.amount,			-- amount
	b.user_ins,			-- created_by
	b.date_ins,			-- created_at
	b.user_upd,			-- updated_by
	b.date_upd,			-- updated_at 
	0 					-- object_version
FROM bidasio.order_detail b
LEFT JOIN company.order_header h ON b.id_header = h.external_code AND h.company_id = 30
LEFT JOIN company.item i ON b.item = i.external_code AND i.company_id = 30;

DO $$ BEGIN RAISE NOTICE '% END Import order lines', clock_timestamp(); END; $$;


--
-- Import order line departments
--

DO $$ BEGIN RAISE NOTICE '% BEGIN Import order line departments', clock_timestamp(); END; $$;

INSERT INTO company.order_line_department (
	external_code,
	company_id,
	order_header_department_id, 
	event_id, 
	event_date, 
	day_part, 
	item_id, 
	variants,
	quantity,
	created_by,
	created_at,
	updated_by,
	updated_at,
	object_version)
SELECT 
	b.id,				-- external_code
	30,					-- company_id
	x.order_header_department_id,	-- order_header_department_id
	e.event_id,			-- event_id
	b.event_date,		-- event_date
	b.day_part,			-- day_part
	i.item_id,			-- item_id
	b.variants,			-- variants
	b.quantity,			-- quantity
	b.user_ins,			-- created_by
	b.date_ins, 		-- created_at
	b.user_upd, 		-- updated_by
	b.date_upd, 		-- updated_at
	0 					-- object_version
FROM bidasio.order_detail_department b
LEFT JOIN company.order_header h ON b.id_header = h.external_code AND h.company_id = 30
LEFT JOIN company.event e ON b.event = e.external_code AND e.company_id = 30
LEFT JOIN company.department d ON b.department = d.external_code AND d.company_id = 30
LEFT JOIN company.order_header_department x ON h.order_header_id = x.order_header_id AND d.department_id = x.department_id
LEFT JOIN company.item i ON b.item = i.external_code AND i.company_id = 30;

DO $$ BEGIN RAISE NOTICE '% END Import order line departments', clock_timestamp(); END; $$;


--
-- update inventory, ordered delivered and numbering
--

-- this should speedup everything

REINDEX TABLE company.order_header;
REINDEX TABLE company.order_header_department;
REINDEX TABLE company.order_line;
REINDEX TABLE company.order_line_department;

DO $$ BEGIN RAISE NOTICE '% BEGIN Update inventory, ordered delivered and numbering', clock_timestamp(); END; $$;

DO $$
DECLARE
i int;
BEGIN

	FOR i IN 	
		SELECT event_id 
		FROM company.event 
		WHERE company_id = 30
		ORDER BY event_id
	LOOP
		RAISE NOTICE '% BEGIN Event % Rebuild numbering', clock_timestamp(), i;
		PERFORM company.numbering_rebuild(i);
		RAISE NOTICE '% END   Event % Rebuild numbering', clock_timestamp(), i;
		RAISE NOTICE '% BEGIN Event % Rebuild inventory', clock_timestamp(), i;
		PERFORM company.inventory_rebuild(i);
		RAISE NOTICE '% END   Event % Rebuild inventory', clock_timestamp(), i;
		RAISE NOTICE '% BEGIN Event % Rebuild ordered delivered', clock_timestamp(), i;
		PERFORM company.ordered_delivered_rebuild(i);
		RAISE NOTICE '% END   Event % Rebuild ordered delivered', clock_timestamp(), i;
	END LOOP;
	
END;
$$
language plpgsql;

DO $$ BEGIN RAISE NOTICE '% END Update inventory, ordered delivered and numbering', clock_timestamp(); END; $$;


--
-- RE-ENABLE TRIGGERS AND REINDEX
--

DO $$ 
DECLARE
s text;
t text;
n text;
BEGIN 
	-- enable trigger
	-- can't use DISABLE TRIGGER ALL because is available only for superuser
	FOR s, t, n IN
		SELECT DISTINCT trigger_schema, event_object_table, trigger_name
		FROM information_schema.triggers
		WHERE trigger_catalog = current_database() 
			AND trigger_schema = 'company'
	LOOP
		EXECUTE format('ALTER TABLE %s.%s ENABLE TRIGGER %s', s, t, n);
	END LOOP;

	-- re-index
	FOR s, t IN 	
		SELECT table_schema, table_name
		FROM information_schema.tables
		WHERE table_catalog = current_database() 
			AND table_type = 'BASE TABLE'
			AND table_schema = 'company'
	LOOP
		EXECUTE format('REINDEX TABLE %s.%s', s, t);
	END LOOP;
END;
$$;

-- END

