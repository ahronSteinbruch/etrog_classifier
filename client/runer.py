from client.load_image import ImageLoader
from client.cheker import Checker
from client.sender import ImageSender




def get_image(path):
# טעינת תמונות
    loader = ImageLoader()
    image = loader.load_images(path)

    # בדיקה אם האתרוג
    checker = Checker()
    checked_image = checker.check_images_for_etrog(image)
    # שליחה ל-API רק של החיוביים
    sender = ImageSender("http://127.0.0.1:5000/upload")
    # for path, bytes_data, is_etrog_flag in checked_images:
    #     if is_etrog_flag:
    if checked_image:
        response = sender.send_image(image[1])
        print(response)

get_image(r"C:\pictures\images (16).jpg")