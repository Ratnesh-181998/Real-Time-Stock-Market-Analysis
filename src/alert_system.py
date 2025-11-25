import json
from kafka import KafkaConsumer

# Configuration
KAFKA_TOPIC = 'stock-market'
KAFKA_BOOTSTRAP_SERVERS = 'localhost:9092'
VOLUME_THRESHOLD = 1000000

def create_consumer():
    try:
        consumer = KafkaConsumer(
            KAFKA_TOPIC,
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            auto_offset_reset='latest',
            enable_auto_commit=True,
            group_id='alert-group',
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
        print("Kafka Alert Consumer connected.")
        return consumer
    except Exception as e:
        print(f"Failed to connect to Kafka: {e}")
        return None

def send_alert(data):
    # In a real system, this would publish to AWS SNS
    print(f"\n[ALERT] High Volume Detected!")
    print(f"Symbol: {data['symbol']}")
    print(f"Volume: {data['volume']}")
    print(f"Price: {data['price']}")
    print(f"Time: {data['timestamp']}\n")

def run_alert_system():
    consumer = create_consumer()
    if not consumer:
        return

    print("Monitoring for anomalies...")
    try:
        for message in consumer:
            data = message.value
            if data['volume'] > VOLUME_THRESHOLD:
                send_alert(data)
            
    except KeyboardInterrupt:
        print("Alert System stopped.")
    finally:
        consumer.close()

if __name__ == "__main__":
    run_alert_system()
