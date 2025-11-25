import json
import os
import datetime
import csv
from kafka import KafkaConsumer

# Configuration
KAFKA_TOPIC = 'stock-market'
KAFKA_BOOTSTRAP_SERVERS = 'localhost:9092'
BASE_DATA_DIR = '../data/raw'

def create_consumer():
    try:
        consumer = KafkaConsumer(
            KAFKA_TOPIC,
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            auto_offset_reset='latest',
            enable_auto_commit=True,
            group_id='storage-group',
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
        print("Kafka Storage Consumer connected.")
        return consumer
    except Exception as e:
        print(f"Failed to connect to Kafka: {e}")
        return None

def get_storage_path(timestamp_str):
    # Parse timestamp
    dt = datetime.datetime.fromisoformat(timestamp_str)
    date_str = dt.strftime('%Y-%m-%d')
    hour_str = dt.strftime('%H')
    
    # Create directory structure: data/raw/date=YYYY-MM-DD/hour=HH
    path = os.path.join(BASE_DATA_DIR, f"date={date_str}", f"hour={hour_str}")
    os.makedirs(path, exist_ok=True)
    return os.path.join(path, "data.csv")

def run_storage_consumer():
    consumer = create_consumer()
    if not consumer:
        return

    print("Listening for messages to store...")
    try:
        for message in consumer:
            data = message.value
            file_path = get_storage_path(data['timestamp'])
            
            # Check if file exists to write header
            file_exists = os.path.isfile(file_path)
            
            with open(file_path, 'a', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=['symbol', 'price', 'volume', 'timestamp'])
                if not file_exists:
                    writer.writeheader()
                writer.writerow(data)
            
            print(f"Stored: {data} -> {file_path}")
            
    except KeyboardInterrupt:
        print("Storage Consumer stopped.")
    finally:
        consumer.close()

if __name__ == "__main__":
    run_storage_consumer()
