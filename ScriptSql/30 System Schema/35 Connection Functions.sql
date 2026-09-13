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


-- Error codes:
-- PA001 Wrong PGSQL Server version
-- PA002 Wrong application database
-- PA003 Wrong application database version
-- PA004 --
-- PA005 A password is required
-- PA006 Authentication failed (wrong user or password)
-- PA007 Unknown company
-- PA008 No access rights to required company
-- PA009 Can not kill current connection


-- system function: create an application connection, returns session parameters
CREATE FUNCTION pa_connect(
    in_pg_version              numeric,
	in_app_name                text,
	in_version_major           integer,
	in_version_minor           integer,
	in_user_code               text,
	in_user_pwd                text,
	in_client_name             text
    )
RETURNS TABLE (	session_id              integer,
				app_user_code           varchar,
                user_description        text,
                is_admin                boolean,
                can_edit_views          boolean,
                can_edit_sortfilters    boolean,
				can_edit_reports        boolean,
                l10n                    character,
                style_theme             varchar,
                color_scheme            character,
                icon_theme              varchar,
                font_family             varchar,
                font_size               integer,
                tool_button_style       character,
                tab_position            character,
                current_company         integer,    -- user's last company is the current company
                new_password_required   boolean,
                app_system_user         text
                ) AS 
$$
DECLARE
	app_db_major            int;
    app_db_minor            int;
    app_user_profile        text;
    app_company             int;
    new_pwd_required        boolean;
    is_password_correct     boolean;
    last_login_date         timestamptz;
BEGIN
	-- initialize this flag to False
	new_pwd_required := false;

	--
	-- check if a connection is possible
	--

	-- check postgres version
	IF current_setting('server_version_num')::int < in_pg_version THEN
        RAISE EXCEPTION 'Wrong PostgreSQL server version: required % detected %', in_pg_version, current_setting('server_version_num')::int
        USING HINT = 'You need to use a different database server version', ERRCODE = 'PA001';
    END IF;

	-- check application database
	IF system.pa_setting('app_name') != in_app_name THEN
		RAISE EXCEPTION 'Wrong application database: required ''%'' detected ''%''', in_app_name, system.pa_setting('app_name') 
		USING HINT = 'You need to use a different database', ERRCODE = 'PA002';
	END IF;

	-- check application db version
    -- no need to check for schema definition as the first sql command is system.pa_connect() which raise an error if schema 'system' or function 'pa_connect' does not exists
    SELECT major, minor INTO app_db_major, app_db_minor 
    FROM system.version 
    ORDER BY installed_at DESC LIMIT 1;
    IF app_db_major != in_version_major OR app_db_minor != in_version_minor THEN
        RAISE EXCEPTION 'Wrong application database version: required %.% detected %.%', in_version_major, in_version_minor, app_db_major, app_db_minor
        USING HINT = 'You need to use a different application database version', ERRCODE = 'PA003';
    END IF;

	-- check application user
    IF NOT EXISTS(
        SELECT user_code 
        FROM system.app_user 
        WHERE user_code = in_user_code
        ) THEN
        RAISE EXCEPTION 'Authentication failed (wrong user or password)' 
        USING HINT = 'Check user name and password', ERRCODE = 'PA004';
    END IF;

	-- check application user password
    -- coalesce is for manage null password
    IF (
        SELECT coalesce(user_password = system.crypt(in_user_pwd, user_password), false) 
        FROM system.app_user 
        WHERE user_code = in_user_code
        ) IS NOT true THEN
        RAISE EXCEPTION 'Authentication failed (wrong user or password)' 
        USING HINT = 'Check user name and password', ERRCODE = 'PA006';
    END IF;

	-- if a new password is reqired set new_pwd_required variable at True
    SELECT u.new_password_required INTO new_pwd_required 
    FROM system.app_user u
    WHERE u.user_code = in_user_code;

	-- if password is expired set new_password_required variable at True
    IF (
        SELECT (now()::date - coalesce(password_date, 'epoch')::date) >= system.pa_setting('password_expire_days')::int 
        FROM system.app_user 
        WHERE user_code = in_user_code
        ) THEN
        new_pwd_required = true;
    END IF;

	-- clean up connection table from orphan records
    -- delete any record in system.connection that not mach an active pid
    DELETE FROM system.connection sc
    WHERE sc.session_id NOT IN (
        SELECT pid 
        FROM pg_catalog.pg_stat_activity 
        WHERE application_name = system.pa_setting('app_name')
        );

	--
	-- Ok, start a connection
	--

	-- set application name
    PERFORM set_config('application_name', system.pa_setting('app_name'), false);
    -- log access
    INSERT INTO system.connection (app_user_code, client_name) 
    VALUES (in_user_code, in_client_name)
    RETURNING access_date INTO last_login_date;
    -- update user's last login date
    UPDATE system.app_user 
    SET last_login = last_login_date 
    WHERE user_code = system.pa_current_user();

    -- set search_path
    PERFORM set_config('search_path', 'common, company', false);

    -- return user session parameters (not connected to a company yet)
    RETURN QUERY
        SELECT 
            pg_backend_pid(),
            c.app_user_code,
            u.description,
            u.is_admin,
            u.can_edit_views,
            u.can_edit_sortfilters,
            u.can_edit_reports,
            u.l10n,
            u.style_theme,
            u.color_scheme,
            u.icon_theme,
            u.font_family,
            u.font_size,
            u.tool_button_style,
            u.tab_position,
            u.last_company,
            u.new_password_required,
            system.pa_setting('app_system_user')
        FROM system.connection c
        JOIN system.app_user u ON c.app_user_code = u.user_code
        WHERE c.session_id = pg_backend_pid();
END;
$$
LANGUAGE plpgsql;
COMMENT ON FUNCTION pa_connect(numeric, text, integer, integer, text, text, text) IS
    'Function for open an application connection';
ALTER FUNCTION pa_connect(numeric, text, integer, integer, text, text, text) 
    OWNER TO {pyAppPgOwnerRole};

  
-- system function: close application connection
CREATE FUNCTION pa_disconnect()
RETURNS void AS
$$
DECLARE
	cur_user varchar(40);
	cur_company int;
BEGIN
	DELETE FROM system.connection 
    WHERE session_id = pg_backend_pid();
END;
$$
LANGUAGE plpgsql;
COMMENT ON FUNCTION pa_disconnect() IS
    'Function for close the currrent application connection';
ALTER FUNCTION pa_disconnect() 
    OWNER TO {pyAppPgOwnerRole};


-- system function: change company in the current database connection
CREATE FUNCTION pa_company_change(in_new_company int)
RETURNS TABLE (
    current_company     int,
	company_description text,
	company_image       bytea,
	profile             varchar,
	menu                varchar,
	toolbar             varchar
  ) AS
$$
DECLARE
	c_app_user          text;
	c_app_client_name   text;
	c_app_company       int;
	c_app_user_profile  text;
	n_company_code_desc text;
BEGIN
	-- get user, client name and company id from current connection
	SELECT 
        c.app_user_code,
        c.client_name,
        c.company_id 
    INTO 
        c_app_user,
        c_app_client_name,
        c_app_company 
    FROM system.connection c 
    WHERE c.session_id = pg_backend_pid();

	-- check new company name
	IF NOT EXISTS(SELECT company_id 
                  FROM system.company 
                  WHERE company_id = in_new_company) THEN
		RAISE EXCEPTION 'Unknown company id ''%''', in_new_company 
		USING HINT = 'The provided company id does not exists', ERRCODE = 'PA007';
	END IF;

	-- check access rights for user to new compay
	SELECT uc.profile_code INTO c_app_user_profile 
    FROM system.app_user_company uc 
    WHERE uc.app_user_code = c_app_user 
        AND uc.company_id = in_new_company;
	IF c_app_user_profile IS NULL THEN
		RAISE EXCEPTION 'User ''%'' have no access rights for company ''%''', c_app_user, in_new_company 
		USING HINT = 'check user privileges for the provided company', ERRCODE = 'PA008';
	END IF;

	-- update or insert a connection record
	IF c_app_company IS NULL THEN
		-- update current application connection
		UPDATE system.connection 
		SET company_id = in_new_company, profile_code = c_app_user_profile
		WHERE session_id = pg_backend_pid();
	ELSE
		-- close previous application connection and create a new one
		DELETE FROM system.connection 
        WHERE session_id = pg_backend_pid();
		-- log access
		INSERT INTO system.connection (app_user_code, client_name, company_id, profile_code) 
		VALUES (c_app_user, c_app_client_name, in_new_company, c_app_user_profile);
	END IF;
	
    -- update user's lastcompany
	SELECT company_id::text || ' ' || description 
    INTO n_company_code_desc 
    FROM system.company 
    WHERE company_id = in_new_company;
	
    UPDATE system.app_user 
    SET last_company = in_new_company,
        last_company_desc = n_company_code_desc 
    WHERE user_code = c_app_user;
	
	RETURN QUERY
        SELECT 
            c.company_id,
            co.description,
            co.company_image,
            c.profile_code,
            uc.menu_code,
            uc.toolbar_code
        FROM system.connection c
        JOIN system.company co ON c.company_id = co.company_id
        JOIN system.app_user_company uc ON c.app_user_code = uc.app_user_code AND c.company_id = uc.company_id
        --JOIN system.profile p ON uc.profile_code = p.code
        WHERE c.session_id = pg_backend_pid();
END;
$$
LANGUAGE plpgsql;
COMMENT ON FUNCTION pa_company_change(int) IS
    'Function for change company in the currrent application connection';
ALTER FUNCTION pa_company_change(int) 
    OWNER TO {pyAppPgOwnerRole};


-- system function: kill client connection
CREATE FUNCTION pa_kill_client(in_cid int)
RETURNS void AS
$$
BEGIN
	DELETE FROM system.connection 
    WHERE session_id = in_cid;
	IF in_cid = (SELECT pg_backend_pid()) THEN
		RAISE 'Can not kill current connection' 
		USING HINT = 'You are trying to kill your current connection and this is not allowed',  ERRCODE = 'PA009';
	END IF;
	IF EXISTS(SELECT pid FROM pg_stat_activity WHERE pid = in_cid) THEN
		PERFORM pg_terminate_backend(in_cid);
	END IF;
END;
$$
LANGUAGE plpgsql;
COMMENT ON FUNCTION pa_kill_client(int) IS 
    'Function force client exit';
ALTER FUNCTION pa_kill_client(int) 
    OWNER TO {pyAppPgOwnerRole};
