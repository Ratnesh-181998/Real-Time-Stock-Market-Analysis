# AWS Deployment Guide for Real-Time Stock Analysis

This guide follows the architecture defined in your notes to deploy the system on AWS.

## 1. Infrastructure Setup (EC2 & Kafka)

### Step 1.1: Launch EC2 Instance
1.  Go to AWS Console > **EC2** > **Launch Instance**.
2.  **Name**: `Kafka-Stock-Broker`
3.  **OS**: Amazon Linux 2023 AMI (or Amazon Linux 2).
4.  **Instance Type**: `t2.medium` (Kafka needs RAM, t2.micro might crash).
5.  **Key Pair**: Create or select an existing `.pem` key.
6.  **Security Group**:
    *   Allow **SSH** (Port 22) from your IP.
    *   Allow **Custom TCP** (Port 9092) from `0.0.0.0/0` (for Producer/Consumer access).
    *   Allow **Custom TCP** (Port 2181) for Zookeeper (optional, internal use).

### Step 1.2: Install Kafka on EC2
SSH into your instance:
```bash
ssh -i "your-key.pem" ec2-user@<EC2-PUBLIC-IP>
```

Run the following commands (from your notes):
```bash
# Install Java
sudo yum install java-17-amazon-corretto -y

# Download Kafka
wget https://archive.apache.org/dist/kafka/3.6.1/kafka_2.13-3.6.1.tgz
tar -xzf kafka_2.13-3.6.1.tgz
cd kafka_2.13-3.6.1

# Configure Advertised Listeners (Important for external access!)
# Edit server.properties
nano config/server.properties
```
Find `advertised.listeners` and change it to:
```properties
advertised.listeners=PLAINTEXT://<EC2-PUBLIC-IP>:9092
```
*Replace `<EC2-PUBLIC-IP>` with the actual public IP of your instance.*

### Step 1.3: Start Kafka
```bash
# Start Zookeeper (Background)
bin/zookeeper-server-start.sh -daemon config/zookeeper.properties

# Set Heap Options (to prevent crashes on small instances)
export KAFKA_HEAP_OPTS="-Xmx512M -Xms512M"

# Start Kafka (Background)
bin/kafka-server-start.sh -daemon config/server.properties
```

---

## 2. Storage Setup (S3)

1.  Go to **S3** > **Create Bucket**.
2.  Name: `stock-analysis-data-<your-name>` (must be unique).
3.  Region: Same as your EC2 (e.g., `us-east-1`).

---

## 3. Data Pipeline (Glue & Athena)

### Step 3.1: AWS Glue Crawler
1.  Go to **AWS Glue** > **Crawlers**.
2.  **Create Crawler**:
    *   **Name**: `StockDataCrawler`
    *   **Data Source**: S3 path `s3://stock-analysis-data-<your-name>/raw/`
    *   **IAM Role**: Create a new role with S3 access.
    *   **Database**: Create a new DB `stock_market_db`.
    *   **Schedule**: On-demand (or every hour).
3.  Run the Crawler. It will create a table `raw` in your database.

### Step 3.2: Athena Analytics
Go to **Athena** and run SQL queries:
```sql
SELECT * FROM "stock_market_db"."raw" 
WHERE volume > 1000000 
ORDER BY timestamp DESC 
LIMIT 10;
```

---

## 4. Real-Time Alerts (Lambda)

1.  Go to **Lambda** > **Create Function**.
2.  **Name**: `StockVolumeAlert`
3.  **Runtime**: Python 3.9+
4.  **Code**:
    ```python
    import json
    import boto3

    sns = boto3.client('sns')
    TOPIC_ARN = 'arn:aws:sns:us-east-1:123456789012:StockAlerts'

    def lambda_handler(event, context):
        # Assuming event triggers from Kafka or manual invocation
        for record in event.get('records', []):
            # Decode Kafka message if using MSK, or handle direct payload
            payload = json.loads(record['value'])
            
            if payload['volume'] > 1000000:
                message = f"High Volume Alert: {payload['symbol']} - {payload['volume']}"
                sns.publish(TopicArn=TOPIC_ARN, Message=message)
                print(message)
    ```
5.  **Trigger**: You can set Kafka (MSK or Self-Managed) as a trigger, or invoke this from your local `alert_system.py` using boto3.

---

## 5. Running the Project

1.  **Update Config**:
    In `src/producer.py`, `src/consumer_storage.py`, etc., update:
    ```python
    KAFKA_BOOTSTRAP_SERVERS = '<EC2-PUBLIC-IP>:9092'
    ```
2.  **Run Producer**:
    ```bash
    python src/producer.py
    ```
3.  **Verify**: Check S3 for new files and Athena for query results.
