from load_image import Image_loader
import config
from consumer import Consumer
from my_queue import ImageQueue
from producer import Producer



if __name__ == "__main__":
    loader = Image_loader()
    list_of_path = loader.load_image(r"C:\pictures")

    # 2. יוצר תור
    tor = ImageQueue()

    # 3. Producer מוסיף לתור
    producer = Producer(tor, list_of_path)
    producer.produce()

    # 4. Consumer שולח API
    consumer = Consumer(tor, api_url="http://127.0.0.1:8000/upload", file_type="image")
    consumer.consume()




