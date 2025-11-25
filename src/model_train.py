import os
import glob
import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout

# Configuration
DATA_DIR = '../data/raw'
MODEL_PATH = 'lstm_model.keras'
SCALER_PATH = 'scaler.pkl'

def load_data():
    # Find all CSV files in the data directory
    files = glob.glob(os.path.join(DATA_DIR, '**', '*.csv'), recursive=True)
    if not files:
        print("No data found. Generating dummy data for training demonstration...")
        return generate_dummy_data()
    
    print(f"Loading data from {len(files)} files...")
    df_list = [pd.read_csv(f) for f in files]
    df = pd.concat(df_list, ignore_index=True)
    return df

def generate_dummy_data():
    # Generate 1000 rows of dummy data for 'AAPL'
    dates = pd.date_range(start='2023-01-01', periods=1000, freq='T')
    prices = np.random.normal(150, 5, 1000).cumsum() # Random walk
    df = pd.DataFrame({
        'timestamp': dates,
        'symbol': 'AAPL',
        'price': abs(prices),
        'volume': np.random.randint(1000, 500000, 1000)
    })
    return df

def preprocess_data(df):
    # Filter for a single stock for simplicity (e.g., AAPL or the most frequent one)
    top_stock = df['symbol'].mode()[0]
    print(f"Training model for symbol: {top_stock}")
    df = df[df['symbol'] == top_stock].copy()
    
    # Sort by time
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.sort_values('timestamp')
    
    # Feature Engineering: 5-min Moving Average (rolling window of 5 if data is minutely)
    # The notes say 300 seconds = 5 mins. Assuming 1 row per minute or second.
    df['5min_MA'] = df['price'].rolling(window=5).mean()
    df.dropna(inplace=True)
    
    # Features for LSTM: Price, Volume, MA
    features = ['price', 'volume', '5min_MA']
    data = df[features].values
    
    # Scale data
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(data)
    
    return scaled_data, scaler

def create_sequences(data, time_steps=60):
    X, y = [], []
    for i in range(len(data) - time_steps):
        X.append(data[i:(i + time_steps)])
        y.append(data[i + time_steps, 0]) # Predict next price
    return np.array(X), np.array(y)

def train_model():
    df = load_data()
    if df.empty:
        print("DataFrame is empty.")
        return

    scaled_data, scaler = preprocess_data(df)
    
    time_steps = 60
    if len(scaled_data) <= time_steps:
        print("Not enough data to create sequences.")
        return

    X_train, y_train = create_sequences(scaled_data, time_steps)
    
    # Reshape for LSTM [samples, time steps, features]
    # X_train is already [samples, time_steps, features]
    
    print(f"Training data shape: {X_train.shape}")
    
    # Build LSTM Model
    model = Sequential([
        LSTM(128, input_shape=(X_train.shape[1], X_train.shape[2])),
        Dropout(0.3),
        Dense(1)
    ])
    
    model.compile(loss='mae', optimizer='adam')
    
    model.fit(X_train, y_train, epochs=5, batch_size=32, verbose=1)
    
    # Save model and scaler
    model.save(MODEL_PATH.replace('.h5', '.keras'))
    joblib.dump(scaler, SCALER_PATH)
    print(f"Model saved to {MODEL_PATH.replace('.h5', '.keras')}")
    print(f"Scaler saved to {SCALER_PATH}")

if __name__ == "__main__":
    train_model()
