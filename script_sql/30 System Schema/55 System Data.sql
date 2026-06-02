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


-- system.settings parameters list
SELECT
pa_setting_set('app_name', '{pyAppName}'),
pa_setting_set('app_description', '{pyAppDescription}'),
pa_setting_set('app_system_user', 'system'),
pa_setting_set('password_expire_days', '180'),
pa_setting_set('strong_password_required', 'false');

-- create default profiles
INSERT INTO profile (profile_code, description, is_system_object) 
VALUES
('default', 'Default profile', true),
('full', 'Full privileges profile', true);

-- system.profile_actions
INSERT INTO profile_action (profile_code, action, auth) 
VALUES
-- full profile
('full', 'sys_change_company', 'X'),
('full', 'sys_change_password', 'X'),
('full', 'sys_preferences', 'X'),
('full', 'sys_quit', 'X'),
('full', 'sys_company', 'X'),
('full', 'sys_connection', 'X'),
('full', 'sys_connection_history', 'X'),
('full', 'sys_user', 'X'),
('full', 'sys_profile', 'X'),
('full', 'sys_menu', 'X'),
('full', 'sys_toolbar', 'X'),
('full', 'sys_report', 'X'),
('full', 'sys_scripting', 'X'),
('full', 'sys_customization', 'X'),
('full', 'edit_new', 'X'),
('full', 'edit_save', 'X'),
('full', 'edit_delete', 'X'),
('full', 'edit_reload', 'X'),
('full', 'edit_first', 'X'),
('full', 'edit_previous', 'X'),
('full', 'edit_counter', 'X'),
('full', 'edit_next', 'X'),
('full', 'edit_last', 'X'),
('full', 'edit_filter', 'X'),
('full', 'edit_change_view', 'X'),
('full', 'edit_print', 'X'),
('full', 'edit_export', 'X'),
('full', 'help_index', 'X'),
('full', 'help_faq', 'X'),
('full', 'about_program', 'X'),
('full', 'about_qt', 'X'),
('full', 'about_system_info', 'X'),
-- default profile
('default', 'sys_change_company', 'X'),
('default', 'sys_change_password', 'X'),
('default', 'sys_preferences', 'X'),
('default', 'sys_quit', 'X'),
('default', 'edit_new', 'X'),
('default', 'edit_save', 'X'),
('default', 'edit_delete', 'X'),
('default', 'edit_reload', 'X'),
('default', 'edit_first', 'X'),
('default', 'edit_previous', 'X'),
('default', 'edit_counter', 'X'),
('default', 'edit_next', 'X'),
('default', 'edit_last', 'X'),
('default', 'edit_filter', 'X'),
('default', 'edit_change_view', 'X'),
('default', 'edit_print', 'X'),
('default', 'edit_export', 'X'),
('default', 'help_index', 'X'),
('default', 'help_faq', 'X'),
('default', 'about_program', 'X'),
('default', 'about_qt', 'X'),
('default', 'about_system_info', 'X');

-- MENU
INSERT INTO menu_toolbar (type, code, description, is_system_object) 
VALUES
-- EN menu
('M', 'm_full_en', 'Full menu', true),
('M', 'm_full_it', 'Menu completo', true),
-- IT menu
('M', 'm_default_it', 'Menu predefinito', true);

-- MENU ITEMS
INSERT INTO menu_toolbar_item (parent, child, description, sorting, item_type, action) 
VALUES
-- full system menu
('m_full_en', 'fs', 'System', 1, 'M', Null),
('m_full_en', 'ae', 'Edit', 15, 'M', Null),
('m_full_en', 'fh', 'Help', 99, 'M', Null),

('m_full_it', 'fs', 'Sistema', 1, 'M', Null),
('m_full_it', 'ae', 'Modifica', 15, 'M', Null),
('m_full_it', 'fh', 'Aiuto', 99, 'M', Null),

('fs', 'fscc', Null, 1, 'A', 'sys_change_company'),
('fs', 'fss1', Null, 2, 'S', Null),
('fs', 'fscp', Null, 3, 'A', 'sys_change_password'),
('fs', 'fss2', Null, 4, 'S', Null),
('fs', 'fspr', Null, 5, 'A', 'sys_preferences'),
('fs', 'fss3', Null, 6, 'S', Null),
('fs', 'fscn', Null, 9, 'A', 'sys_connection'),
('fs', 'fscnh', Null, 10, 'A', 'sys_connection_history'),
('fs', 'fss5', Null, 11, 'S', Null),
('fs', 'fsmc', Null, 12, 'A', 'sys_company'),
('fs', 'fsmp', Null, 13, 'A', 'sys_profile'),
('fs', 'fsmu', Null, 14, 'A', 'sys_user'),
('fs', 'fss6', Null, 16, 'S', Null),
('fs', 'fsmtm', Null, 18, 'A', 'sys_menu'),
('fs', 'fsmtt', Null, 19, 'A', 'sys_toolbar'),
('fs', 'fsmts', Null, 20, 'A', 'sys_shortcut'),
('fs', 'fss7', Null, 21, 'S', Null),
('fs', 'fsrp', Null, 22, 'A', 'sys_report'),
('fs', 'fssc', Null, 23, 'A', 'sys_scripting'),
('fs', 'fscu', Null, 25, 'A', 'sys_customization'),
('fs', 'fss8', Null, 26, 'S', Null),
('fs', 'fsq', Null, 27, 'A', 'sys_quit'),
-- menu edit for all
('ae', 'aenw', Null, 1, 'A', 'edit_new'),
('ae', 'aesa', Null, 2, 'A', 'edit_save'),
('ae', 'aede', Null, 3, 'A', 'edit_delete'),
('ae', 'aerl', Null, 4, 'A', 'edit_reload'),
('ae', 'aes1', Null, 5, 'S', Null),
('ae', 'aefr', Null, 6, 'A', 'edit_first'),
('ae', 'aepr', Null, 7, 'A', 'edit_previous'),
('ae', 'aene', Null, 8, 'A', 'edit_next'),
('ae', 'aela', Null, 9, 'A', 'edit_last'),
('ae', 'aes2', Null, 10, 'S', Null),
('ae', 'aefl', Null, 11, 'A', 'edit_filter'),
('ae', 'aecv', Null, 12, 'A', 'edit_change_view'),
('ae', 'aes3', Null, 13, 'S', Null),
('ae', 'aept', Null, 14, 'A', 'edit_print'),
('ae', 'aeex', Null, 15, 'A', 'edit_export'),
-- full help menu
('fh', 'fhi', Null, 1, 'A', 'help_index'),
('fh', 'fhf', Null, 2, 'A', 'help_faq'),
('fh', 'fhs1', Null, 3, 'S', Null),
('fh', 'fhs', Null, 4, 'A', 'about_system_info'),
('fh', 'fhs2', Null, 5, 'S', Null),
('fh', 'fha', Null, 6, 'A', 'about_program'),
('fh', 'fhqt', Null, 7, 'A', 'about_qt'),
-- menu default IT
('m_default_it', 'ds', 'Sistema', 1, 'M', Null),
('m_default_it', 'ae', 'Modifica', 15, 'M', Null),
('m_default_it', 'dh', 'Aiuto', 99, 'M', Null),
('ds', 'dscc', Null, 1, 'A', 'sys_change_company'),
('ds', 'dss1', Null, 2, 'S', Null),
('ds', 'dscp', Null, 3, 'A', 'sys_change_password'),
('ds', 'dss2', Null, 4, 'S', Null),
('ds', 'dsct', Null, 5, 'A', 'sys_preferences'),
('ds', 'dss3', Null, 6, 'S', Null),
('ds', 'dsq', Null, 7, 'A', 'sys_quit'),
('dh', 'dhi', Null, 1, 'A', 'help_index'),
('dh', 'dhf', Null, 2, 'A', 'help_faq'),
('dh', 'dhs1', Null, 3, 'S', Null),
('dh', 'dhs', Null, 4, 'A', 'about_system_info'),
('dh', 'dhs2', Null, 5, 'S', Null),
('dh', 'dha', Null, 6, 'A', 'about_program'),
('dh', 'dhqt', Null, 7, 'A', 'about_qt');

-- TOOLBAR
INSERT INTO menu_toolbar (type, code, description, is_system_object) 
VALUES
-- EN
('T', 't_full_en', 'Full', True),
-- IT
('T', 't_default_it', 'Predefinita', True);

-- TOOLBAR ITEMS
INSERT INTO menu_toolbar_item (parent, child, description, sorting, item_type, action) 
VALUES
-- EN toolbars
-- full toolbars
('t_full_en', 'tae', 'Edit', 2, 'T', Null),
('t_full_en', 'tfqa', 'Quick access', 4, 'T', Null),
('tae', 'taene', Null, 1, 'A', 'edit_new'),
('tae', 'taesa', Null, 2, 'A', 'edit_save'),
('tae', 'taede', Null, 3, 'A', 'edit_delete'),
('tae', 'taerl', Null, 4, 'A', 'edit_reload'),
('tae', 'taes1', Null, 5, 'S', Null),
('tae', 'taefr', Null, 6, 'A', 'edit_first'),
('tae', 'taepr', Null, 7, 'A', 'edit_previous'),
('tae', 'taect', Null, 8, 'A', 'edit_counter'),
('tae', 'taenx', Null, 9, 'A', 'edit_next'),
('tae', 'taels', Null, 10, 'A', 'edit_last'),
('tae', 'taes2', Null, 11, 'S', Null),
('tae', 'taefl', Null, 12, 'A', 'edit_filter'),
('tae', 'taecv', Null, 13, 'A', 'edit_change_view'),
('tae', 'taes3', Null, 14, 'S', Null),
('tae', 'taept', Null, 15, 'A', 'edit_print'),
('tae', 'taeex', Null, 16, 'A', 'edit_export'),
-- IT toolbars
-- default toolbars
('t_default_it', 'tae', 'Modifica', 2, 'T', Null),
('t_default_it', 'tdqa', 'Accesso rapido', 4, 'T', Null);

-- app users
INSERT INTO app_user (user_code, description, user_password, is_admin, is_system_object, can_edit_views, can_edit_sortfilters, can_edit_reports, l10n) 
VALUES 
('system', '{pyAppName} system administrator', system.crypt('System@1', system.gen_salt('bf')), True, True, True, True, True, 'en_US'),
('sistema', 'Amministratore del sistema {pyAppName}', system.crypt('Sistem@1', system.gen_salt('bf')), True, True, True, True, True, 'it_IT'),
('pySagraWeb', '{pyAppName} web order entry system user', system.crypt('pySagraWeb', system.gen_salt('bf')), False, True, False, False, False, 'en_US');


