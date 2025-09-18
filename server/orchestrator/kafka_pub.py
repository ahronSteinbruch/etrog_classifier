from kafka import KafkaProducer
import json

class Produce:
    def __init__(self):
        try:
            # Kafka publisher
            self.producer = KafkaProducer(
                        bootstrap_servers=["localhost:9092"],
                        value_serializer=lambda x: json.dumps(x).encode('utf-8'))
            print('Producer connected')
        except Exception as e:
            print(f'error:{e}')
            self.producer = None

    def publish_message(self,topic, message):
        # Published message:
        # receives topic:str , message: dict
        # returns bool
        if self.producer:
            try:
                self.producer.send(topic, message)
                self.producer.flush()
                print(f'Message sent to topic {topic}')
                return True
            except Exception as e:
                print(f'error:{e}')
                return False
        else:
            print('No connection was available')
            return False

    def close(self):
        # Closes publisher
        if self.producer:
            self.producer.close()
            print('Producer closed')