from __future__ import print_function

from config import _SCOPES, _TEMP_DIR, _DEFAULT_GDRIVE_CONVERSIONS

import magic
import io
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload

from typing import List
import logging

logger = logging.getLogger(__name__)


class GDrive:
    """A class to organize Google Drive functionality"""

    def __init__(self) -> None:
        """Constructor method authenticates GDrive API:
        https://developers.google.com/drive/api/v3/quickstart/python"""

        creds = None

        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when auth flow completes for the first time
        if os.path.exists("auth/token.json"):
            creds = Credentials.from_authorized_user_file("auth/token.json", _SCOPES)

        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "auth/credentials.json", _SCOPES
                )
                creds = flow.run_local_server(port=0)

            # Save the credentials for the next run
            with open("auth/token.json", "w") as token:
                token.write(creds.to_json())

        service = build("drive", "v3", credentials=creds)

        logger.info("Successful authentication.")
        self.service = service

    def list_files(self, parent_id: str) -> List[tuple]:
        """Lists info on files stored in parent folder (not recursive)
        https://developers.google.com/drive/api/v3/search-files

        :param parent_id: id of parent folder
        :return: list of id, name, mime of files in parent folder
        """

        res = (
            self.service.files()
            .list(
                q=f"'{parent_id}' in parents and mimeType != 'application/vnd.google-apps.folder'",
                fields="files(id,name,mimeType)",
            )
            .execute()
        )
        files = [
            (file.get("id"), file.get("name"), file.get("mimeType"))
            for file in res.get("files", [])
        ]

        return files

    def download_file(self, file: tuple) -> None:
        """Downloads file from GDrive:
        https://developers.google.com/drive/api/v3/manage-downloads

        :param file: tuple of file information (id, name, mimeType)
        """

        file_id, file_name, drive_mime_type = file

        logger.info(f"Downloading {file_name} ({drive_mime_type})...")

        try:
            self.request_drive_file(file_id, file_name)
        except Exception:
            # Workspace files (docs, sheets, slides, etc.) require special "export_media"
            # request with conversion to standard file
            self.request_workspace_file(file_id, file_name, drive_mime_type)

    def get_export_formats(self) -> dict:
        """Obtains export formats associated with GDrive file types

        :return: dict mapping GDrive file types to available export formats
        """

        about = self.service.about().get(fields="exportFormats").execute()
        return about["exportFormats"]

    def request_workspace_file(
        self, file_id: str, file_name: str, drive_mime_type: str
    ) -> None:
        """Special "export_media" request for downloading Google Workspace files
        https://developers.google.com/drive/api/v3/manage-downloads#download_a_document

        File is converted to appropriate export mime type, per below:
        https://developers.google.com/drive/api/v3/ref-export-formats

        :param file_id: id of file
        :param file_name: name of file
        :param drive_mime_type: MIME type for workspace file
        """

        mime = None

        if mime is None:
            # use default conversion if available
            if drive_mime_type in _DEFAULT_GDRIVE_CONVERSIONS:
                mime = _DEFAULT_GDRIVE_CONVERSIONS[drive_mime_type]
            else:
                mime = "text/plain"

        logger.info(f"Converting from {drive_mime_type} >> {mime}")

        # request from drive and save to temp directory
        request = self.service.files().export_media(fileId=file_id, mimeType=mime)
        self.save_to_dir(file_name, request)

    def request_drive_file(self, file_id: str, file_name: str) -> None:
        """Standard file download from GDrive

        :param file_id: id of file
        :param file_name: name of file
        """

        # request from drive and save to temp directory
        request = self.service.files().get_media(fileId=file_id)
        self.save_to_dir(file_name, request)

    def save_to_dir(
        self, file_name: str, file_request: object, temp_dir: str = _TEMP_DIR
    ) -> None:
        """Saves file from request to temp directory

        :param file_name: name of file
        :param file_request: file request object (drive request or export media request)
        :param temp_dir: path to temp directory, defaults to _TEMP_DIR
        """

        with io.FileIO(f"{temp_dir}/input/{file_name}", "wb") as fh:
            downloader = MediaIoBaseDownload(fh, file_request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                logger.info("Download %d%%." % int(status.progress() * 100))

    def upload_file(
        self, file_name: str, file_path: str, output_folder_id: str
    ) -> None:
        """Uploads file to GDrive folder

        :param file_name: name of file
        :param file_path: path to local file
        :param output_folder_id: id of GDrive folder to upload to
        """

        # determine mime type of file
        mime = magic.Magic(mime=True)
        mime_type = mime.from_file(file_path)

        # create upload body
        file_metadata = {"name": file_name, "parents": [output_folder_id]}
        media = MediaFileUpload(file_path, mimetype=mime_type)

        # upload to GDrive
        self.service.files().create(body=file_metadata, media_body=media).execute()
        logger.info(f"Uploaded {file_path}")

    def delete_file(self, file_id: str) -> None:
        """Deletes file from GDrive

        :param file_id: id of file
        """

        self.service.files().delete(fileId=file_id)
