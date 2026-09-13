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


-- system table: application database version table, the current version is the latest
-- program and database must match only major and minor
CREATE TABLE version (
    major                   integer,
    minor                   integer,
    patch                   integer,        -- db patch <> application patch
    tag                     varchar(16),    -- db tag <> application tag
    installed_at            timestamp(3) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    description             varchar(60),
    note                    text,
    --
    CONSTRAINT version_pk 
        PRIMARY KEY (major, minor, patch)
        USING INDEX TABLESPACE {pyAppPgIndexesTS},
    CONSTRAINT version_major_check 
        CHECK (major BETWEEN 0 AND 999),
    CONSTRAINT version_minor_check 
        CHECK (minor BETWEEN 0 AND 999),
    CONSTRAINT version_patch_check 
        CHECK (patch BETWEEN 0 AND 99999)
    )
TABLESPACE {pyAppPgTablesTS};
COMMENT ON TABLE version IS
    '{pyAppName} version history, the current version is the latest';
ALTER TABLE version 
    OWNER TO {pyAppPgOwnerRole};


-- set database version
INSERT INTO version (
    major,
    minor,
    patch,
    tag,
    description
    )
VALUES (
    {pyAppVersionMajor},
    {pyAppVersionMinor},
    {pyAppVersionPatch},
    '{pyAppVersionTag}',
    '{pyAppVersionDescription}'
    );
