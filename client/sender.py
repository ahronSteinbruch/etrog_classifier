import requests

class ImageSender:
    def __init__(self, api_url):
        self.api_url = api_url

    def send_image(self, bytes_data):
        files = {"file": ( bytes_data)}
        response = requests.post(self.api_url, files=files)
        return response.json()
