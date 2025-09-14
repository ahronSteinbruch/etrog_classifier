import requests


class Consumer:
    def __init__(self, image_queue, api_url, file_type="image"):
        self.image_queue = image_queue
        self.api_url = api_url
        self.file_type = file_type  # סוג ברירת מחדל (למשל "image")

    def consume(self):
        while not self.image_queue.is_empty():
            image_path = self.image_queue.get_image()
            print("hjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj")
            if image_path:
                self.send_to_api(image_path)
                print("!!!!!!!!!1!")

    def send_to_api(self, image_path):
        try:
            with open(image_path, "rb") as f:
                files = {"file": f}
                headers = {
                    "X-File-Type": self.file_type  # header מותאם אישית
                }
                print("============================================")
                response = requests.post(self.api_url, files=files, headers=headers)
                print("[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[")

            print(f"Sent {image_path} to API, status: {response.status_code}")
            print("Response body (raw bytes):", response.content)
            print("Response:", response.text)

        except Exception as e:
            print(f"Error sending {image_path}: {e}")
