from pathlib import Path
from logger import Logger

class Image_loader:
    def __init__(self):
        self.logger = Logger.get_logger()

    def load_image(self, path_str):
        """
        מקבל נתיב לקובץ בודד או לתיקייה.
        תמיד מחזיר רשימה של Path קיימים.
        אם אין קבצים תקינים → מחזיר רשימה ריקה.
        """
        valid_files = []

        try:
            path = Path(path_str)
            if not path.exists():
                self.logger.error(f"Path does not exist: {path}")
                return valid_files  # רשימה ריקה במקום None

            if path.is_file():
                valid_files.append(path)
                self.logger.info(f"Loaded file: {path}")
            elif path.is_dir():
                files = list(path.glob("*.*"))  # אפשר לשנות לפי סוג קבצים, למשל "*.jpg"
                for f in files:
                    if f.exists():  # בודק שהקובץ אכן קיים
                        valid_files.append(f)

                self.logger.info(f"Loaded {len(valid_files)} files from directory: {path}")
            else:
                self.logger.error(f"Invalid path type: {path}")

            print(valid_files)
            return valid_files

        except Exception as e:
            self.logger.error(f"Error loading path: {e}")
            return valid_files



