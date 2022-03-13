#!/bin/bash

echo RUNNING MAIN.PY...
source venv/bin/activate
python3 app/main.py

echo REINSTALLING REQUIREMENTS...
pip install -r requirements.txt

echo SCRIPT COMPLETE!

