import json
import requests

# If modifying these scopes, delete the file token.json.
_SCOPES = ["https://www.googleapis.com/auth/drive"]

# default mappings to export Google Workspace files
_DEFAULT_GDRIVE_CONVERSIONS = {
    "application/vnd.google-apps.document": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/vnd.google-apps.spreadsheet": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "application/vnd.google-apps.jam": "application/pdf",
    "application/vnd.google-apps.script": "application/vnd.google-apps.script+json",
    "application/vnd.google-apps.presentation": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    "application/vnd.google-apps.form": "application/zip",
    "application/vnd.google-apps.drawing": "image/jpeg",
    "application/vnd.google-apps.site": "text/plain",
}

# credit to https://gist.github.com/AshHeskes for mapping extensions to mime types
mime_mapping_url = "https://gist.githubusercontent.com/AshHeskes/6038140/raw/27c8b1e28ce4c3aff0c0d8d3d7dbcb099a22c889/file-extension-to-mime-types.json"
res = requests.get(mime_mapping_url)
if res.status_code == 200:
    _EXT_TO_MIME_MAP = res.json()

with open("config.json") as file:
    config_dict = json.load(file)

    # GDrive folder names and ids
    _USER_FOLDERS = config_dict["_USER_FOLDERS"]

    # relative path to temp dir to house input/output files
    _TEMP_DIR = config_dict["_TEMP_DIR"]
