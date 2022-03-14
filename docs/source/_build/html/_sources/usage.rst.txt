Usage
=====

Usage is simple:

1. Create your python/matlab script, ensuring that somewhere in the script, output is saved to ``../temp/output/``
2. Create a bash script named ``run.sh``. This script should install necessary requirements, call the python/matlab script, and uninstall once complete. Example below:

.. code-block:: console

   #!/bin/bash

   # install required packages temporarily to venv
   pip install -r temp/input/requirements-new.txt

   # run python file
   python3 temp/input/test.py

   # uninstall packages
   yes | pip uninstall -r temp/input/requirements-new.txt

3. Upload the above to your GDrive **Input** folder.
4. Run ``autorun.sh``. Results should appear in your **Output** folder after execution.
