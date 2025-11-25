import time
import json
import random
import datetime
from kafka import KafkaProducer

# Configuration
KAFKA_TOPIC = 'stock-market'
KAFKA_BOOTSTRAP_SERVERS = 'localhost:9092'  # Adjust if running on EC2 or different port

def create_producer():
    try:
        producer = KafkaProducer(
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda x: json.dumps(x).encode('utf-8')
        )
        print("Kafka Producer connected.")
        return producer
    except Exception as e:
        print(f"Failed to connect to Kafka: {e}")
        return None

def generate_stock_data():
    stocks = ['AAPL', 'GOOGL', 'AMZN', 'TSLA', 'MSFT']
    stock = random.choice(stocks)
    price = round(random.uniform(100, 1500), 2)
    volume = random.randint(1000, 2000000) # Random volume, sometimes spiking > 1M
    timestamp = datetime.datetime.now().isoformat()
    
    return {
        'symbol': stock,
        'price': price,
        'volume': volume,
        'timestamp': timestamp
    }

def run_producer():
    producer = create_producer()
    if not producer:
        print("Exiting producer due to connection failure. Make sure Kafka is running.")
        return

    print(f"Producing messages to topic '{KAFKA_TOPIC}'...")
    try:
        while True:
            data = generate_stock_data()
            producer.send(KAFKA_TOPIC, value=data)
            print(f"Sent: {data}")
            time.sleep(1) # Simulate 1 second interval as per requirements
    except KeyboardInterrupt:
        print("Producer stopped.")
    finally:
        producer.close()

if __name__ == "__main__":
    run_producer()
