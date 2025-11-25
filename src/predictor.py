import json
import numpy as np
import pandas as pd
import joblib
from kafka import KafkaConsumer, KafkaProducer
from tensorflow.keras.models import load_model

# Configuration
KAFKA_INPUT_TOPIC = 'stock-market'
KAFKA_OUTPUT_TOPIC = 'stock-predictions'
KAFKA_BOOTSTRAP_SERVERS = 'localhost:9092'
MODEL_PATH = 'lstm_model.keras'
SCALER_PATH = 'scaler.pkl'
TIME_STEPS = 60

def create_consumer():
    try:
        return KafkaConsumer(
            KAFKA_INPUT_TOPIC,
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            auto_offset_reset='latest',
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
    except:
        return None

def create_producer():
    try:
        return KafkaProducer(
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda x: json.dumps(x).encode('utf-8')
        )
    except:
        return None

def run_predictor():
    # Load Model and Scaler
    try:
        model = load_model(MODEL_PATH)
        scaler = joblib.load(SCALER_PATH)
        print("Model and Scaler loaded.")
    except Exception as e:
        print(f"Error loading model/scaler: {e}. Run model_train.py first.")
        return

    consumer = create_consumer()
    producer = create_producer()
    
    if not consumer or not producer:
        print("Kafka connection failed.")
        return

    # Buffer to hold recent data for prediction
    data_buffer = []

    print("Starting Real-Time Predictor...")
    
    for message in consumer:
        data = message.value
        
        # We need Price, Volume, and MA. 
        # MA requires history. For simplicity, we calculate MA on the buffer.
        
        current_price = data['price']
        current_volume = data['volume']
        
        # Add to buffer (temp storage for raw values)
        data_buffer.append({'price': current_price, 'volume': current_volume})
        
        # Keep buffer size manageable, but enough for MA and TimeSteps
        if len(data_buffer) > TIME_STEPS + 10:
            data_buffer.pop(0)
            
        # Need at least 5 points for MA and TIME_STEPS points for prediction
        if len(data_buffer) >= TIME_STEPS:
            df = pd.DataFrame(data_buffer)
            df['5min_MA'] = df['price'].rolling(window=5).mean()
            
            # Get the last TIME_STEPS rows
            recent_df = df.iloc[-TIME_STEPS:].copy()
            
            if recent_df['5min_MA'].isnull().any():
                continue # Wait for valid MA
                
            features = recent_df[['price', 'volume', '5min_MA']].values
            
            # Scale
            scaled_features = scaler.transform(features)
            
            # Reshape for LSTM [1, time_steps, features]
            input_seq = scaled_features.reshape(1, TIME_STEPS, 3)
            
            # Predict
            prediction_scaled = model.predict(input_seq, verbose=0)
            
            # Inverse transform (trickier because scaler expects 3 features)
            # We create a dummy array with the predicted price and 0s for others
            dummy = np.zeros((1, 3))
            dummy[0, 0] = prediction_scaled[0, 0]
            prediction = scaler.inverse_transform(dummy)[0, 0]
            
            print(f"Current: {current_price}, Predicted: {prediction:.2f}")
            
            # Send prediction to Kafka
            output_msg = {
                'symbol': data['symbol'],
                'timestamp': data['timestamp'],
                'predicted_price': float(prediction)
            }
            producer.send(KAFKA_OUTPUT_TOPIC, value=output_msg)

if __name__ == "__main__":
    run_predictor()
