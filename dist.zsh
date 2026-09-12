#!/bin/zsh

# move to projec root
cd /Users/paolo/Development/pySagra

# activate virtual env
source /Users/paolo/Development/.venv/pyside-psycopg/bin/activate

pyinstaller --clean \
	--onedir \
	--windowed \
	--icon Icon/pySagra.icns \
	--exclude-module PySide6.QtDBus \
	--exclude-module PySide6.QtQml \
	--exclude-module PySide6.QtQuick \
	pySagra.py
	
# remove security issue on macos
#xattr -cr dist/pySagra.app
codesign --force --deep --sign - /Users/paolo/Development/pySagra/dist/pySagra.app

# exit from venv
deactivate
