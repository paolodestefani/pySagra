set search_path to system;

-- system function: drop company 
CREATE or replace FUNCTION pa_company_drop(in_company int) 
RETURNS void AS
$$
DECLARE
i integer;
t text[];
BEGIN
	-- check if company is in use
	IF EXISTS(
                SELECT company_id 
                FROM system.connection 
                WHERE company_id = in_company) THEN
		RAISE EXCEPTION 'Can not drop company % because it is in use', in_company
        USING HINT = 'Disconnect users from this company', ERRCODE = 'PA013';
	END IF;
	-- delete some table first, shoul be faster
	DELETE FROM company.ordered_delivered WHERE company_id = in_company;
	DELETE FROM company.inventory WHERE company_id = in_company;
	-- disable triggers
	ALTER TABLE company.order_line_department DISABLE TRIGGER t10_order_line_to_inventory;
    ALTER TABLE company.order_line_department DISABLE TRIGGER t20_order_line_to_ordered_delivered;
	ALTER TABLE company.order_line_department DISABLE TRIGGER t99_update_company_user_date;
	ALTER TABLE company.order_line DISABLE TRIGGER t99_update_company_user_date;
	ALTER TABLE company.order_header_department DISABLE TRIGGER t10_update_order_header_department;
	ALTER TABLE company.order_header_department DISABLE TRIGGER t99_update_company_user_date;
	ALTER TABLE company.order_header DISABLE TRIGGER t10_update_numbering;
	ALTER TABLE company.order_header DISABLE TRIGGER t99_update_company_user_date;
	
    -- delete company record
	DELETE FROM system.company WHERE company_id = in_company;
	
    -- ri-enable triggers
	ALTER TABLE company.order_line_department ENABLE TRIGGER t10_order_line_to_inventory;
    ALTER TABLE company.order_line_department ENABLE TRIGGER t20_order_line_to_ordered_delivered;
	ALTER TABLE company.order_line_department ENABLE TRIGGER t99_update_company_user_date;
	ALTER TABLE company.order_line ENABLE TRIGGER t99_update_company_user_date;
	ALTER TABLE company.order_header_department ENABLE TRIGGER t10_update_order_header_department;
	ALTER TABLE company.order_header_department ENABLE TRIGGER t99_update_company_user_date;
	ALTER TABLE company.order_header ENABLE TRIGGER t10_update_numbering;
	ALTER TABLE company.order_header ENABLE TRIGGER t99_update_company_user_date;
	-- update identity
	FOREACH t SLICE 1 IN ARRAY ARRAY[
		['system.connection_history', 'history_id'],
		['company.cash_desk', 'cash_desk_id'],
		['company.department', 'department_id'],
		['company.event', 'event_id'],
		['company.item', 'item_id'],
		['company.item_part', 'item_part_id'],
		['company.item_variant', 'item_variant_id'],
		['company.numbering', 'numbering_id'],
		['company.order_header', 'order_header_id'],
		['company.order_header_department', 'order_header_department_id'],
		['company.order_line', 'order_line_id'],
		['company.order_line_department', 'order_line_department_id'],
		['company.price_list', 'price_list_id'],
		['company.price_list_item', 'price_list_item_id'],
		['company.printer_class', 'printer_class_id'],
		['company.printer_class_printer', 'printer_class_printer_id'],
		['company.seat_map', 'seat_map_id'],
		['company.inventory', 'inventory_id'],
		['company.ordered_delivered', 'ordered_delivered_id'],
		['company.web_order_header', 'web_order_header_id'],
		['company.web_order_line', 'web_order_line_id']
		] LOOP
		EXECUTE format('SELECT coalesce(max(%s), 0) + 1 FROM %s', t[2], t[1]) INTO i;
		EXECUTE format('ALTER TABLE %s ALTER COLUMN %s RESTART WITH %s', t[1], t[2], i) ;
		--RAISE NOTICE '%', t[2];
	END LOOP;
	-- reindex main tables
	REINDEX TABLE company.order_header;
	REINDEX TABLE company.order_header_department;
	REINDEX TABLE company.order_line;
	REINDEX TABLE company.order_line_department;
	REINDEX TABLE company.item;
	REINDEX TABLE company.item_part;
	REINDEX TABLE company.item_variant;
END;
$$
LANGUAGE plpgsql;
COMMENT ON FUNCTION pa_company_drop(int) IS 
    'Function for drop a company';
ALTER FUNCTION pa_company_drop(int) 
    OWNER TO pa_owner_role;
