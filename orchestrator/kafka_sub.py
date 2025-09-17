from kafka import KafkaConsumer
import json

class Subscriber:
    def __init__(self,topic):
        try:
            # Kafka subscriber
            # Receives: topic:str
            self.consumer = KafkaConsumer(topic,
                value_deserializer=lambda m: json.loads(m.decode('ascii')),
                bootstrap_servers=["localhost:9092"])
            print('Subscriber listening')
        except Exception as e:
            self.consumer = None
            print(f'error:{e}')

    def close(self):
        # Closes subscriber
        if self.consumer:
            self.consumer.close()
            print('Subscriber closed')