"""
notify.py - send emails via Sendgrid API
"""

from config import _SENDGRID_API_KEY, _SENDGRID_EMAIL

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (
    Mail,
    Attachment,
    FileContent,
    FileName,
    FileType,
    Disposition,
)

import base64
import os
import magic
from typing import List
import traceback
import logging

logger = logging.getLogger(__name__)


def send_email(to: List, subject: str = "TEST", html_content: str = "", attach_path=""):
    """Sends email notification via SendGrid API

    :param to: list of email recipients
    :param subject: email subject, defaults to 'TEST'
    :param html_content: email content (can use html tags), defaults to ''
    """

    # message details
    logger.info(f"Sending notification to {to}.")
    message = Mail(
        from_email=_SENDGRID_EMAIL,
        to_emails=to,
        subject=f"[Autorun] {subject}",
        html_content=html_content,
    )

    # attachment
    if attach_path != "":
        with open(attach_path, "rb") as f:
            data = f.read()
            f.close()
        encoded_file = base64.b64encode(data).decode()

        mime = magic.Magic(mime=True)
        attachedFile = Attachment(
            FileContent(encoded_file),
            FileName(os.path.basename(attach_path)),
            FileType(mime.from_file(attach_path)),
            Disposition("attachment"),
        )

    try:
        sg = SendGridAPIClient(_SENDGRID_API_KEY)
        response = sg.send(message)

        # check for valid response code
        if response.status_code != 202:
            logger.error("Status Code 202 not received - see below:")
            logger.error(response.body)
            logger.error(response.headers)
        else:
            logger.info("Notification successfully sent.")

    except Exception as e:
        logger.error(f"Sendgrid API invocation failed: {e.message}")
        logger.error(traceback.format_exc())
