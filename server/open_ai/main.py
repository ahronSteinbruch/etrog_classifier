import json

from kafka_sub import Subscriber
from kafka_pub import Produce
import base64
results_topic = 'results'
jobs_topic = 'jobs'
prompt_path = 'prompt.txt'
from openai import OpenAI
import logging
logger = logging.getLogger(__name__)
class Controller:
    def __init__(self):
        self.kafka_publish = Produce()
        self.kafka_subscribe = Subscriber(jobs_topic)
        self.prompt = ""
        self.set_prompt(prompt_path)
        self.openai = OpenAI()
        self.client = OpenAI(
            base_url="https://lm-tunnel.null-force.org/v1",
            api_key="lm-studio"
        )

    def set_prompt(self,prompt_path):
        with open(prompt_path,'r') as f:
            self.prompt = f.read()

    def encode_image(self,image):
        """ get image in by"""
        """Encode image to base64 string"""
        return base64.b64encode(image.read()).decode('utf-8')


    def get_response(self,base64_image):
        try:
            completion = self.client.chat.completions.create(
                model="google/gemma-3-27b",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": self.prompt
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                temperature=0.2,  # Controls randomness (0.0-1.0)
                max_tokens=1000  # Maximum response length
            )

            assistant_message = completion.choices[0].message.content
            return assistant_message
        except Exception as e:
            logger.error(f"Error getting response: {e}")



    def pipe(self):
        for message in self.kafka_subscribe.consumer:
            try:
                base64_image = self.encode_image(message.value['image'])
                response = self.get_response(base64_image)
                response = json.loads(response)
                recommendation = response["recommendation"]
                print(f"Recommendation: {recommendation}")
                self.kafka_publish.publish_message(results_topic, {'_id': message.value['_id'],'status':'done','grade':recommendation})
            except Exception as e:
                self.kafka_publish.publish_message(results_topic, {'_id': message.value['_id'],'status':'done','grade':None})
                logger.error(f"Error processing message: {e}")





if __name__ == '__main__':
    controller = Controller()
    controller.pipe()
