--
-- 
-- Upgrade profile and menu for 2.1
--

---------------------------
-- SYSTEM SCHEMA OBJECTS --
---------------------------

-- APPLICATION PROFILE ACTIONS
DELETE FROM system.profile_action;

INSERT INTO system.profile_action (profile, action, auth) VALUES
('full', 'app_file_printers', 'X'),
('full', 'app_file_departments', 'X'),
('full', 'app_file_tables', 'X'),
('full', 'app_file_items', 'X'),
('full', 'app_file_price_list', 'X'),
('full', 'app_file_events', 'X'),
('full', 'app_file_web_orders', 'X'),
('full', 'app_file_orders', 'X'),
('full', 'app_file_settings', 'X'),
('full', 'app_activities_orders', 'X'),
('full', 'app_activities_stock_inventory', 'X'),
('full', 'app_activities_order_progress', 'X'),
('full', 'app_activities_stock_unload', 'X'),
('full', 'app_activities_income_summary', 'X'),
('full', 'app_statistics_sales', 'X'),
('full', 'app_statistics_consumption', 'X'),
('full', 'app_statistics_export', 'X'),
('full', 'app_utilities_delete_orders', 'X'),
('full', 'app_utilities_unloads_rebuild', 'X'),
('full', 'app_utilities_numbering_rebuild', 'X'),
('full', 'app_utilities_mark_as_processed', 'X'),

('default', 'app_file_printers', 'R'),
('default', 'app_file_departments', 'R'),
('default', 'app_file_tables', 'X'),
('default', 'app_file_items', 'X'),
('default', 'app_file_price_list', 'X'),
('default', 'app_file_events', 'R'),
('default', 'app_file_web_orders', 'X'),
('default', 'app_file_orders', 'X'),
('default', 'app_file_settings', 'R'),
('default', 'app_activities_orders', 'X'),
('default', 'app_activities_stock_inventory', 'X'),
('default', 'app_activities_order_progress', 'X'),
('default', 'app_activities_stock_unload', 'X'),
('default', 'app_activities_income_summary', 'X'),
('default', 'app_statistics_sales', 'R'),
('default', 'app_statistics_consumption', 'X'),
('default', 'app_statistics_export', 'X'),
('default', 'app_utilities_delete_orders', 'X'),
('default', 'app_utilities_unloads_rebuild', 'X'),
('default', 'app_utilities_numbering_rebuild', 'X'),
('default', 'app_utilities_mark_as_processed', 'X');


-- APPLICATION MENU
DELETE FROM system.menu_item;

-- FULL MENU EN
INSERT INTO system.menu_item (parent, child, description, sorting, item_type, action) VALUES
('full_en', 'ffi', 'File', 10, 'M', Null), -- System is 1, Edit is 15, Help is 99
('full_en', 'fac', 'Activities', 20, 'M', Null),
('full_en', 'fst', 'Statistics', 30, 'M', Null),
('full_en', 'fut', 'Utilities', 40, 'M', Null),
-- file menu
('ffi', 'ffiprn', Null, 1, 'A', 'app_file_printers'),
--('ffi', 'fficsd', Null, 2, 'A', 'app_file_cash_desks'),
('ffi', 'ffidep', Null, 3, 'A', 'app_file_departments'),
('ffi', 'ffitab', Null, 4, 'A', 'app_file_tables'),
('ffi', 'ffiite', Null, 5, 'A', 'app_file_items'),
('ffi', 'ffiprl', Null, 6, 'A', 'app_file_price_list'),
('ffi', 'ffieve', Null, 7, 'A', 'app_file_events'),
('ffi', 'ffisp1', Null, 8, 'S', Null),
('ffi', 'ffiwor', Null, 9, 'A', 'app_file_web_orders'),
('ffi', 'ffiord', Null, 10, 'A', 'app_file_orders'),
('ffi', 'ffisp2', Null, 11, 'S', Null),
('ffi', 'ffiset', Null, 12, 'A', 'app_file_settings'),
-- activities menu
('fac', 'facord', Null, 1, 'A', 'app_activities_orders'),
('fac', 'facsp1', Null, 2, 'S', Null),
('fac', 'facsti', Null, 3, 'A', 'app_activities_stock_inventory'),
('fac', 'faccun', Null, 4, 'A', 'app_activities_stock_unload'),
('fac', 'facopr', Null, 5, 'A', 'app_activities_order_progress'),
('fac', 'facsp2', Null, 6, 'S', Null),
('fac', 'facins', Null, 7, 'A', 'app_activities_income_summary'),
-- statistics menu
('fst', 'fstsls', Null, 1, 'A', 'app_statistics_sales'),
('fst', 'fstcns', Null, 2, 'A', 'app_statistics_consumption'),
('fst', 'fstsp1', Null, 3, 'S', Null),
('fst', 'fstexp', Null, 4, 'A', 'app_statistics_export'),
-- utilities menu
('fut', 'futdor', Null, 1, 'A', 'app_utilities_delete_orders'),
('fut', 'futurb', Null, 2, 'A', 'app_utilities_unloads_rebuild'),
('fut', 'futnrb', Null, 3, 'A', 'app_utilities_numbering_rebuild'),
('fut', 'futmap', Null, 4, 'A', 'app_utilities_mark_as_processed'),

-- FULL MENU IT
('full_it', 'ffi', 'Archivi', 10, 'M', Null), -- System is 1, Edit is 15, Help is 99
('full_it', 'fac', 'Attività', 20, 'M', Null),
('full_it', 'fst', 'Statistiche', 30, 'M', Null),
('full_it', 'fut', 'Utility', 40, 'M', Null),

-- DEFAULT MENU
('default_it', 'dfi', 'Archivi', 10, 'M', Null), -- System is 1, Edit is 15, Help is 99
('default_it', 'dac', 'Attività', 20, 'M', Null),
('default_it', 'dst', 'Statistiche', 30, 'M', Null),
('default_it', 'dut', 'Utility', 40, 'M', Null),
-- file menu
('dfi', 'dfiprn', Null, 1, 'A', 'app_file_printers'),
('dfi', 'dfidep', Null, 3, 'A', 'app_file_departments'),
('dfi', 'dfitab', Null, 4, 'A', 'app_file_tables'),
('dfi', 'dfiite', Null, 5, 'A', 'app_file_items'),
('dfi', 'dfiprl', Null, 6, 'A', 'app_file_price_list'),
('dfi', 'dfieve', Null, 7, 'A', 'app_file_events'),
('dfi', 'dfisp1', Null, 8, 'S', Null),
('dfi', 'dfiwor', Null, 9, 'A', 'app_file_web_orders'),
('dfi', 'dfiord', Null, 10, 'A', 'app_file_orders'),
('dfi', 'dfisp2', Null, 11, 'S', Null),
('dfi', 'dfiset', Null, 12, 'A', 'app_file_settings'),
-- activities menu
('dac', 'dacord', Null, 1, 'A', 'app_activities_orders'),
('dac', 'dacsp1', Null, 2, 'S', Null),
('dac', 'dacsti', Null, 3, 'A', 'app_activities_stock_inventory'),
('dac', 'daccsa', Null, 4, 'A', 'app_activities_stock_unload'),
('dac', 'dacopr', Null, 5, 'A', 'app_activities_order_progress'),
('dac', 'dacsp2', Null, 6, 'S', Null),
('dac', 'dacins', Null, 7, 'A', 'app_activities_income_summary'),
-- statistics menu
('dst', 'dstsls', Null, 1, 'A', 'app_statistics_sales'),
('dst', 'dstcns', Null, 2, 'A', 'app_statistics_consumption'),
('dst', 'dstsp1', Null, 3, 'S', Null),
('dst', 'dstexp', Null, 4, 'A', 'app_statistics_export'),
-- utilities menu
('dut', 'dutdor', Null, 1, 'A', 'app_utilities_delete_orders'),
('dut', 'duturb', Null, 2, 'A', 'app_utilities_unloads_rebuild'),
('dut', 'dutnrb', Null, 3, 'A', 'app_utilities_numbering_rebuild'),
('dut', 'dutmap', Null, 4, 'A', 'app_utilities_mark_as_processed');
