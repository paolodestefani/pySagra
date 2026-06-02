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


---------------------------
-- SYSTEM SCHEMA OBJECTS --
---------------------------

SET search_path = system;


-- system table: application base settings table

-- settings are strored in text fields
-- application must convert to the proper data type
-- txt -> int
-- txt -> number (english notation)
-- txt -> bolean ('true' or 'false')
-- txt -> date (universal date format: YYYYMMDD)
-- etc.

CREATE TABLE setting (
    setting                 varchar(48),
    setting_value           text,
    description             text,
    --
    CONSTRAINT setting_pk 
        PRIMARY KEY (setting) 
        USING INDEX TABLESPACE {pyAppPgIndexesTS}
)
TABLESPACE {pyAppPgTablesTS};
COMMENT ON TABLE setting IS 
    '{pyAppName} system settings table, whole application system parameters';
ALTER TABLE setting 
    OWNER TO {pyAppPgOwnerRole};


-- system function: create param value
CREATE FUNCTION pa_setting_create(in_setting varchar, in_value text, in_description text)
RETURNS void AS
$$
BEGIN
    IF EXISTS(  
        SELECT setting 
        FROM system.setting 
        WHERE setting = in_setting
        ) THEN
        RAISE EXCEPTION 'Cannot create ''%s'' setting because it already exists ', in_name;
    END IF;
    INSERT INTO system.setting (
        setting,
        setting_value, 
        description
        ) 
    VALUES (
        in_setting,
        in_value, 
        in_description
        );
END;
$$
LANGUAGE plpgsql;
COMMENT ON FUNCTION pa_setting_create(varchar, text, text) IS
    'Function for create a system setting parameter';
ALTER FUNCTION pa_setting_create(varchar, text, text) 
    OWNER TO {pyAppPgOwnerRole};


-- system function: set param value
CREATE FUNCTION pa_setting_set(in_setting text, in_value text)
RETURNS void AS
$$
BEGIN
    IF NOT EXISTS(  
        SELECT setting 
        FROM system.setting 
        WHERE setting = in_setting
        ) THEN
        RAISE EXCEPTION 'Unknown setting parameter ''%''', in_setting;
    END IF;
    UPDATE system.setting 
    SET setting_value = in_value 
    WHERE setting = in_setting;
END;
$$
LANGUAGE plpgsql;
COMMENT ON FUNCTION pa_setting_set(text, text) IS
    'Function for set a system setting value';
ALTER FUNCTION pa_setting_set(text, text) 
    OWNER TO {pyAppPgOwnerRole};


-- system function: get param value
CREATE FUNCTION pa_setting(in_setting text)
RETURNS text AS
$$
DECLARE
    out_value text;
BEGIN
    IF NOT EXISTS(  
        SELECT setting 
        FROM system.setting 
        WHERE setting = in_setting
        ) THEN
        RAISE EXCEPTION 'Unknown setting parameter ''%''', in_setting;
    END IF;
    SELECT setting_value INTO out_value 
    FROM system.setting 
    WHERE setting = in_setting;
    RETURN out_value;
END;
$$
LANGUAGE plpgsql;
COMMENT ON FUNCTION pa_setting(text) IS
    'Function for get a system setting value';
ALTER FUNCTION pa_setting(text) 
    OWNER TO {pyAppPgOwnerRole};


-- system wide settings, each parameter's value is set in application_data script
SELECT
pa_setting_create('app_name', Null, 'Application name'),
pa_setting_create('app_description', Null, 'Application description'),
pa_setting_create('app_pg_table_ts', '{pyAppPgTablesTS}', 'PostgreSQL table table space - setted on database creation'),
pa_setting_create('app_pg_index_ts', '{pyAppPgIndexesTS}', 'PostgreSQL index table space - setted on database creation'),
pa_setting_create('app_pg_owner_role', '{pyAppPgOwnerRole}', 'PostgreSQL role that own all db object without login privilege - setted on database creation'),
pa_setting_create('app_system_user', Null, 'Application System Administrator'),
pa_setting_create('default_system_profile', Null, 'New company default profile assigned to company creator and profile for system user'),
pa_setting_create('default_system_menu', Null, 'New company default menu assigned to company creator and menu for system user'),
pa_setting_create('password_expire_days', Null, 'Number of days before password expires'),
pa_setting_create('strong_password_required', Null, 'If True a strong password is require'),
pa_setting_create('clear_connection_history', Null, 'If not null delete connection history records older then the stated number of days')

