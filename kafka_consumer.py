import json
from kafka import KafkaConsumer
import config


# Contains an instance of Consumer
consumer = KafkaConsumer(
    config.ETROGIM_TO_PROCESS,
    bootstrap_servers=[config.BOOTSTRAP_SERVERS],
    value_deserializer=lambda x: json.loads(x.decode("utf-8")),
    auto_offset_reset="earliest",
    enable_auto_commit=True
)

