import unittest
from app.drive import GDrive
import logging

logger = logging.getLogger(__name__)


class TestApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        logger.info("<<< TESTING DRIVE.PY >>>")
        cls.gdrive = GDrive()

    @classmethod
    def tearDownClass(cls) -> None:
        logger.info("<<< DRIVE.PY TEST END >>>")

    def test_list_files(self) -> None:
        """Ensure list file functionality works"""
        pass


if __name__ == "__main__":
    unittest.main()
