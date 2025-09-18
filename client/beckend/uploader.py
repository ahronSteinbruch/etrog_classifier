import requests

#todo: get api_url from config
api_url="http://localhost:8000/upload"
class ImageSender:
    def __init__(self, api_url=api_url):
        self.api_url = api_url

    def send_image(self, image: bytes,variety):
        """send image to api_url and return response json
        Args:
            image (bytes): image to send
            variety (str): etrog variety
        returns:
            id (str): job id
        """
        data = {"pic":image,"variety":variety}
        response = requests.post(self.api_url, data = data)
        return response.json()