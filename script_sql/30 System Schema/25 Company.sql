--
-- **************************
-- ** APPLICATION DATABASE **
-- **************************
--

-- Paolo De Stefani 10.2018

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

-- This set of variables MUST be resolved before executing the scripts:
-- {pyAppPgOwnerRole} = PostgresSQL Role that own all db objects without login privilege
-- {pyAppPgDataBase} = Postgres database name
-- {pyAppPgLoginRole} = PostgresSQL Role used for standard login users
-- {pyAppPgLoginPassword} = Password for pyAppPgLoginRole
-- {pyAppName} = Python application name
-- {pyAppDescription} = Python application description
-- {pyAppVersion} = Application release version
-- {pyAppPgDataBaseTS} = Database table space (MUST be created before script execution)
-- {pyAppPgTablesTS} = Tables table space (MUST be created before script execution)
-- {pyAppPgIndexesTS} = Indexes table space (MUST be created before script execution)


---------------------------
-- SYSTEM SCHEMA OBJECTS --
---------------------------

SET search_path = system;


-- system table: companies
CREATE TABLE company (
    created_at              timestamptz(3) NOT NULL,
	created_by              text NOT NULL,
    updated_at              timestamptz(3) NOT NULL,
	updated_by              text NOT NULL,
    object_version          integer NOT NULL,
    --
    company_id              integer,
    description             text NOT NULL,
    company_image           bytea,
    is_system_object        boolean NOT NULL DEFAULT False,
    --
    CONSTRAINT company_pk 
        PRIMARY KEY (company_id) 
        USING INDEX TABLESPACE {pyAppPgIndexesTS}
)
TABLESPACE {pyAppPgTablesTS};
COMMENT ON TABLE company IS 
    '{pyAppName} companies table and companies'' settings';
ALTER TABLE company 
    OWNER TO {pyAppPgOwnerRole};

CREATE TRIGGER t99_update_company_user_date 
    BEFORE INSERT OR UPDATE ON company 
    FOR EACH ROW EXECUTE PROCEDURE update_company_user_date();


-- system function: create company 
CREATE FUNCTION system.pa_company_create( new_id int,
                                          new_description text,
                                          new_system_object boolean,
                                          new_company_image bytea)
RETURNS void AS
$$
BEGIN
	-- check if company id already exists
	IF EXISTS(
                SELECT company_id 
                FROM system.company 
                WHERE company_id = new_id) THEN
		RAISE EXCEPTION 'Company ID % already exists', new_id USING HINT = 'Try a different company ID', ERRCODE = 'PA012';
	END IF;
	-- create company reference on system.company
	INSERT INTO system.company (company_id, description, is_system_object, company_image) 
	VALUES (new_id, new_description, new_system_object, new_company_image);
    -- create company settings for th new company
	INSERT INTO company.setting (company_id) 
	VALUES (new_id);
END;
$$
LANGUAGE plpgsql;
COMMENT ON FUNCTION pa_company_create(int, text, boolean, bytea) IS 
    'Function for create a new company';
ALTER FUNCTION pa_company_create(int, text, boolean, bytea) 
    OWNER TO {pyAppPgOwnerRole};


-- system function: drop company 
CREATE FUNCTION pa_company_drop(in_company int) 
RETURNS void AS
$$
DECLARE
i integer;
s text;
t text;
n text;
tt text[];
BEGIN
	-- check if company is in use
	IF EXISTS(
                SELECT company_id 
                FROM system.connection 
                WHERE company_id = in_company) THEN
		RAISE EXCEPTION 'Can not drop company % because it is in use', in_company
        USING HINT = 'Disconnect users from this company', ERRCODE = 'PA013';
	END IF;

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

	-- *********************
	
    -- delete company record
	DELETE FROM system.company WHERE company_id = in_company;
	
	-- *********************
	
	-- re-enable trigger
	-- can't use ENABLE TRIGGER ALL because is available only for superuser
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

	-- update identity
	FOREACH tt SLICE 1 IN ARRAY ARRAY[
		['system.connection_history', 'history_id'],
		['company.cash_desk', 'cash_desk_id'],
		['company.department', 'department_id'],
		['company.event', 'event_id'],
		['company.inventory', 'inventory_id'],
        ['company.item', 'item_id'],
		['company.item_part', 'item_part_id'],
		['company.item_variant', 'item_variant_id'],
		['company.numbering', 'numbering_id'],
		['company.order_header', 'order_header_id'],
		['company.order_header_department', 'order_header_department_id'],
		['company.order_line', 'order_line_id'],
		['company.order_line_department', 'order_line_department_id'],
        ['company.ordered_delivered', 'ordered_delivered_id'],
		['company.price_list', 'price_list_id'],
		['company.price_list_item', 'price_list_item_id'],
		['company.printer_class', 'printer_class_id'],
		['company.printer_class_printer', 'printer_class_printer_id'],
		['company.seat_map', 'seat_map_id']
		] LOOP
		EXECUTE format('SELECT coalesce(max(%s), 0) + 1 FROM %s', tt[2], tt[1]) INTO i;
		EXECUTE format('ALTER TABLE %s ALTER COLUMN %s RESTART WITH %s', tt[1], tt[2], i) ;
		--RAISE NOTICE '%', t[2];
	END LOOP;
    
END;
$$
LANGUAGE plpgsql;
COMMENT ON FUNCTION pa_company_drop(int) IS 
    'Function for drop a company';
ALTER FUNCTION pa_company_drop(int) 
    OWNER TO {pyAppPgOwnerRole};

