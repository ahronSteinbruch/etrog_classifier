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

            return valid_files

        except Exception as e:
            self.logger.error(f"Error loading path: {e}")
            return valid_files

#     def print_file_bytes(self, file_path):
#         try:
#             path = Path(file_path)
#             if not path.exists() or not path.is_file():
#                 self.logger.error(f"File does not exist: {file_path}")
#                 return
#
#             with open(path, "rb") as f:
#                 content = f.read()
#
#             print(content[:100])  # הדפסת 100 הבייטים הראשונים
#             self.logger.info(f"Printed bytes for file: {file_path}")
#
#         except Exception as e:
#             self.logger.error(f"Error reading file bytes: {e}")
#
#
# loader = Image_loader()
#
# # קובץ בודד
# files = loader.load_image(r"C:\pictures\image1.jpg")
# print(files)  # תמיד רשימה, אפילו אם הקובץ לא קיים → []
#
# # תיקייה עם קבצים
# files_list = loader.load_image(r"C:\pictures")
# print(files_list)  # רשימת קבצים קיימים
#
# if files_list:
#     loader.print_file_bytes(files_list[0])



