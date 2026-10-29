#!/bin/zsh

# move to projec root
cd /Users/paolo/Development/pySagra

# activate virtual env
source /Users/paolo/Development/.venv/pyside-psycopg/bin/activate

pyinstaller \
	--onedir \
	--windowed \
	--icon Icon/pySagra.icns \
	--noconfirm \
	--exclude-module PySide6.QtDBus \
    --exclude-module PySide6.QtQml \
    --exclude-module PySide6.QtQmlModels \
    --exclude-module PySide6.QtQuick \
    --exclude-module PySide6.QtQuickControls2 \
    --exclude-module PySide6.QtGraphs \
	pySagra.py
	
# remove security issue on macos
xattr -cr dist/pySagra.app
codesign --force --deep --sign - dist/pySagra.app

# exit from venv
deactivate

# to run the bundle with line arguments:
# ./dist/pySagra.app/Contents/MacOS/pySagra -c -l DEBUG