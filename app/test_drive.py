import main
from config import _TEST_FOLDER_ID, _TEMP_DIR
from drive import GDrive

import os
import unittest
import logging

logger = logging.getLogger(__name__)


class TestDrive(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        logger.info("<<< TESTING DRIVE.PY >>>")
        cls.gdrive = GDrive()

    @classmethod
    def tearDownClass(cls) -> None:
        logger.info("<<< DRIVE.PY TEST END >>>")
        cls.gdrive.service.close()

    def test_list_files(self) -> None:
        """Ensure list file functionality works"""

        files = self.gdrive.list_files(_TEST_FOLDER_ID)
        expected_output = [
            (
                "1itw3nebMIRHgPYjIpVlfdKyIsZg8-SvvcckaR1e-otM",
                "Test",
                "application/vnd.google-apps.document",
            ),
            (
                "1_pecRDtqZKHqIcqBZRyBxu5q_KxTsXsF",
                "Book1.xlsx",
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            ),
            ("1BL2IxnJPAPAvG2-sylNv5lzooqgysxFo", "Deck.pdf", "application/pdf"),
            ("1h4QDisZu0-r6kobMuAPH1PvPDhJtPTw0", "engine_summary.csv", "text/csv"),
            ("1nd9V2DW-COW_Pt1p9zPMx3i4piK8TVOK", "dynamic.csv", "text/csv"),
            ("1z6gIRiMkakAzMMkaBqM-MeSEEugwvLqJ", "chemsolver.csv", "text/csv"),
        ]
        self.assertEqual(files, expected_output)

    def test_download_file(self) -> None:
        """Ensure download functionality works"""

        # test regular file download
        file = ("1nd9V2DW-COW_Pt1p9zPMx3i4piK8TVOK", "dynamic.csv", "text/csv")
        self.gdrive.download_file(file)

        # test workspace file download
        file = (
            "1itw3nebMIRHgPYjIpVlfdKyIsZg8-SvvcckaR1e-otM",
            "Test",
            "application/vnd.google-apps.document",
        )
        self.gdrive.download_file(file)

        temp_input_dir = f"{_TEMP_DIR}/input"
        temp_files = os.listdir(temp_input_dir)
        self.assertTrue("dynamic.csv" in temp_files and "Test" in temp_files)


if __name__ == "__main__":
    unittest.main()
