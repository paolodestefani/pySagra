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


-------------------------------
-- DEFINITION OF THE SCHEMAS --
-------------------------------

-- remove all schemas including public schema
DROP SCHEMA IF EXISTS public    CASCADE;
DROP SCHEMA IF EXISTS demo1     CASCADE;
DROP SCHEMA IF EXISTS demo2     CASCADE;
DROP SCHEMA IF EXISTS common    CASCADE;
DROP SCHEMA IF EXISTS common1   CASCADE;
DROP SCHEMA IF EXISTS common2   CASCADE;
DROP SCHEMA IF EXISTS company   CASCADE;
DROP SCHEMA IF EXISTS system    CASCADE;
DROP SCHEMA IF EXISTS temp    CASCADE;

-- create system schema
CREATE SCHEMA system AUTHORIZATION  {pyAppPgOwnerRole};
COMMENT ON SCHEMA system IS 
    'System schema for {pyAppName} database';

-- create common schema
CREATE SCHEMA common AUTHORIZATION {pyAppPgOwnerRole};
COMMENT ON SCHEMA common IS 
    'Common schema for {pyAppName} database, container of all objects shared between companies';

-- create company schema
CREATE SCHEMA company AUTHORIZATION {pyAppPgOwnerRole};
COMMENT ON SCHEMA company IS 
    'Company schema for {pyAppName} database, container of company specific objects';

-- create temp schema
CREATE SCHEMA temp AUTHORIZATION {pyAppPgOwnerRole};
COMMENT ON SCHEMA company IS 
    'Temp schema for {pyAppName} database, container of objects used only temporarily';

