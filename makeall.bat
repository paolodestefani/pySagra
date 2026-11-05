@ECHO OFF

ECHO move to projec root
cd C:\pyWare\pySagra

ECHO activate virtual env
call "C:\PyWare\.venv\pysagra\Scripts\activate.bat"

ECHO create lib ui modules
"c:\windows\system32\forfiles.exe" /P "App\Ui" /M *.ui /c "cmd /c pyside6-uic -o @fname.py @file"

ECHO Translations without pro file: every source and form, App\Ui\*.py are generated
REM AnalysisWidget.ui is excluded because it is still a work in progress
set LUPDATE_LIST=%TEMP%\pysagra_lupdate.lst
echo pySagra.py> "%LUPDATE_LIST%"
dir /s /b App\*.py | findstr /v /i /r "\\App\\Ui\\" >> "%LUPDATE_LIST%"
dir /s /b App\Ui\*.ui | findstr /v /i "AnalysisWidget.ui" >> "%LUPDATE_LIST%"
pyside6-lupdate @"%LUPDATE_LIST%" -tr-function-alias translate+=_tr -noobsolete -ts translation\ts\pySagra_it.ts

pyside6-lrelease translation\ts\pySagra_it.ts -qm translation\pySagra_it.qm

ECHO resources
pyside6-rcc resources.qrc -o resources_rc.py 

ECHO exit from venv
call deactivate

pause
