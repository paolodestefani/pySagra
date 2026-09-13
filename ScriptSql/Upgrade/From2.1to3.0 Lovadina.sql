--
-- Execute in the new database after restore the schema of the company to be imported
-- 
-- This is for lovadina company, "lovadina" schema, new company code 40
-- Execute one table at a time
--
-- 1 Clean previous import
-- 2 Create users (in script) from user_ins of order_header
-- 3 Create a specific company (in script) numeber 40
-- 4 Set default profile/medu/toolbar to all user for the company 40
-- 5 Import data disabling triggers for faster execution
-- 6 Update inventory, ordered delivered and numbering
-- 7 Reindex tables

SET search_path = system, common, company;

DO $$ BEGIN RAISE NOTICE '% Set path', clock_timestamp(); END; $$;


--
-- DELETE PREVIOUS IMPORT
--

-- Drop company

DO $$ BEGIN RAISE NOTICE '% BEGIN Drop company 40', clock_timestamp(); END; $$;

SELECT system.pa_company_drop(40);

DO $$ BEGIN RAISE NOTICE '% END Drop company 40', clock_timestamp(); END; $$;

-- delete users from importing company
DELETE FROM system.app_user
WHERE user_code IN (
	SELECT DISTINCT
		user_ins
	FROM lovadina.order_header
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
	FROM lovadina.order_header
	WHERE user_ins NOT IN ('postgres', 'system', 'utente')
	) u
ON CONFLICT DO NOTHING;

DO $$ BEGIN RAISE NOTICE '% Imported users', clock_timestamp(); END; $$;


--
-- create company
--

SELECT system.pa_company_create(40, 'Lovadina', false, Null);

DO $$ BEGIN RAISE NOTICE '% Created new company 40', clock_timestamp(); END; $$;


--
-- Set default profile/menu/toolbar to all users for company 40
--

INSERT INTO system.app_user_company (
	app_user_code,
	company_id, 
	profile_code,
	menu_code,
	toolbar_code)
SELECT 
	u.user_ins,
	40,
	'default',
	'm_default_it',
	't_default_it'
FROM (
	SELECT DISTINCT
		user_ins
	FROM lovadina.order_header
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
VALUES ('system', 40, 'full', 'm_full_en', 't_full_en')
ON CONFLICT DO NOTHING;

DO $$ BEGIN RAISE NOTICE '% Set profile/menu/toolbar for users on company 40', clock_timestamp(); END; $$;


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
	40,				-- company_id
	description,	-- description
	date_start,		-- date_start
	date_end,		-- date_end
	image,			-- image
	user_ins,		-- created_by
	date_ins, 		-- created_at
	user_upd,		-- updated_by
	date_upd,		-- updated_at
	0				-- object_version
FROM lovadina.event;

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
	40,				-- company_id
	description,	-- description
	user_ins,		-- created_by
	date_ins,		-- created_at
	user_upd,		-- updated_by
	date_upd,		-- updated_at
	0				-- object_version
FROM lovadina.printer_class;

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
	l.id,				-- external_code
	40,					-- company_id
	c.printer_class_id,	-- class_id
	l.computer,			-- computer
	l.printer,			-- printer
	l.user_ins,			-- created_by
	l.date_ins,			-- created_at
	l.user_upd,			-- updated_by
	l.date_upd,			-- updated_at
	0					-- object_version
FROM lovadina.printer_class_printer l
JOIN company.printer_class c ON l.class_id = c.external_code AND c.company_id = 40;

DO $$ BEGIN RAISE NOTICE '% Imported printer class printer', clock_timestamp(); END; $$;


--
-- Import settings
--

WITH par AS (
	SELECT 
		40 AS company_id,
		l.lunch_start_time,
		l.dinner_start_time,
		l.normal_background_color,
		l.normal_text_color,
		l.warning_background_color,
		l.warning_text_color,
		l.warning_stock_level,
		l.critical_background_color,
		l.critical_text_color,
		l.critical_stock_level,
		l.disabled_background_color,
		l.disabled_text_color,
		l.default_delivery_type,
		-- l.default_payment_type,
		l.order_list_tab_position,
		l.order_list_rows,
		l.order_list_columns,
		l.order_list_spacing,
		l.order_list_font_family,
		l.order_list_font_size,
		l.print_customer_copy,
		l.print_department_copy,
		l.print_cover_copy,
		l.customer_copies,
		l.department_copies,
		l.cover_copies,
		l.customer_report,
		l.department_report,
		l.cover_report,
		c1.printer_class_id AS customer_printer_class,
		c2.printer_class_id AS cover_printer_class,
		l.max_covers,
		l.manage_order_progress,
		l.automatic_show_variants,
		l.always_show_stock_inventory,
		l.mandatory_table_number,
		l.use_table_list,
		l.table_list_rows,
		l.table_list_columns,
		l.table_list_spacing,
		l.table_list_font_family,
		l.table_list_font_size,
		l.check_inactivity,
		l.inactivity_time,
		l.stock_unload_automatic_update,
		l.stock_unload_update_interval,
		l.print_stock_unload_report,
		l.stock_unload_copies,
		l.stock_unload_report,
		c3.printer_class_id AS stock_unload_printer_class,
		l.num_orders_for_start_stock_unload,
		l.num_orders_for_next_stock_unload,
		l.quantity_decimal_places,
		l.currency_symbol
	FROM lovadina.setting l
	LEFT JOIN company.printer_class c1 ON l.customer_printer_class = c1.external_code AND c1.company_id = 40
	LEFT JOIN company.printer_class c2 ON l.cover_printer_class = c2.external_code AND c2.company_id = 40
	LEFT JOIN company.printer_class c3 ON l.stock_unload_printer_class = c3.external_code AND c3.company_id = 40
	WHERE l.id IS true
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
	l.id, 				-- external_code
	40,					-- company_id
	l.description,		-- description
	l.sorting,			-- sorting
	p.printer_class_id,	-- printer_class
	l.is_obsolete,		-- is_obsolete
	l.is_not_managed,	-- is_menu_container
	l.is_for_takeaway, 	-- is_for_takeaway
	l.user_ins, 		-- created_by
	l.date_ins,			-- created_at
	l.user_upd,			-- updated_by
	l.date_upd,			-- updated_at
	0					-- object_version
FROM lovadina.department l
JOIN company.printer_class p ON l.printer_class = p.external_code AND p.company_id = 40;

-- add a temporary department used for items that not have a department
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
	40,
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
	40, 				-- company_id
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
FROM lovadina.numbered_table;

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
	l.id,						-- external_code
	40, 						-- company_id
	l.item_type,				-- item_type
	l.description,				-- description
	l.customer_description,		-- customer_description
	coalesce(d.department_id, m.department_id),		-- department_id
	l.sorting,					-- sorting
	l.pos_row,					-- pos_row
	l.pos_column,				-- pos_column
	upper(l.normal_background_color),		-- normal_background_color
	upper(l.normal_text_color),				-- normal_text_color
	l.has_variants,				-- has_variants
	l.has_stock_control,		-- has_stock_control
	l.has_unload_control,		-- has_unload_control
	l.is_kit_part,				-- is_kit_part
	l.is_menu_part,				-- is_menu_part
	l.is_salable,				-- is_salable
	l.is_web_available,			-- is_web_available
	l.web_sorting,				-- web_sorting
	l.is_obsolete,				-- is_obsolete
	l.user_ins,					-- created_by
	l.date_ins,					-- created_at
	l.user_upd,					-- updated_by
	l.date_upd,					-- updated_at
	0							-- object_version
FROM lovadina.item l
LEFT JOIN company.department d ON l.department = d.external_code AND d.company_id = 40
CROSS JOIN (
	SELECT department_id
	FROM company.department 
	WHERE company_id = 40 
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
	l.id,					-- external_code
	40, 					-- company_id
	i.item_id,				-- item_id
	l.variant_description,	-- variant_description
	l.sorting,				-- sorting
	l.price_delta,			-- price_delta
	l.user_ins,				-- created_by
	l.date_ins,				-- created_at
	l.user_upd,				-- updated_by
	l.date_upd,				-- updated_at
	0						-- object_version
FROM lovadina.item_variant l
LEFT JOIN company.item i ON l.item = i.external_code AND i.company_id = 40;

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
	l.id,			-- external_code
	40,				-- company_id
	l.item_type,	-- item_type
	i1.item_id,		-- item_id
	i2.item_id,		-- part_id
	l.quantity,		-- quantity
	l.user_ins,		-- created_by
	l.date_ins,		-- created_at
	l.user_upd,		-- updated_by
	l.date_upd,		-- updated_at
	0				-- object_version
FROM lovadina.item_part l
LEFT JOIN company.item i1 ON l.item = i1.external_code AND i1.company_id = 40
LEFT JOIN company.item i2 ON l.part = i2.external_code AND i2.company_id = 40;

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
	40,				-- company_id,
	description,	-- description
	user_ins,		-- created_by
	date_ins,		-- created_at
	user_upd,		-- updated_by
	date_upd,		-- updated_at
	0				-- object_version
FROM lovadina.price_list;

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
    l.id,				-- external_code
	40, 				-- company_id
	p.price_list_id,	-- price_list_id
	i.item_id,	 		-- item_id
    l.price,			-- price
    l.user_ins,			-- created_by
    l.date_ins,			-- created_at
    l.user_upd,			-- updated_by
    l.date_upd,			-- updated_at
    0 					-- object_version
FROM lovadina.price_list_detail l
LEFT JOIN company.price_list p ON l.id_price_list = p.external_code AND p.company_id = 40
LEFT JOIN company.item i ON l.item = i.external_code AND i.company_id = 40;

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
    l.id,				-- external_code
	40, 				-- company_id
	e.event_id,			-- event_id
	i.item_id,	 		-- item_id
    l.loaded,			-- loaded
    l.user_ins,			-- created_by
    l.date_ins,			-- created_at
    l.user_upd,			-- updated_by
    l.date_upd,			-- updated_at
    0 					-- object_version
FROM lovadina.stock_inventory l
LEFT JOIN company.event e ON l.event = e.external_code AND e.company_id = 40
LEFT JOIN company.item i ON l.item = i.external_code AND i.company_id = 40;

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
	l.id, 					-- external_code,
	40, 					-- company_id,
	e.event_id, 			-- event_id,
	l.date_time,			-- date_time
	l.order_number,			-- order_number
	l.order_date,			-- order_date
	l.order_time,			-- order_time
	l.stat_order_date,		-- stat_order_date
	l.stat_order_day_part,	-- stat_order_day_part
	l.cash_desk,			-- cash_desk
	l.delivery,				-- delivery
	l.table_num,			-- table_num
	l.customer_name,		-- customer_name
	l.covers,				-- covers
	l.total_amount,			-- total_amount
	l.discount,				-- discount
	l.cash,					-- cash
	l.change,				-- change
	--is_electronic_payment, -- is_electronic_payment
	l.status,				-- status
	l.fulfillment_date,	-- fulfillment_date
	l.user_ins,				-- created_by
	l.date_ins,				-- created_at
	l.user_upd,				-- updated_by
	l.date_upd,				-- updated_at
	0 						-- object_version
FROM lovadina.order_header l
LEFT JOIN company.event e ON l.event = e.external_code AND e.company_id=40;

DO $$ BEGIN RAISE NOTICE '% END Import order headers', clock_timestamp(); END; $$;


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
	l.id, 				-- external_code
	40,					-- company_id
	h.order_header_id, 	-- header_id
	i.item_id,			-- item_id
	l.variants,			-- variants
	l.quantity,			-- quantity
	l.price,			-- price
	l.amount,			-- amount
	l.user_ins,			-- created_by
	l.date_ins,			-- created_at
	l.user_upd,			-- updated_by
	l.date_upd,			-- updated_at 
	0 					-- object_version
FROM lovadina.order_detail l
LEFT JOIN company.order_header h ON l.id_header = h.external_code AND h.company_id = 40
LEFT JOIN company.item i ON l.item = i.external_code AND i.company_id = 40;

DO $$ BEGIN RAISE NOTICE '% END Import order lines', clock_timestamp(); END; $$;


--
-- Create an order_header_department record from order_line_department
--

DO $$ BEGIN RAISE NOTICE '% BEGIN Create order header department', clock_timestamp(); END; $$;

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
	Null, 					-- external_code
	40, 					-- company_id
	h.order_header_id,		-- header_id 
	d.department_id, 		-- department_id
	Null,					-- note
	Null,				 	-- other_departments
	coalesce(h.fulfillment_date, h.date_time), 	-- fulfillment_date
	h.created_by,			-- created_by
	h.created_at,			-- created_at
	h.updated_by,			-- updated_by
	h.updated_at,			-- updated_at
	0						-- object_version
FROM (
	SELECT DISTINCT
		id_header,
		department
	FROM lovadina.order_detail_department
	) x
LEFT JOIN company.order_header h ON x.id_header = h.external_code AND h.company_id = 40
LEFT JOIN company.department d ON x.department = d.external_code AND d.company_id = 40;

-- update from old order_header_department

WITH cte AS (
	SELECT 
		p.order_header_department_id,
		l.note,
		l.other_departments,
		l.fulfillment_date,
		l.id
	FROM company.order_header_department p
	JOIN company.order_header h ON p.order_header_id = h.order_header_id
	JOIN company.department d ON p.department_id = d.department_id
	JOIN lovadina.order_header_department l ON 
		(l.id_header = h.external_code AND h.company_id = 40)
		AND (l.department = d.external_code AND d.company_id = 40)
	)
UPDATE company.order_header_department i
SET note 				= cte.note,
	other_departments	= cte.other_departments,
	fulfillment_date	= coalesce(cte.fulfillment_date, i.fulfillment_date),
	external_code		= cte.id
FROM cte
WHERE i.order_header_department_id = cte.order_header_department_id;

DO $$ BEGIN RAISE NOTICE '% END Create order header department', clock_timestamp(); END; $$;


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
	l.id,				-- external_code
	40,					-- company_id
	x.order_header_department_id,	-- order_header_department_id
	e.event_id,			-- event_id
	l.event_date,		-- event_date
	l.day_part,			-- day_part
	i.item_id,			-- item_id
	l.variants,			-- variants
	l.quantity,			-- quantity
	l.user_ins,			-- created_by
	l.date_ins, 		-- created_at
	l.user_upd, 		-- updated_by
	l.date_upd, 		-- updated_at
	0 					-- object_version
FROM lovadina.order_detail_department l
LEFT JOIN company.order_header h ON l.id_header = h.external_code AND h.company_id = 40
LEFT JOIN company.event e ON l.event = e.external_code AND e.company_id = 40
LEFT JOIN company.department d ON l.department = d.external_code AND d.company_id = 40
LEFT JOIN company.order_header_department x ON h.order_header_id = x.order_header_id AND d.department_id = x.department_id
LEFT JOIN company.item i ON l.item = i.external_code AND i.company_id = 40;

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
		WHERE company_id = 40
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

