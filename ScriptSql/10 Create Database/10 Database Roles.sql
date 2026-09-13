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


--------------------
-- DATABASE ROLES --
--------------------

DO LANGUAGE plpgsql
$$
BEGIN
    IF NOT EXISTS (
        SELECT rolname
        FROM   pg_roles
        WHERE  rolname = '{pyAppPgOwnerRole}') 
        THEN
            CREATE ROLE {pyAppPgOwnerRole} 
                WITH NOSUPERUSER NOINHERIT NOCREATEDB NOCREATEROLE NOLOGIN;
            COMMENT ON ROLE {pyAppPgOwnerRole} IS 
                'PostgreSQL group role that owns all {pyAppName} db objects without login priviledge';
            IF '{pyAppPgDataBaseTS}' != 'pg_default' THEN
                GRANT CREATE ON TABLESPACE {pyAppPgDataBaseTS} TO {pyAppPgOwnerRole};
            END IF;
            IF '{pyAppPgTablesTS}' != 'pg_default' THEN
                GRANT CREATE ON TABLESPACE {pyAppPgTablesTS} TO {pyAppPgOwnerRole};
            END IF;
            IF '{pyAppPgIndexesTS}' != 'pg_default' THEN
                GRANT CREATE ON TABLESPACE {pyAppPgIndexesTS} TO {pyAppPgOwnerRole};
            END IF;
    END IF;
    IF NOT EXISTS (
        SELECT rolname
        FROM   pg_roles
        WHERE  rolname = '{pyAppPgLoginRole}') 
        THEN
            CREATE ROLE {pyAppPgLoginRole} 
                WITH NOSUPERUSER INHERIT NOCREATEDB NOCREATEROLE LOGIN PASSWORD '{pyAppPgLoginPassword}';
            COMMENT ON ROLE {pyAppPgLoginRole} IS 
                'PostgreSQL login role that inherits {pyAppPgOwnerRole} privileges';
            GRANT {pyAppPgOwnerRole} TO {pyAppPgLoginRole};
    END IF;
END
$$;
