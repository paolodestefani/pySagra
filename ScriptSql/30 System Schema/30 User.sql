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


-- system table: user
CREATE TABLE app_user (
    created_at              timestamptz(3) NOT NULL,
	created_by              text NOT NULL,
    updated_at              timestamptz(3) NOT NULL,
	updated_by              text NOT NULL,
    object_version          integer NOT NULL,
    --
    user_code               varchar(48),
    description             text NOT NULL,
    user_image              bytea,
    user_password           varchar(256) NOT NULL,
    password_date           timestamptz(3) DEFAULT clock_timestamp(), 
	new_password_required   boolean NOT NULL DEFAULT False,
    is_admin                boolean NOT NULL DEFAULT False,
    is_system_object        boolean NOT NULL DEFAULT False,
	can_edit_views          boolean NOT NULL DEFAULT false,
	can_edit_sortfilters    boolean NOT NULL DEFAULT false,
	can_edit_reports        boolean NOT NULL DEFAULT false,
    l10n                    char(5) NOT NULL,
    last_company            integer NULL,
    last_company_desc       text NULL, -- used for user table information, include code and description
    last_login              timestamptz(3) NULL,
    -- appearence
    style_theme             varchar(48) NULL,
    color_scheme            char(1) NULL,
    icon_theme              varchar(48) NULL,
    font_family             varchar(60) NULL,
    font_size               integer NULL,
    tool_button_style       char(1) NULL,
	tab_position            char(1) NULL,
    --
    CONSTRAINT app_user_pk 
        PRIMARY KEY (user_code) 
        USING INDEX TABLESPACE {pyAppPgIndexesTS}
)
TABLESPACE {pyAppPgTablesTS};
COMMENT ON TABLE app_user IS 
    '{pyAppName} user table';
ALTER TABLE app_user 
    OWNER TO {pyAppPgOwnerRole};

CREATE TRIGGER t99_update_company_user_date 
    BEFORE INSERT OR UPDATE ON app_user 
    FOR EACH ROW EXECUTE PROCEDURE update_company_user_date();


-- system table: app_user_company
CREATE TABLE app_user_company (
    created_at              timestamptz(3) NOT NULL,
	created_by              text NOT NULL,
    updated_at              timestamptz(3) NOT NULL,
	updated_by              text NOT NULL,
    object_version          integer NOT NULL,
    --
    app_user_code           varchar(48),
    company_id              integer,
    profile_code            varchar(48) NOT NULL,
    menu_code               varchar(48) NOT NULL, -- *** lack of a check constraint for menu existence (subquery check not available in pgsql)
    toolbar_code            varchar(48) NOT NULL, -- *** lack of a check constraint for toolbar existence (subquery check not available in pgsql)
    --
    CONSTRAINT app_user_company_pk 
        PRIMARY KEY (app_user_code, company_id) 
        USING INDEX TABLESPACE {pyAppPgIndexesTS},
    CONSTRAINT app_user_company_user_fk 
        FOREIGN KEY (app_user_code) 
        REFERENCES app_user (user_code)
        MATCH SIMPLE ON UPDATE NO ACTION ON DELETE CASCADE,
    CONSTRAINT app_user_company_company_fk 
        FOREIGN KEY (company_id) 
        REFERENCES company (company_id)
        MATCH SIMPLE ON UPDATE NO ACTION ON DELETE CASCADE,
    CONSTRAINT app_user_company_profile_fk 
        FOREIGN KEY (profile_code) 
        REFERENCES profile (profile_code)
        MATCH SIMPLE ON UPDATE NO ACTION ON DELETE CASCADE,
    CONSTRAINT app_user_company_menu_fk
        FOREIGN KEY (menu_code) 
        REFERENCES menu_toolbar (code)
        MATCH SIMPLE ON UPDATE NO ACTION ON DELETE CASCADE,
    CONSTRAINT app_user_company_toolbar_fk 
        FOREIGN KEY (toolbar_code) 
        REFERENCES menu_toolbar (code)
        MATCH SIMPLE ON UPDATE NO ACTION ON DELETE CASCADE
)
TABLESPACE {pyAppPgTablesTS};
COMMENT ON TABLE app_user_company IS 
    '{pyAppName} user''s profile/menu/toolbar for each company';
ALTER TABLE app_user_company 
    OWNER TO {pyAppPgOwnerRole};

CREATE TRIGGER t99_update_company_user_date 
    BEFORE INSERT OR UPDATE ON app_user_company 
    FOR EACH ROW EXECUTE PROCEDURE update_company_user_date();


-- system function: change user password
CREATE FUNCTION pa_password_change(in_user text, in_password text) 
RETURNS void AS
$$
BEGIN
    -- update password
    UPDATE system.app_user
    SET user_password = system.crypt(in_password, system.gen_salt('bf')), password_date = clock_timestamp(), new_password_required = false
    WHERE user_code = in_user; 
END;
$$ 
LANGUAGE plpgsql;
COMMENT ON FUNCTION pa_password_change(text, text) IS 
    'Function that changes an user password';
ALTER FUNCTION pa_password_change(text, text) 
    OWNER TO {pyAppPgOwnerRole};
