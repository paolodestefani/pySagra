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

-- web_order_server table
CREATE TABLE web_order_server (
    created_at          timestamptz(3) NOT NULL,
	created_by          text NOT NULL,
    updated_at          timestamptz(3) NOT NULL,
	updated_by          text NOT NULL,
    object_version      integer NOT NULL,
    --
    company_id          integer NOT NULL,
    --
    server_address      text NOT NULL,
    port_number         integer NOT NULL DEFAULT 21,
    encoding_type       varchar(12) NOT NULL DEFAULT 'utf-8',
    user_name           varchar(256) NOT NULL,  -- encrypted
    user_password       varchar(256) NULL,      -- encrypted
    file_name           text NOT NULL,          -- encrypted
    --
    CONSTRAINT web_order_server_pk 
        PRIMARY KEY (company_id) 
        USING INDEX TABLESPACE {pyAppPgIndexesTS},
    CONSTRAINT web_order_server_company_fk 
        FOREIGN KEY (company_id)
        REFERENCES system.company (company_id) 
        MATCH SIMPLE ON UPDATE NO ACTION ON DELETE CASCADE

) TABLESPACE {pyAppPgTablesTS};
COMMENT ON TABLE web_order_server IS 
    'Web order server parameters';
ALTER TABLE web_order_server 
    OWNER TO {pyAppPgOwnerRole};

-- CREATE INDEX web_order_server_keys_idx ON web_order_server (company_id);

CREATE TRIGGER t99_update_company_user_date 
    BEFORE INSERT OR UPDATE ON web_order_server 
    FOR EACH ROW EXECUTE PROCEDURE system.update_company_user_date();
   