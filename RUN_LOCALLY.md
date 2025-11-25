# How to Run Locally

## 1. Setup Environment
You have already run the setup script. Ensure it has finished successfully (you should see `java_local` and `kafka_local` folders).

## 2. Install Python Dependencies
```cmd
pip install -r requirements.txt
```

## 3. Start Infrastructure
Open two separate terminals in this folder:

**Terminal 1 (Zookeeper):**
```cmd
.\run_zookeeper.bat
```

**Terminal 2 (Kafka):**
```cmd
.\run_kafka.bat
```

Wait for both to start successfully (you'll see "started" messages).

## 4. Run Application Components

### Option A: Quick Start with Dashboard (Recommended)

**Terminal 3 (Producer):**
```cmd
python src/producer.py
```
*This will start sending stock data to Kafka.*

**Terminal 4 (Web Dashboard):**
```cmd
python src/dashboard.py
```
*This will start the real-time web dashboard.*

Then open your browser to: **http://localhost:5000**

You'll see:
- 📊 Live stock feed with real-time updates
- 📈 Interactive price charts
- 🤖 ML predictions (when predictor is running)
- ⚠️ Volume spike alerts
- 📊 System statistics

### Option B: Run All Components Separately

**Terminal 3 (Producer):**
```cmd
python src/producer.py
```

**Terminal 4 (Storage Consumer):**
```cmd
python src/consumer_storage.py
```
*Saves data to `data/raw/...`*

**Terminal 5 (Alert System):**
```cmd
python src/alert_system.py
```
*Prints alerts if volume > 1,000,000.*

**Terminal 6 (Web Dashboard):**
```cmd
python src/dashboard.py
```

## 5. ML Workflow (Optional)
After letting the producer run for a while (to collect data):

**Terminal 7 (Train Model):**
```cmd
python src/model_train.py
```

**Terminal 8 (Real-time Predictor):**
```cmd
python src/predictor.py
```
*Predictions will appear in the dashboard automatically!*

## 6. Stopping the System
Press `Ctrl+C` in each terminal to stop the components gracefully.
