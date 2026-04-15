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


-- *** PROFILE/MENU/TOOLBAR FOR CASHIER ONLY *** --

-- profile
INSERT INTO profile (profile_code, description, is_system_object) 
VALUES
('cashier', 'Solo cassa', false);

-- profile actions
INSERT INTO profile_action (profile_code, action, auth) 
VALUES
('cashier', 'sys_change_company', 'X'),
('cashier', 'sys_change_password', 'X'),
('cashier', 'sys_preferences', 'X'),
('cashier', 'sys_quit', 'X'),
('cashier', 'edit_new', 'X'),
('cashier', 'edit_save', 'X'),
('cashier', 'edit_delete', 'X'),
('cashier', 'edit_reload', 'X'),
('cashier', 'edit_first', 'X'),
('cashier', 'edit_previous', 'X'),
('cashier', 'edit_counter', 'X'),
('cashier', 'edit_next', 'X'),
('cashier', 'edit_last', 'X'),
('cashier', 'edit_filter', 'X'),
('cashier', 'edit_change_view', 'X'),
('cashier', 'edit_print', 'X'),
('cashier', 'edit_export', 'X'),
('cashier', 'help_index', 'X'),
('cashier', 'help_faq', 'X'),
('cashier', 'about_program', 'X'),
('cashier', 'about_qt', 'X'),
('cashier', 'about_system_info', 'X'),
('cashier', 'app_file_cash_desk', 'R'),
('cashier', 'app_file_order', 'X'),
('cashier', 'app_activity_order_entry', 'X'),
('cashier', 'app_activity_stock_inventory', 'R'),
('cashier', 'app_activity_order_progress', 'R'),
('cashier', 'app_activity_stock_unload', 'R'),
('cashier', 'app_activity_sales_summary', 'X');

-- menu
INSERT INTO menu_toolbar (type, code, description, is_system_object) 
VALUES
-- IT menu
('M', 'm_cashier_it', 'Solo cassa', false);

-- menu items
INSERT INTO menu_toolbar_item (parent, child, description, sorting, item_type, action) 
VALUES
('m_cashier_it', 'cs', 'Sistema', 10, 'M', Null),
('m_cashier_it', 'cfi', 'Archivi', 20, 'M', Null),
('m_cashier_it', 'ae', 'Modifica', 30, 'M', Null),
('m_cashier_it', 'cac', 'Attività', 40, 'M', Null),
('m_cashier_it', 'ch', 'Aiuto', 99, 'M', Null),
-- system menu
('cs', 'cscc', Null, 1, 'A', 'sys_change_company'),
('cs', 'css1', Null, 2, 'S', Null),
('cs', 'cscp', Null, 3, 'A', 'sys_change_password'),
('cs', 'css2', Null, 4, 'S', Null),
('cs', 'csct', Null, 5, 'A', 'sys_preferences'),
('cs', 'css3', Null, 6, 'S', Null),
('cs', 'csq', Null, 7, 'A', 'sys_quit'),
-- help menu
('ch', 'chi', Null, 1, 'A', 'help_index'),
('ch', 'chf', Null, 2, 'A', 'help_faq'),
('ch', 'chs1', Null, 3, 'S', Null),
('ch', 'chs', Null, 4, 'A', 'about_system_info'),
('ch', 'chs2', Null, 5, 'S', Null),
('ch', 'cha', Null, 6, 'A', 'about_program'),
('ch', 'chqt', Null, 7, 'A', 'about_qt'),
-- file menu
('cfi', 'cficdk', Null, 1, 'A', 'app_file_cash_desk'),
('cfi', 'cfiord', Null, 2, 'A', 'app_file_order'),
-- activities menu
('cac', 'cacord', Null, 1, 'A', 'app_activity_order_entry'),
('cac', 'cacsp1', Null, 2, 'S', Null),
('cac', 'cacsp2', Null, 6, 'S', Null),
('cac', 'cacins', Null, 7, 'A', 'app_activity_sales_summary');

-- toolbar
INSERT INTO menu_toolbar (type, code, description, is_system_object) 
VALUES
('T', 't_cashier_it', 'Solo cassa', false);

-- toolbar items
INSERT INTO menu_toolbar_item (parent, child, description, sorting, item_type, action) 
VALUES
('t_cashier_it', 'tae', 'Modifica', 2, 'T', Null),
('t_cashier_it', 'tsqa', 'Accesso rapido', 4, 'T', Null),
('tsqa', 'tsqaord', Null, 1, 'T', 'app_activity_order_entry');


-- *** PROFILE/MENU/TOOLBAR FOR ORDER PROGRESS ONLY *** --

-- profile
INSERT INTO profile (profile_code, description, is_system_object) 
VALUES
('progress', 'Solo avanzamento ordini', false);

-- profile actions
INSERT INTO profile_action (profile_code, action, auth) 
VALUES
('progress', 'sys_change_company', 'X'),
('progress', 'sys_change_password', 'X'),
('progress', 'sys_preferences', 'X'),
('progress', 'sys_quit', 'X'),
('progress', 'edit_new', 'X'),
('progress', 'edit_save', 'X'),
('progress', 'edit_delete', 'X'),
('progress', 'edit_reload', 'X'),
('progress', 'edit_first', 'X'),
('progress', 'edit_previous', 'X'),
('progress', 'edit_counter', 'X'),
('progress', 'edit_next', 'X'),
('progress', 'edit_last', 'X'),
('progress', 'edit_filter', 'X'),
('progress', 'edit_change_view', 'X'),
('progress', 'edit_print', 'X'),
('progress', 'edit_export', 'X'),
('progress', 'help_index', 'X'),
('progress', 'help_faq', 'X'),
('progress', 'about_program', 'X'),
('progress', 'about_qt', 'X'),
('progress', 'about_system_info', 'X'),
('progress', 'app_file_order', 'X'),
('progress', 'app_activity_order_progress', 'X');

-- menu
INSERT INTO menu_toolbar (type, code, description, is_system_object) 
VALUES
-- IT menu
('M', 'm_progress_it', 'Solo avanzamento ordini', false);

-- menu items
INSERT INTO menu_toolbar_item (parent, child, description, sorting, item_type, action) 
VALUES
('m_progress_it', 'ps', 'Sistema', 10, 'M', Null),
('m_progress_it', 'pfi', 'Archivi', 20, 'M', Null),
('m_progress_it', 'ae', 'Modifica', 30, 'M', Null),
('m_progress_it', 'pac', 'Attività', 40, 'M', Null),
('m_progress_it', 'ph', 'Aiuto', 99, 'M', Null),
-- system menu
('ps', 'sscc', Null, 1, 'A', 'sys_change_company'),
('ps', 'pss1', Null, 2, 'S', Null),
('ps', 'pscp', Null, 3, 'A', 'sys_change_password'),
('ps', 'pss2', Null, 4, 'S', Null),
('ps', 'psct', Null, 5, 'A', 'sys_preferences'),
('ps', 'pss3', Null, 6, 'S', Null),
('ps', 'psq', Null, 7, 'A', 'sys_quit'),
-- help menu
('ph', 'phi', Null, 1, 'A', 'help_index'),
('ph', 'phf', Null, 2, 'A', 'help_faq'),
('ph', 'phs1', Null, 3, 'S', Null),
('ph', 'phs', Null, 4, 'A', 'about_system_info'),
('ph', 'phs2', Null, 5, 'S', Null),
('ph', 'pha', Null, 6, 'A', 'about_program'),
('ph', 'phqt', Null, 7, 'A', 'about_qt'),
-- file menu
('pfi', 'pficdk', Null, 1, 'A', 'app_file_cash_desk'),
('pfi', 'pfiord', Null, 2, 'A', 'app_file_order'),
-- activities menu
('pac', 'pacord', Null, 1, 'A', 'app_activity_order_progress');

-- toolbar
INSERT INTO menu_toolbar (type, code, description, is_system_object) 
VALUES
('T', 't_progress_it', 'Solo avanzamento ordini', false);

-- toolbar items
INSERT INTO menu_toolbar_item (parent, child, description, sorting, item_type, action) 
VALUES
('t_progress_it', 'tae', 'Modifica', 2, 'T', Null),
('t_progress_it', 'tpqa', 'Accesso rapido', 4, 'T', Null),
('tpqa', 'tpqaord', Null, 1, 'T', 'app_activity_order_progress');


-- DEMO COMPANY
-- create demo company
SELECT
system.pa_company_create(10, 'First demo company / Prima azienda dimostrativa', true, Null),
system.pa_company_create(20, 'Second demo company / Seconda azienda dimostrativa', true, Null);

-- USERS
-- create application users
INSERT INTO app_user (user_code, description, user_password, is_admin, is_system_object, can_edit_views, can_edit_sortfilters, can_edit_reports, l10n) 
VALUES
('utente', 'Utente applicativo di {pyAppName}', system.crypt('utente', system.gen_salt('bf')), False, False, False, False, False, 'it_IT'),
('cassa', 'Operatore cassa', system.crypt('cassa', system.gen_salt('bf')), False, False, False, False, False, 'it_IT'),
('avanza', 'Avanzamento ordini', system.crypt('avanza', system.gen_salt('bf')), False, False, False, False, False, 'it_IT');

-- additional profile/menu for users
INSERT INTO system.app_user_company (app_user_code, company_id, profile_code, menu_code, toolbar_code) 
VALUES
('system', 10, 'full', 'm_full_en', 't_full_en'),
('system', 20, 'full', 'm_full_en', 't_full_en'),
('utente', 10, 'default', 'm_default_it', 't_default_it'),
('utente', 20, 'default', 'm_default_it', 't_default_it'),
('cassa', 10, 'cashier', 'm_cashier_it', 't_cashier_it'),
('cassa', 20, 'cashier', 'm_cashier_it', 't_cashier_it'),
('avanza', 10, 'progress', 'm_progress_it', 't_progress_it'),
('avanza', 20, 'progress', 'm_progress_it', 't_progress_it');



