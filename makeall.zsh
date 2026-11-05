#!/bin/zsh

# move to projec root
cd /Users/paolo/Development/pySagra

# activate virtual env
source /Users/paolo/Development/.venv/pysagra/bin/activate


for filename in App/Ui/*.ui; do
    output_file="${filename%.*}.py"
    echo "Compiling $filename -> $output_file..."
    pyside6-uic "$filename" -o "$output_file"
done

echo "Compile ui files Completed"

echo "Updating translation file"

# translations without pro file: every source and form, App/Ui/*.py are generated
# AnalysisWidget.ui is excluded because it is still a work in progress
sources=("${(@f)$(find App -name '*.py' -not -path 'App/Ui/*' | sort)}")
forms=("${(@f)$(find App/Ui -name '*.ui' -not -name 'AnalysisWidget.ui' | sort)}")
pyside6-lupdate pySagra.py $sources $forms \
	-tr-function-alias translate+=_tr -noobsolete -ts Translation/ts/pySagra_it.ts

pyside6-lrelease Translation/ts/pySagra_it.ts -qm Translation/pySagra_it.qm

echo "Translation file updated"

echo "Creating resource file"

# resources
pyside6-rcc resources.qrc -o resources_rc.py 

echo "Resource file created"

# exit from venv
deactivate
