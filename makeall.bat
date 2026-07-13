@ECHO OFF

ECHO move to projec root
cd C:\pyWare\pySagra

ECHO activate virtual env
call "C:\PyWare\.venv\pysidepsycopg\Scripts\activate.bat"

ECHO create lib ui modules
"c:\windows\system32\forfiles.exe" /P "App\Ui" /M *.ui /c "cmd /c pyside6-uic -o @fname.py @file"

ECHO Translations without pro file sources and forms
pyside6-lupdate^
 pySagra.py^
 App\Core\ExceptionHandler.py^
 App\Core\Gui.py^
 App\Core\Scripting.py^
 App\Database\Models.py^
 App\System\About.py^
 App\System\Action.py^
 App\System\Company.py^
 App\System\Connection.py^
 App\System\Customization.py^
 App\System\Help.py^
 App\System\Login.py^
 App\System\Mainwindow.py^
 App\System\Menu.py^
 App\System\Preferences.py^
 App\System\Profile.py^
 App\System\Report.py^
 App\System\Scripting.py^
 App\System\User.py^
 App\Widget\Control.py^
 App\Widget\Delegate.py^
 App\Widget\Dialog.py^
 App\Widget\Form.py^
 App\Widget\View.py^
 App\Ui\AboutDialog.ui^
 App\Ui\CashDeskWidget.ui^
 App\Ui\ChangeCompanyDialog.ui^
 App\Ui\ChangePasswordDialog.ui^
 App\Ui\ChooseItemDialog.ui^
 App\Ui\ChooseVariantsDialog.ui^
 App\Ui\CompanyWidget.ui^
 App\Ui\ConnectionHistoryWidget.ui^
 App\Ui\ConnectionWidget.ui^
 App\Ui\CopyToolDialog.ui^
 App\Ui\CustomizationsDialog.ui^
 App\Ui\DateTimeInputDialog.ui^
 App\Ui\DeleteToolDialog.ui^
 App\Ui\DepartmentPrinterWidget.ui^
 App\Ui\DepartmentWidget.ui^
 App\Ui\DuplicateDialog.ui^
 App\Ui\EventFilterDialog.ui^
 App\Ui\EventToolDialog.ui^
 App\Ui\EventWidget.ui^
 App\Ui\GenericFormViewWidget.ui^
 App\Ui\HelpDialog.ui^
 App\Ui\InventoryWidget.ui^
 App\Ui\ItemWidget.ui^
 App\Ui\LoginDialog.ui^
 App\Ui\MenuWidget.ui^
 App\Ui\MessageDialog.ui^
 App\Ui\NewCompanyDialog.ui^
 App\Ui\OrderDialog0.ui^
 App\Ui\OrderDialog1.ui^
 App\Ui\OrderDialog2.ui^
 App\Ui\OrderedDeliveredWidget.ui^
 App\Ui\OrderProgressWidget.ui^
 App\Ui\OrderWidget.ui^
 App\Ui\PreferencesDialog.ui^
 App\Ui\PriceListWidget.ui^
 App\Ui\PrintDialog.ui^
 App\Ui\ProfileWidget.ui^
 App\Ui\ReportWidget.ui^
 App\Ui\SalesSummaryWidget.ui^
 App\Ui\ScriptingWidget.ui^
 App\Ui\SeatMapWidget.ui^
 App\Ui\SelectImageDialog.ui^
 App\Ui\SettingsDialog.ui^
 App\Ui\SortFilterDialog.ui^
 App\Ui\StatisticsExportDialog.ui^
 App\Ui\SystemInfoDialog.ui^
 App\Ui\ToolbarWidget.ui^
 App\Ui\UpdateWebOrderServerDialog.ui^
 App\Ui\UserWidget.ui^
 App\Ui\ViewSettingsDialog.ui^
 App\CashDesk.py^
 App\Department.py^
 App\Event.py^
 App\Inventory.py^
 App\Item.py^
 App\OrderArchive.py^
 App\OrderedDelivered.py^
 App\OrderEntry.py^
 App\OrderNumbering.py^
 App\OrderProgress.py^
 App\PriceList.py^
 App\Printer.py^
 App\SalesSummary.py^
 App\SeatMap.py^
 App\Settings.py^
 App\Statistics.py^
 App\Tool.py^
 App\UpdateWOS.py^
 -tr-function-alias translate+=_tr -noobsolete -ts translation\ts\pySagra_it.ts

pyside6-lrelease translation\ts\pySagra_it.ts -qm translation\pySagra_it.qm

ECHO resources
pyside6-rcc resources.qrc -o resources_rc.py 

ECHO exit from venv
call deactivate

pause
