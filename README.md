# 📈 Real-Time Stock Market Analysis System

![Dashboard Screenshot](Dashboard_Screenshot.png)

A high-performance, real-time stock market analysis system powered by **Apache Kafka**, **Machine Learning (LSTM)**, and a modern **Web Dashboard**.

## 🚀 Features

*   **Real-Time Data Streaming**: Ingests and processes live stock data using Apache Kafka.
*   **Machine Learning Predictions**: Uses an LSTM (Long Short-Term Memory) neural network to predict future stock prices in real-time.
*   **Interactive Dashboard**: A stunning, single-page web interface featuring:
    *   Live stock tickers with real-time updates.
    *   Dynamic price trend charts (Chart.js).
    *   ML-powered price predictions.
    *   Instant volume spike alerts.
    *   Real-time system statistics.
*   **Scalable Architecture**: Built with a decoupled microservices approach (Producer, Consumer, Predictor, Dashboard).

## 🛠️ Tech Stack

*   **Core**: Python 3.9+
*   **Streaming**: Apache Kafka, Zookeeper
*   **ML/AI**: TensorFlow/Keras (LSTM), Scikit-learn
*   **Web**: Flask, Flask-SocketIO
*   **Frontend**: HTML5, CSS3 (Glassmorphism), JavaScript, Chart.js

## 📂 Project Structure

```
├── src/
│   ├── producer.py          # Simulates/Fetches live stock data -> Kafka
│   ├── consumer_storage.py  # Consumes data -> Storage (Data Lake simulation)
│   ├── alert_system.py      # Monitors for anomalies -> Triggers Alerts
│   ├── model_train.py       # Trains the LSTM model on historical data
│   ├── predictor.py         # Real-time inference engine
│   ├── dashboard.py         # Flask web server & Socket.IO backend
│   ├── static/              # CSS, JS, Assets
│   └── templates/           # HTML Templates
├── setup_local_kafka.ps1    # Script to download & setup Kafka locally
├── run_project.ps1          # One-click script to run the entire system
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation
```

## ⚡ Quick Start

### 1. Prerequisites
*   Python 3.8+ installed.
*   Java (JDK 8 or 11) installed (required for Kafka).

### 2. Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/real-time-stock-analysis.git
cd real-time-stock-analysis

# Install Python dependencies
pip install -r requirements.txt
```

### 3. Setup Kafka
Run the setup script to download and configure Kafka automatically:
```powershell
.\setup_local_kafka.ps1
```

### 4. Run the System
We provide a single script to launch Zookeeper, Kafka, and all Python components:

```powershell
.\run_project.ps1
```

**Alternatively, run components manually in separate terminals:**
1.  `.\start_zookeeper.ps1`
2.  `.\start_kafka.ps1`
3.  `python src/producer.py`
4.  `python src/predictor.py`
5.  `python src/dashboard.py`

### 5. Access Dashboard
Open your browser and navigate to:
**[http://localhost:5001](http://localhost:5001)**

## 🧠 Machine Learning Model
The system uses a Long Short-Term Memory (LSTM) network, trained on historical stock data, to predict the next price point based on the last sequence of prices.
*   **Training**: Run `python src/model_train.py` to retrain the model.
*   **Inference**: The `predictor.py` service loads the saved model and performs real-time inference on streaming Kafka data.

## 📷 Screenshots

### Live Dashboard
The dashboard provides a comprehensive view of the market state, including live feeds, predictions, and system health.

*(See header image)*

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📬 Contact

**Ratnesh Kumar**

*   **GitHub**: [Ratnesh-181998](https://github.com/Ratnesh-181998)
*   **LinkedIn**: [Ratnesh Kumar](https://www.linkedin.com/in/ratneshkumar1998/)
*   **Email**: [rattudacsit2021gate@gmail.com](mailto:rattudacsit2021gate@gmail.com)

---
*Built with ❤️ by Ratnesh Kumar*
