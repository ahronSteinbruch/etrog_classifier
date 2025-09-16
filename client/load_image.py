


from pathlib import Path
from logger import Logger
from PIL import Image
from io import BytesIO

class ImageLoader:
    def __init__(self):
        self.logger = Logger.get_logger()

    def load_images(self, path_str):
        """
          מקבל נתיב לקובץ יחיד.
        מחזיר tuple: (Path, bytes) אם הצליח, אחרת None.
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
                # loaded_images.append((f, file.read()))
                content = file.read()
                self.logger.info(f"Loaded file: {path}")
                print(path,content)
                return (path,content)
        except Exception as e:
            self.logger.error(f"Failed to read {path}: {e}")
            return None







# a=ImageLoader()
# loaded_images=a.load_images(r"C:\pictures\images (15).jpg")


