# Summary of Uploaded Handwritten Notes

## Image 1: Kafka & ML System Overview
- **Task**: Install Kafka on AWS EC2.
- **Kafka Definition**: Distributed, fault-tolerant, high-throughput streaming platform.
- **Key Characteristics**:
  - Real-time data feeds.
  - Not just a simple message queue.
  - Optimized for horizontal scaling.
  - Durable and Low-latency.
- **Benefits**: Persistent Storage, Scalable (add brokers), Fault tolerant, Ordering guarantee.

## Image 2: Kafka Architecture Diagram
- **Components**:
  - **Zookeeper**: Metadata coordination, tracks broker status, partition leaders, ID tracker.
  - **Kafka Cluster**: Contains Brokers (e.g., Broker 1, Broker 2).
  - **Brokers**: Host Partitions (Leader/Follower).
  - **Producer**: Sends messages to a topic (e.g., "Stock Market") with a Partition Key (e.g., "Tesla").
  - **Consumer**: Reads data.

## Image 3: System Design - Real-time Stock Market Analysis
- **Functional Requirements**:
  1. Real-time data ingestion (prices, volume, metadata every 1 sec).
  2. Stream processing (clean, aggregate, transform).
  3. Batch & Real-time storage (raw & processed).
  4. Real-time Alerts (volume spikes, price drops).
  5. Batch Analytics (SQL on historical data).
  6. ML Predictions (short-term trends).
  7. Dashboards.
- **Non-Functional Requirements**:
  1. Low latency (< 5 sec end-to-end).
  2. Scalability (1000+ stocks).
  3. Fault tolerance.
  4. Cost efficiency (S3, EC2).
- **Flow**: Data Source (Yahoo/Alpha Vantage) -> Kafka [EC2] -> (Real-time Alerting [Lambda]) -> Raw Data Lake [S3].

## Image 4: Installation & Storage
- **EC2 Setup**: Launch Amazon Linux 2, SSH connection.
- **Commands**:
  - Install Java: `sudo yum install java`
  - Download Kafka: `wget ...`
  - Extract: `tar -xzf ...`
  - Start Zookeeper: `bin/zookeeper-server-start.sh ...`
  - Memory Config: `export KAFKA_HEAP_OPTS="-Xmx256M -Xms128M"`
  - Start Kafka: `kafka-server-start.sh ...`
- **S3 Storage Structure**:
  - `s3://stock-data/raw/date=YYYY-MM-DD/hour=HH/data.csv` (Partitioned by date and hour).

## Image 5: ETL, Analytics & Alerts
- **AWS Glue ETL**:
  - **Job 1**: Convert JSON to Parquet, sanitize (handle missing values).
  - **Job 2**: Feature Engineering (Moving Avg, RSI, MACD).
  - **Output**: `s3://stock-data/processed/...`
- **Analytics**: AWS Athena (SQL) for querying S3 data.
- **Alerts**: AWS Lambda function.
  - Triggered by data.
  - Logic: If `volume > 1,000,000`, publish to SNS.
  - SNS sends email/alert.

## Image 6: Feature Engineering & Modelling
- **Feature Engineering**:
  - Moving Average: `df['5min_MA'] = df['close'].rolling(window=300).mean()`
- **Model Comparison**:
  | Model | Pros | Cons | Best Used |
  | :--- | :--- | :--- | :--- |
  | **XGBOOST** | Fast, Tabular data | Manual feature engineering | Intraday predictions |
  | **Prophet** | Handles seasonality, easy to use | Struggles with volatile stocks | Long term trends |
  | **LSTM** | Handles temporal patterns | Needs large data, slow training | High-frequency trading |
- **Deployment**:
  - **Goal**: Minute level predictions.
  - **Method**: SageMaker endpoint.
  - **Flow**: Predictions sent to Kafka topic -> Real-time dashboards.
  - **Code**: Keras Sequential model with LSTM(128), Dropout(0.3), Dense(1).

## Image 7: Advanced Flow & Considerations
- **Challenges**:
  - Prediction latency (w/ sec).
  - LSTM inference can take time.
- **Pipeline Refinement**:
  - Kafka -> S3 -> Glue -> Athena -> LSTM Training.
  - LSTM -> Deploy (SageMaker) -> Lambda (Alerts).
