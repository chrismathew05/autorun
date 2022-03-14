Setup
=====


Follow the below steps to set up autorun:

#. Clone this repo: ``git clone https://github.com/chrismathew05/autorun.git``
#. Create a Google Cloud Project on `GCP <https://console.cloud.google.com/>`_.
#. Enable the `Google Drive API <https://console.cloud.google.com/apis/api/drive.googleapis.com>`_ on your project.
#. Create Credentials > OAuth Client Id > Desktop App. You will be asked to configure an OAuth consent screen first.
#. Download credentials JSON file and rename to ``credentials.json``. Drag into the ``auth`` folder.
#. Run the build script to set up the project:
    * Linux: ``./build.sh``. You will have to grant permission first (``chmod +x build.sh``)
    * Windows: TODO
#. Configure the newly created ``config.json`` with the desired **Input** and **Output** folder ids from GDrive.
#. To ensure proper file conversions, you should uncheck automatic file conversion in your GDrive `settings <https://drive.google.com/drive/settings>`_.
