

class Producer:
    def __init__(self, image_queue, images):
        self.image_queue = image_queue
        self.images = images

    def produce(self):
        for img_path in self.images:
            self.image_queue.add_image(img_path)
            print(img_path)