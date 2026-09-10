@ECHO OFF

ECHO move to projec root
cd C:\pyWare\pySagra

ECHO activate virtual env
call "C:\PyWare\.venv\pysidepsycopg\Scripts\activate.bat"

ECHO create pyInstaller package
pyinstaller --clean^
 --onedir^
 --icon Icon\pySagra.ico^
 --windowed^
 --exclude-module PySide6.QtDBus^
 --exclude-module PySide6.QtQml^
 --exclude-module PySide6.QtQuick^
 pySagra.py

ECHO deactivate virtual env
call "C:\PyWare\.venv\pysidepsycopg\Scripts\deactivate.bat"

pause


