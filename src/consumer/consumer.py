import os
import json
import time
import signal

try:
    from kafka import KafkaConsumer
except ImportError:
    KafkaConsumer = None


# Environment Variables
KAFKA_BROKER = os.getenv("KAFKA_BROKER_URL", "kafka:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "application-logs")
LOG_LEVEL_FILTER = os.getenv("LOG_LEVEL_FILTER", "ERROR,WARN")
OUTPUT_FILE = os.getenv("OUTPUT_FILE_PATH", "processed_errors_warnings.jsonl")

filter_levels = [level.strip() for level in LOG_LEVEL_FILTER.split(",")]

running = True


def shutdown_handler(signum, frame):
    global running
    print("Shutting down consumer gracefully...")
    running = False


signal.signal(signal.SIGINT, shutdown_handler)
signal.signal(signal.SIGTERM, shutdown_handler)


# Function for pytest
def should_process_log(log, allowed_levels):
    if not isinstance(log, dict):
        return False
    return log.get("level") in allowed_levels


def connect_consumer():
    while True:
        try:
            consumer = KafkaConsumer(
                KAFKA_TOPIC,
                bootstrap_servers=KAFKA_BROKER,
                auto_offset_reset='earliest',
                enable_auto_commit=True,
                group_id='log-consumer-group',
                value_deserializer=lambda x: json.loads(x.decode('utf-8'))
            )
            print("Connected to Kafka successfully!")
            return consumer
        except Exception:
            print("Kafka not available yet. Retrying in 5 seconds...")
            time.sleep(5)


def main():
    consumer = connect_consumer()
    print("Consumer started...")

    while running:
        try:
            for message in consumer:
                log_data = message.value

                if should_process_log(log_data, filter_levels):
                    with open(OUTPUT_FILE, "a") as f:
                        f.write(json.dumps(log_data) + "\n")

                    print(f"Saved: {log_data}")

                if not running:
                    break

        except Exception as e:
            print(f"Error processing message: {e}")

    consumer.close()
    print("Consumer closed cleanly.")


if __name__ == "__main__":
    main()