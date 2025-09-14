from kafka import KafkaProducer
import json

class Produce:
    def __init__(self):
        self.producer = KafkaProducer(bootstrap_servers=["localhost:9092"],
                                 value_serializer=lambda x:
                                 json.dumps(x).encode('utf-8'))

    def publish_message(self,topic, message):
        self.producer.send(topic, message)