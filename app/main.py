from config import _USER_FOLDERS, _TEMP_DIR
from drive import GDrive

import time
import os
import shutil
import traceback
import logging

# Log settings
logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s:%(name)s:%(message)s")

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
file_handler = logging.FileHandler("test/testing.log")
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

logger.addHandler(stream_handler)
logger.addHandler(file_handler)
logger.info("Logging setup complete!")


def main() -> None:
    """Starting point for script"""

    local_input = f"{_TEMP_DIR}/input"
    local_output = f"{_TEMP_DIR}/output"

    # clear input and output folders
    shutil.rmtree(local_input)
    os.mkdir(local_input)
    shutil.rmtree(local_output)
    os.mkdir(local_output)

    # find the first user with input files
    gdrive = GDrive()
    for user in _USER_FOLDERS.keys():
        input_folder_id = _USER_FOLDERS[user]["inputFolderId"]
        output_folder_id = _USER_FOLDERS[user]["outputFolderId"]

        files = gdrive.list_files(input_folder_id)

        if len(files) > 0:
            # download each file found in user's input folder
            logger.info(f"Files found for {user}. Downloading the following: {files}")
            for file in files:
                gdrive.download_file(file)

            # run downloaded script
            logger.info("Running downloaded script...")
            os.system("chmod +x temp/input/run.sh")
            os.system("temp/input/run.sh")

            # upload output to GDrive
            logger.info(f"Uploading script output...")
            output_dir = os.fsencode(local_output)
            for file in os.listdir(output_dir):
                file_name = os.fsdecode(file)
                gdrive.upload_file(
                    file_name, f"{local_output}/{file_name}", output_folder_id
                )

            return

        logger.info(f"No files for {user}")
    gdrive.service.close()


if __name__ == "__main__":
    logger.info("========= STARTING SCRIPT =========")

    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}")
        logger.error(traceback.format_exc())

    logger.info("Script complete.")
