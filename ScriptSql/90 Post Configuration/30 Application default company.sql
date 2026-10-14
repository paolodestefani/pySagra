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

-- for string quoting put a * e.g. {pyAppPgOwnerRole*} -> 'pa_owner_role'


----------------------------
-- COMPANY SCHEMA OBJECTS --
----------------------------

SET search_path = system;


-- DEFAULT USERS
-- app users
INSERT INTO app_user (user_code, description, user_password, is_admin, is_system_object, can_edit_views, can_edit_sortfilters, can_edit_reports, l10n, icon_theme) 
VALUES 
('system', '{pyAppName} system administrator', system.crypt('system', system.gen_salt('bf')), True, True, True, True, True, 'en_US', 'oxygen'),
('sistema', 'Amministratore del sistema {pyAppName}', system.crypt('sistema', system.gen_salt('bf')), True, True, True, True, True, 'it_IT', 'flatwoken'),
('user', 'Default user', system.crypt('user', system.gen_salt('bf')), False, False, False, False, False, 'en_US', 'oxygen'),
('utente', 'Utente predefinito', system.crypt('utente', system.gen_salt('bf')), False, False, False, False, False, 'it_IT', 'flatwoken'),
('pySagraWeb', '{pyAppName} web system user', system.crypt('pySagraWeb', system.gen_salt('bf')), False, True, False, False, False, 'en_US', Null);

-- DEFAULT COMPANY
-- create default company
SELECT
system.pa_company_create(10, 'pySagra', true, Null);

-- user company settings
INSERT INTO app_user_company (app_user_code, company_id, profile_code, menu_code, toolbar_code) 
VALUES
('system', 10, 'full', 'm_full_en', 't_full_en'),
('sistema', 10, 'full', 'm_full_it', 't_full_it'),
('user', 10, 'default', 'm_default_en', 't_default_en'),
('utente', 10, 'default', 'm_default_it', 't_default_it'),
('pySagraWeb', 10, 'full', 'm_full_it', 't_full_en');



