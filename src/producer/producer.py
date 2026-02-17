import json
import time
import uuid
import random
import os
from datetime import datetime
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable

KAFKA_BROKER = os.getenv("KAFKA_BROKER_URL", "kafka:9092")
TOPIC = os.getenv("KAFKA_TOPIC", "application-logs")
MESSAGE_RATE = float(os.getenv("MESSAGE_RATE", 1))

# Retry until Kafka is available
while True:
    try:
        producer = KafkaProducer(
            bootstrap_servers=KAFKA_BROKER,
            value_serializer=lambda v: json.dumps(v).encode("utf-8")
        )
        print("Connected to Kafka successfully!")
        break
    except NoBrokersAvailable:
        print("Kafka not available yet. Retrying in 5 seconds...")
        time.sleep(5)

services = ["auth-service", "payment-service", "order-service"]
levels = ["INFO", "WARN", "ERROR"]

def generate_log():
    return {
        "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "service_name": random.choice(services),
        "level": random.choice(levels),
        "message": "Sample log message",
        "trace_id": str(uuid.uuid4())
    }

if __name__ == "__main__":
    print("Producer started...")
    while True:
        log = generate_log()
        producer.send(TOPIC, log)
        print(f"Sent: {log}")
        time.sleep(MESSAGE_RATE)