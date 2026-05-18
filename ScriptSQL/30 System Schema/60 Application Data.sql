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


-- APPLICATION PROFILE ACTIONS

INSERT INTO profile_action (profile_code, action, auth) 
VALUES
-- full
('full', 'app_file_cash_desk', 'X'),
('full', 'app_file_printer', 'X'),
('full', 'app_file_department', 'X'),
('full', 'app_file_seat_map', 'X'),
('full', 'app_file_item', 'X'),
('full', 'app_file_price_list', 'X'),
('full', 'app_file_event', 'X'),
('full', 'app_file_update_wo_server', 'X'),
('full', 'app_file_order', 'X'),
('full', 'app_file_order_number', 'X'),
('full', 'app_file_setting', 'X'),
('full', 'app_activity_order_entry', 'X'),
('full', 'app_activity_inventory', 'X'),
('full', 'app_activity_order_progress', 'X'),
('full', 'app_activity_ordered_delivered', 'X'),
('full', 'app_activity_sales_summary', 'X'),
('full', 'app_statistics_analysis', 'X'),
('full', 'app_statistics_print', 'X'),
('full', 'app_statistics_export', 'X'),
('full', 'app_tool_event_based', 'X'),
('full', 'app_tool_delete', 'X'),
('full', 'app_tool_copy', 'X'),
-- default
('default', 'app_file_cash_desk', 'R'),
('default', 'app_file_printer', 'R'),
('default', 'app_file_department', 'R'),
('default', 'app_file_seat_map', 'X'),
('default', 'app_file_item', 'X'),
('default', 'app_file_price_list', 'X'),
('default', 'app_file_event', 'R'),
('default', 'app_file_update_wo_server', 'X'),
('default', 'app_file_order', 'X'),
('default', 'app_file_order_number', 'R'),
('default', 'app_file_setting', 'R'),
('default', 'app_activity_order_entry', 'X'),
('default', 'app_activity_inventory', 'X'),
('default', 'app_activity_order_progress', 'X'),
('default', 'app_activity_ordered_delivered', 'X'),
('default', 'app_activity_sales_summary', 'X'),
('default', 'app_statistics_analysis', 'R'),
('default', 'app_statistics_print', 'X'),
('default', 'app_statistics_export', 'X'),
('default', 'app_tool_event_based', 'X'),
('default', 'app_tool_delete', 'X'),
('default', 'app_tool_copy', 'X');


-- APPLICATION MENU

-- FULL MENU EN
INSERT INTO menu_toolbar_item (parent, child, description, sorting, item_type, action) 
VALUES
('m_full_en', 'ffi', 'File', 10, 'M', Null), -- System is 1, Edit is 15, Help is 99
('m_full_en', 'fac', 'Activity', 20, 'M', Null),
('m_full_en', 'fst', 'Statistics', 30, 'M', Null),
('m_full_en', 'ftl', 'Tools', 40, 'M', Null),
-- file menu
('ffi', 'fficdk', Null, 1, 'A', 'app_file_cash_desk'),
('ffi', 'ffiprn', Null, 2, 'A', 'app_file_printer'),
('ffi', 'ffidep', Null, 3, 'A', 'app_file_department'),
('ffi', 'ffisem', Null, 4, 'A', 'app_file_seat_map'),
('ffi', 'ffiite', Null, 5, 'A', 'app_file_item'),
('ffi', 'ffiprl', Null, 6, 'A', 'app_file_price_list'),
('ffi', 'ffieve', Null, 7, 'A', 'app_file_event'),
('ffi', 'ffiuwo', Null, 8, 'A', 'app_file_update_wo_server'),
('ffi', 'ffisp1', Null, 9, 'S', Null),
('ffi', 'ffiord', Null, 10, 'A', 'app_file_order'),
('ffi', 'ffionm', Null, 11, 'A', 'app_file_order_number'),
('ffi', 'ffisp2', Null, 12, 'S', Null),
('ffi', 'ffiset', Null, 13, 'A', 'app_file_setting'),
-- activities menu
('fac', 'facord', Null, 1, 'A', 'app_activity_order_entry'),
('fac', 'facsp1', Null, 2, 'S', Null),
('fac', 'facsti', Null, 3, 'A', 'app_activity_inventory'),
('fac', 'faccun', Null, 4, 'A', 'app_activity_ordered_delivered'),
('fac', 'facopr', Null, 5, 'A', 'app_activity_order_progress'),
('fac', 'facsp2', Null, 6, 'S', Null),
('fac', 'facins', Null, 7, 'A', 'app_activity_sales_summary'),
-- statistics menu
('fst', 'fstana', Null, 1, 'A', 'app_statistics_analysis'),
('fst', 'fstpnt', Null, 2, 'A', 'app_statistics_print'),
('fst', 'fstsp1', Null, 3, 'S', Null),
('fst', 'fstexp', Null, 4, 'A', 'app_statistics_export'),
-- tools menu
('ftl', 'ftlebt', Null, 1, 'A', 'app_tool_event_based'),
('ftl', 'ftldel', Null, 2, 'A', 'app_tool_delete'),
('ftl', 'ftlcpy', Null, 3, 'A', 'app_tool_copy'),
-- FULL MENU IT
('m_full_it', 'ffi', 'Archivi', 10, 'M', Null), -- System is 1, Edit is 15, Help is 99
('m_full_it', 'fac', 'Attività', 20, 'M', Null),
('m_full_it', 'fst', 'Statistiche', 30, 'M', Null),
('m_full_it', 'ftl', 'Strumenti', 40, 'M', Null),

-- DEFAULT MENU
('m_default_it', 'dfi', 'Archivi', 10, 'M', Null), -- System is 1, Edit is 15, Help is 99
('m_default_it', 'dac', 'Attività', 20, 'M', Null),
('m_default_it', 'dst', 'Statistiche', 30, 'M', Null),
('m_default_it', 'dtl', 'Strumenti', 40, 'M', Null),
-- file menu
('dfi', 'dficdk', Null, 1, 'A', 'app_file_cash_desk'),
('dfi', 'dfiprn', Null, 2, 'A', 'app_file_printer'),
('dfi', 'dfidep', Null, 3, 'A', 'app_file_department'),
('dfi', 'dfisem', Null, 4, 'A', 'app_file_seat_map'),
('dfi', 'dfiite', Null, 5, 'A', 'app_file_item'),
('dfi', 'dfiprl', Null, 6, 'A', 'app_file_price_list'),
('dfi', 'dfieve', Null, 7, 'A', 'app_file_event'),
('dfi', 'dfiuwo', Null, 8, 'A', 'app_file_update_wo_server'),
('dfi', 'dfisp1', Null, 9, 'S', Null),
('dfi', 'dfiord', Null, 10, 'A', 'app_file_order'),
('dfi', 'dfionm', Null, 11, 'A', 'app_file_order_number'),
('dfi', 'dfisp2', Null, 12, 'S', Null),
('dfi', 'dfiset', Null, 13, 'A', 'app_file_setting'),
-- activities menu
('dac', 'dacord', Null, 1, 'A', 'app_activity_order_entry'),
('dac', 'dacsp1', Null, 2, 'S', Null),
('dac', 'dacsti', Null, 3, 'A', 'app_activity_inventory'),
('dac', 'daccsa', Null, 4, 'A', 'app_activity_ordered_delivered'),
('dac', 'dacopr', Null, 5, 'A', 'app_activity_order_progress'),
('dac', 'dacsp2', Null, 6, 'S', Null),
('dac', 'dacins', Null, 7, 'A', 'app_activity_sales_summary'),
-- statistics menu
('dst', 'dstana', Null, 1, 'A', 'app_statistics_analysis'),
('dst', 'dstpnt', Null, 2, 'A', 'app_statistics_print'),
('dst', 'dstsp1', Null, 3, 'S', Null),
('dst', 'dstexp', Null, 4, 'A', 'app_statistics_export'),
-- utilities menu
('dtl', 'dtlebt', Null, 1, 'A', 'app_tool_event_based'),
('dtl', 'dtldel', Null, 2, 'A', 'app_tool_delete'),
('dtl', 'dtlcpy', Null, 3, 'A', 'app_tool_copy');

-- TOOLBAR ITEMS
INSERT INTO menu_toolbar_item (parent, child, description, sorting, item_type, action) 
VALUES
-- EN toolbars
-- full toolbars
('tfqa', 'tfqaord', Null, 1, 'T', 'app_activity_order_entry'),
-- IT toolbars
-- default toolbars
('tdqa', 'tdqaord', Null, 1, 'T', 'app_activity_order_entry');
