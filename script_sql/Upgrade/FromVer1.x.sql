--
-- Execute in the new database
-- Command for restore of version 1.x data
-- Data are restored in the "public" schema of the new database "progress" so "public" schema MUST EXISTS
--
-- psql -U postgres -d progress < c:\PyWare\pySagra\2.0\script\Upgrade\Lovadina.sql
--
-- 1 Create users (in script)
-- 2 Create a specific company (in script)
-- 3 Modify the search path ***
-- 4 Import one table at a time ***
--

--
-- create users
--
DELETE FROM system.app_user WHERE code not in ('system', 'utente', 'pySagraWeb');
INSERT INTO system.app_user (code, description, user_password, is_admin, system, l10n)
SELECT user_name, user_description, system.crypt(user_name, system.gen_salt('bf')), False, False, 'it_IT'
FROM public.sys_users;

--
-- create company
--
DROP SCHEMA IF EXISTS lovadina CASCADE;
DELETE FROM system.company WHERE id = 30;
SELECT system.pa_company_create(30, ps.company_name, 'lovadina', 'lovadina', false, Null)
FROM public.settings ps;

--
-- grant new company to all users with default profile/menu/toolbar
--
INSERT INTO system.app_user_company (app_user, company, profile, menu, toolbar)
SELECT code, 30, 'default', 'default_it', 'default_it'
FROM system.app_user
ON CONFLICT DO NOTHING;
-- set profile/menu/toolbar for system user
UPDATE system.app_user_company SET profile = 'full', menu = 'full_en', toolbar = 'full_en'
WHERE app_user = 'system';

--
-- set search path to new schema
--
SET search_path = 'lovadina';


--
-- clean company data first
--
ALTER TABLE event DISABLE TRIGGER update_user_date;
DELETE FROM event; -- delete all orders as well
ALTER TABLE item_part DISABLE TRIGGER update_user_date;
DELETE FROM item_part;
ALTER TABLE item_variant DISABLE TRIGGER update_user_date;
DELETE FROM item_variant;
ALTER TABLE item DISABLE TRIGGER update_user_date;
DELETE FROM item;
ALTER TABLE price_list_detail DISABLE TRIGGER update_user_date;
DELETE FROM price_list_detail;
ALTER TABLE department DISABLE TRIGGER update_user_date;
DELETE FROM department;
ALTER TABLE printer_class DISABLE TRIGGER update_user_date;
DELETE FROM printer_class;
ALTER TABLE numbered_table DISABLE TRIGGER update_user_date;
DELETE FROM numbered_table; 
ALTER TABLE order_header DISABLE TRIGGER update_user_date;
DELETE FROM order_header;
ALTER TABLE order_header_department DISABLE TRIGGER update_user_date;
ALTER TABLE order_detail DISABLE TRIGGER update_user_date;
ALTER TABLE order_detail_department DISABLE TRIGGER update_user_date;

--
-- copy events
--
INSERT INTO event (id, description, date_start, date_end, image,
				   user_ins, date_ins, user_upd, date_upd, row_timestamp)
SELECT id,
	description,
	date_start,
	date_end + interval '23h59m',
	decode(base64image, 'base64'),
	user_ins, 
	date_ins, 
	user_upd,
	date_upd,
	clock_timestamp() at time zone 'UTC'
FROM public.events;
ALTER TABLE event ENABLE TRIGGER update_user_date;

--
-- copy printer classes
--
INSERT INTO printer_class (id, description, user_ins, date_ins, user_upd, date_upd, row_timestamp)
SELECT class_id,
	class_description,
	user_ins,
	date_ins,
	user_upd,
	date_upd,
	clock_timestamp() at time zone 'UTC'
FROM public.printers_classes;
ALTER TABLE printer_class ENABLE TRIGGER update_user_date;

--
-- copy settings
--
UPDATE setting
SET lunch_start_time = extract(hour from b.order_lunch_time_start),
	dinner_start_time = extract(hour from b.order_dinner_time_start),
	warning_stock_level = b.stock_yellow_level,
	critical_stock_level = b.stock_red_level,
	default_delivery_type = b.default_delivery_type,
	order_list_tab_position = b.order_list_tab_position,
	order_list_rows = b.order_list_rows,
	order_list_columns = b.order_list_columns,
	max_covers = b.max_covers,
	automatic_show_variants = b.autovariants,
	always_show_stock_inventory = b.always_show_level,
	mandatory_table_number = b.table_number,
	use_table_list = b.use_tables_list,
	table_list_rows = b.tables_list_rows,
	table_list_columns = b.tables_list_columns,
	check_inactivity = b.check_inactivity,
	inactivity_time = b.inactivity_time
FROM setting a
JOIN public.settings b ON a.id = true AND b.id = 1;

--
-- copy departments
--
INSERT INTO department (id, description, sorting, printer_class, is_obsolete, is_not_managed, is_for_takeaway,
					   user_ins, date_ins, user_upd, date_upd, row_timestamp)
SELECT id, 
	description,
	sorting_index,
	printer,
	not is_active,
	is_menu,
	for_takeaway,
	user_ins, 
	date_ins, 
	user_upd, 
	date_upd,
	clock_timestamp() at time zone 'UTC'
FROM public.departments;
ALTER TABLE department ENABLE TRIGGER update_user_date;
-- add a temporary department used for items that not have a department
INSERT INTO department (id, description) VALUES (10, 'TO BE DELETED'); 

--
-- copy tables
--
INSERT INTO numbered_table (table_code, pos_row, pos_column, text_color, background_color, is_obsolete,
						user_ins, date_ins, user_upd, date_upd, row_timestamp)
SELECT "table",
	pos_row,
	pos_column,
	text_color, 
	bg_color,
	not is_active,
	user_ins,
	date_ins,
	user_upd,
	date_upd, 
	clock_timestamp() at time zone 'UTC'
FROM public.tables;
ALTER TABLE numbered_table ENABLE TRIGGER update_user_date;

--
-- copy items
--
INSERT INTO item (id, item_type, description, customer_description, department, sorting, pos_row, pos_column,
				 has_stock_control, has_variants, is_salable, is_obsolete,
				 user_ins, date_ins, user_upd, date_upd, row_timestamp)
SELECT id,
	CASE item_type WHEN 'A' THEN 'I' ELSE item_type END,
	description,
	description,
	coalesce(department, 10),
	sorting_index,
	pos_row,
	pos_column,
	level_check,
	has_variants,
	CASE WHEN is_obsolete IS true THEN false ELSE true END,
	is_obsolete,
	user_ins, 
	date_ins, 
	user_upd, 
	date_upd,
	clock_timestamp() at time zone 'UTC'
FROM public.items;
ALTER TABLE item ENABLE TRIGGER update_user_date;
-- set unload_control items
UPDATE item
SET has_unload_control = true
WHERE id IN (SELECT item FROM public.check_reports_items);
-- web items all non obsolete
UPDATE item 
SET is_web_available = true, web_sorting = sorting
WHERE is_obsolete IS false;

--
-- copy variants
--
INSERT INTO item_variant (id, item, variant_description, sorting, price_delta,
						 user_ins, date_ins, user_upd, date_upd, row_timestamp)
SELECT id,
	item,
	variant_description,
	sorting_index,
	price_delta,
	user_ins, 
	date_ins, 
	user_upd, 
	date_upd,
	clock_timestamp() at time zone 'UTC'
FROM public.items_variants;
ALTER TABLE item_variant ENABLE TRIGGER update_user_date;

--
-- copy kit parts
--
INSERT INTO item_part (item_type, item, part, quantity,
					   user_ins, date_ins, user_upd, date_upd, row_timestamp)
SELECT 'K',
	item,
	item_child,
	quantity,
	user_ins,
	date_ins, 
	user_upd,
	date_upd,
	clock_timestamp() at time zone 'UTC'
FROM public.items_compound
ORDER BY item, item_child;
-- update kit part flag on item for part item
UPDATE item
SET is_kit_part = true
WHERE id IN (SELECT DISTINCT part FROM item_part WHERE item_type = 'K');

--
-- copy menu parts
--
INSERT INTO item_part (item_type, item, part, quantity,
					   user_ins, date_ins, user_upd, date_upd, row_timestamp)
SELECT 'M',
	item,
	item_child, 
	quantity,
	user_ins,
	date_ins, 
	user_upd, 
	date_upd, 
	clock_timestamp() at time zone 'UTC'
FROM public.items_menu
ORDER BY item, item_child;
-- update menu part flag on item for part item
UPDATE item
SET is_menu_part = true
WHERE id IN (SELECT DISTINCT part FROM item_part WHERE item_type = 'M');

ALTER TABLE item_part ENABLE TRIGGER update_user_date;

--
-- create a price list
--
INSERT INTO price_list (id, description) VALUES (1, 'LISTINO');

INSERT INTO price_list_detail (id_price_list, item, price, user_ins, date_ins, user_upd, date_upd, row_timestamp)
SELECT 1,
    id,
    price,
    user_ins,
    date_ins,
    user_upd,
    date_upd,
    clock_timestamp() at time zone 'UTC'
FROM public.items
WHERE is_obsolete IS false;

ALTER TABLE price_list_detail ENABLE TRIGGER update_user_date;

-- 
-- copy order header
--
INSERT INTO order_header (id, event, date_time, order_number, order_date, order_time, stat_order_date, stat_order_day_part,
						 cash_desk, delivery, table_num, customer_name, covers, total_amount, discount, cash, change, 
                         status, fulfillment_date,
						 user_ins, date_ins, user_upd, date_upd, row_timestamp)
SELECT id,
	event,
	date_time,
	order_number,
	order_date,
	order_time::time(0),
	stat_order_date,
	stat_order_day_part,
    '---',
	delivery, 
	table_num, 
	customer_name, 
	covers, 
	total_amount,
	discount, 
	cash, 
	change,
    'P',
    date_time,
	user_ins,
	date_ins, 
	user_upd, 
	date_upd, 
	clock_timestamp() at time zone 'UTC'
FROM public.order_headers;
ALTER TABLE order_header ENABLE TRIGGER update_user_date;

--
-- copy order header department
--
INSERT INTO order_header_department (id, id_header, department, note, other_departments, fulfillment_date,
									 user_ins, date_ins, user_upd, date_upd, row_timestamp)
SELECT ohd.id,
	ohd.id_header,
	ohd.department,
	ohd.note,
	ohd.other_departments,
    oh.date_time,
	oh.user_ins,
	oh.date_ins, 
	oh.user_upd, 
	oh.date_upd, 
	clock_timestamp() at time zone 'UTC'
FROM public.order_headers_deps ohd
JOIN public.order_headers oh ON ohd.id_header = oh.id;
ALTER TABLE order_header_department ENABLE TRIGGER update_user_date;

--
-- copy order detail
--
INSERT INTO order_detail (id, id_header, item, variants, quantity, price, amount,
						 user_ins, date_ins, user_upd, date_upd, row_timestamp)
SELECT od.id,
	od.id_header,
	od.item,
	od.variants,
	od.quantity,
	od.price,
	od.amount,
	oh.user_ins,
	oh.date_ins, 
	oh.user_upd, 
	oh.date_upd, 
	clock_timestamp() at time zone 'UTC'
FROM public.order_details od
JOIN public.order_headers oh ON od.id_header = oh.id;
ALTER TABLE order_detail ENABLE TRIGGER update_user_date;

--
-- copy order detail department
--
INSERT INTO order_detail_department (id, id_header, event, event_date, day_part, department, item, variants, quantity,
									user_ins, date_ins, user_upd, date_upd, row_timestamp)
SELECT odd.id,
	odd.id_header,
	odd.event,
	oh.stat_order_date,
	oh.stat_order_day_part,
	odd.department,
	odd.item,
	odd.variants,
	odd.quantity,
	oh.user_ins,
	oh.date_ins, 
	oh.user_upd, 
	oh.date_upd, 
	clock_timestamp() at time zone 'UTC'
FROM public.order_details_deps odd
JOIN public.order_headers oh ON odd.id_header = oh.id;
ALTER TABLE order_detail_department ENABLE TRIGGER update_user_date;

-- stock_inventory will be rebuild

--
-- update identity on current max value on all tables
--
DO $$
DECLARE
i int;
t text;
BEGIN
FOREACH t IN ARRAY ARRAY['event',
						 'printer_class',
						 'department',
						 'item',
						 'item_variant',
						 'item_part',
						 'price_list',
						 'order_header',
						 'order_header_department',
						 'order_detail',
						 'order_detail_department',
						 'stock_inventory'] LOOP
	EXECUTE format('SELECT coalesce(max(id), 0) + 1 FROM %s', t) INTO i;
	EXECUTE format('ALTER TABLE %s ALTER COLUMN id RESTART WITH %s', t, i) ;
END LOOP;
END;
$$
language plpgsql;

--
-- update unloads and numbering
--
DO $$
DECLARE
i int;
BEGIN
FOR i IN SELECT id FROM event ORDER BY date_end
	LOOP
		PERFORM common.numbering_rebuild(i);
		PERFORM common.unload_rebuild(i);
	END LOOP;
END;
$$
language plpgsql;


