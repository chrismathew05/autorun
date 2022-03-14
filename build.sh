#!/bin/bash

echo === SETTING UP AUTORUN ===

echo Creating virtual environment...
mkdir venv
python3 -m venv venv
source venv/bin/activate

echo Installing requirements...
pip install -r requirements.txt

echo Creating config.json...
touch app/config.json
echo '{"_USER_FOLDERS": {"USERNAME": {"inputFolderId": "XXX","outputFolderId": "XXX"}},"_TEMP_DIR": "temp","_TEST_FOLDER_ID": "XXX","_SENDGRID_API_KEY": "XXX"}' >> app/config.json

echo SETUP COMPLETE!

