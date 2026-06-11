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


-- system table: profile
CREATE TABLE profile (
    created_at              timestamptz(3) NOT NULL,
	created_by              text NOT NULL,
    updated_at              timestamptz(3) NOT NULL,
	updated_by              text NOT NULL,
    object_version          integer NOT NULL,
    --
    profile_code            varchar(48),
    description             text NOT NULL,
    is_system_object        boolean NOT NULL DEFAULT False,
    --
    CONSTRAINT profile_pk 
        PRIMARY KEY (profile_code) 
        USING INDEX TABLESPACE {pyAppPgIndexesTS}
)
TABLESPACE {pyAppPgTablesTS};
COMMENT ON TABLE profile IS 
    '{pyAppName} profiles table';
ALTER TABLE profile 
    OWNER TO {pyAppPgOwnerRole};

CREATE TRIGGER t99_update_company_user_date 
    BEFORE INSERT OR UPDATE ON profile 
    FOR EACH ROW EXECUTE PROCEDURE update_company_user_date();


-- system table: actions for profiles
CREATE TABLE profile_action (
    created_at              timestamptz(3) NOT NULL,
	created_by              text NOT NULL,
    updated_at              timestamptz(3) NOT NULL,
	updated_by              text NOT NULL,
    object_version          integer NOT NULL,
    --
    profile_code            varchar(48),
    action                  varchar(48),
    read                    boolean NOT NULL DEFAULT True,
    write                   boolean NOT NULL DEFAULT True,
    execute                 boolean NOT NULL DEFAULT True,
    --
    CONSTRAINT profile_action_pk 
        PRIMARY KEY (profile_code, action) 
        USING INDEX TABLESPACE {pyAppPgIndexesTS},
    CONSTRAINT profile_action_profile_fk 
        FOREIGN KEY (profile_code) 
        REFERENCES profile (profile_code)
        MATCH SIMPLE ON UPDATE NO ACTION ON DELETE CASCADE
)
TABLESPACE {pyAppPgTablesTS};
COMMENT ON TABLE profile_action IS 
    'Actions for each profile and authorization setting';
ALTER TABLE profile_action 
    OWNER TO {pyAppPgOwnerRole};

CREATE TRIGGER t99_update_company_user_date 
    BEFORE INSERT OR UPDATE ON profile_action 
    FOR EACH ROW EXECUTE PROCEDURE update_company_user_date();


-- system table: menu and toolbar definitions
CREATE TABLE menu_toolbar(
    created_at              timestamptz(3) NOT NULL,
	created_by              text NOT NULL,
    updated_at              timestamptz(3) NOT NULL,
	updated_by              text NOT NULL,
    object_version          integer NOT NULL,
    --
    type                    char(1) NOT NULL, -- (M)enu or (T)oolbar
    code                    varchar(48),
    description             text,
    is_system_object        boolean NOT NULL DEFAULT False,
    --
    CONSTRAINT menu_toolbar_pk 
        PRIMARY KEY (code) 
        USING INDEX TABLESPACE {pyAppPgIndexesTS},
    CONSTRAINT menu_toolbar_type_check 
        CHECK (type IN ('M', 'T'))  -- (M)enu, (T)oolbar
)
TABLESPACE {pyAppPgTablesTS};
COMMENT ON TABLE menu_toolbar IS 
    'Menu and toolbar class definition';
ALTER TABLE menu_toolbar 
    OWNER TO {pyAppPgOwnerRole};

CREATE TRIGGER t99_update_company_user_date 
    BEFORE INSERT OR UPDATE ON menu_toolbar 
    FOR EACH ROW EXECUTE PROCEDURE update_company_user_date();


-- system table: menu toolbar item
CREATE TABLE menu_toolbar_item(
    created_at              timestamptz(3) NOT NULL,
	created_by              text NOT NULL,
    updated_at              timestamptz(3) NOT NULL,
	updated_by              text NOT NULL,
    object_version          integer NOT NULL,
    --
    parent                  varchar(48),
    child                   varchar(48),
    description             text,
    sorting                 integer NOT NULL,
    item_type               char(1) NOT NULL,   -- (A)ction, (M)enu, (S)eparator for menu 
                                                -- (T)oolbar, (A)ction, (S)eparator,  (W)idget for toolbar
    action                  varchar(48),
    --
    CONSTRAINT menu_item_pk 
        PRIMARY KEY (parent, child) 
        USING INDEX TABLESPACE {pyAppPgIndexesTS},
    CONSTRAINT menu_item_item_type_check 
        CHECK (item_type IN ('A', 'M', 'S', 'T', 'W')) -- Action, Menu, Separator, Toolbar, Widget
)
TABLESPACE {pyAppPgTablesTS};
COMMENT ON TABLE menu_toolbar_item IS 
    'Menu and toolbar structure';
ALTER TABLE menu_toolbar_item 
    OWNER TO {pyAppPgOwnerRole};

CREATE TRIGGER t99_update_company_user_date 
    BEFORE INSERT OR UPDATE ON menu_toolbar_item 
    FOR EACH ROW EXECUTE PROCEDURE update_company_user_date();
