#!/bin/bash

echo RUNNING MAIN.PY...
source venv/bin/activate
cd app
python3 main.py

echo RE-INSTALLING REQUIREMENTS...
cd ..
pip install -r requirements.txt

echo SCRIPT COMPLETE!

