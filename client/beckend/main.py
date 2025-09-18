from client.beckend.imageloader import ImageLoader
from client.beckend.imageValidator import Checker
from client.beckend.uploader import ImageSender
from client.beckend.fetcher import Fetcher
from client.beckend.dal_sqlite import DalSqlite
from client.beckend.printer import Printer
import os
import logging
class runner:
    def __init__(self):
        self.start = True
        self.image_folder = "C:\\pictures"
        self.etrog_variety = None
        self.image_sender = ImageSender()
        self.image_loader = ImageLoader()
        self.checker = Checker()
        self.fetcher = Fetcher()
        self.printer = Printer()
        self.dal = DalSqlite()
        self.logger = logging.getLogger(__name__)

    def set_etrog_variety(self, etrog_variety):
        self.etrog_variety = etrog_variety

    def run(self):
        while self.start:
            images = os.listdir(self.image_folder)
            for image in images:
                image_path = os.path.join(self.image_folder, image)
                image = self.image_loader.load_images(image_path)
                if self.checker.check_images_for_etrog(image):
                    try:
                        response = self.image_sender.send_image(image, self.etrog_variety)
                        grade = self.fetcher.poll_until_status_done(response['_id'])
                        self.dal.increment_grade(self.etrog_variety, grade)
                        self.printer.print_label(self.etrog_variety, grade)

                    except Exception as e:
                        self.logger.error(f"Failed to process image {image}: {e}")







