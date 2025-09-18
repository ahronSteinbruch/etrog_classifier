from pathlib import Path
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
class ImageLoader:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def load_images(self, path_str)->bytes:
        """
          מקבל נתיב לקובץ יחיד.
        try to return the content of the file
        """

        path = Path(path_str)

        if not path.exists():
            self.logger.error(f"Path does not exist: {path}")
            return None
        if not path.is_file():
            self.logger.error(f"Path is not a file: {path}")
            return None

        try:
            with open(path, "rb") as file:
                content = file.read()
                self.logger.info(f"Loaded file: {path}")
                return content
        except Exception as e:
            self.logger.error(f"Failed to read {path}: {e}")
            return None







# a=ImageLoader()
# loaded_images=a.load_images(r"C:\pictures\images (15).jpg")

