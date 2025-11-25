from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, emit
import json
import threading
import time
from kafka import KafkaConsumer

app = Flask(__name__)
app.config['SECRET_KEY'] = 'stock-analysis-secret'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Configuration
KAFKA_BOOTSTRAP_SERVERS = 'localhost:9092'
STOCK_TOPIC = 'stock-market'
PREDICTION_TOPIC = 'stock-predictions'

# Store recent data
recent_data = []
recent_predictions = []
alerts = []
total_messages_count = 0

def consume_stock_data():
    """Background thread to consume stock market data"""
    global total_messages_count
    try:
        consumer = KafkaConsumer(
            STOCK_TOPIC,
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            auto_offset_reset='latest',
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
        
        for message in consumer:
            data = message.value
            recent_data.append(data)
            total_messages_count += 1
            
            # Keep only last 100 records
            if len(recent_data) > 100:
                recent_data.pop(0)
            
            # Check for alerts
            if data['volume'] > 1000000:
                alert = {
                    'symbol': data['symbol'],
                    'volume': data['volume'],
                    'price': data['price'],
                    'timestamp': data['timestamp']
                }
                alerts.append(alert)
                if len(alerts) > 20:
                    alerts.pop(0)
                socketio.emit('alert', alert)
            
            # Emit to all connected clients
            data['total_messages'] = total_messages_count
            socketio.emit('stock_update', data)
    except Exception as e:
        print(f"Error in stock consumer: {e}")

def consume_predictions():
    """Background thread to consume predictions"""
    try:
        consumer = KafkaConsumer(
            PREDICTION_TOPIC,
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            auto_offset_reset='latest',
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
        
        for message in consumer:
            data = message.value
            recent_predictions.append(data)
            
            if len(recent_predictions) > 50:
                recent_predictions.pop(0)
            
            socketio.emit('prediction_update', data)
    except Exception as e:
        print(f"Error in prediction consumer: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/api/recent-data')
def get_recent_data():
    return jsonify(recent_data[-50:])

@app.route('/api/predictions')
def get_predictions():
    return jsonify(recent_predictions[-20:])

@app.route('/api/alerts')
def get_alerts():
    return jsonify(alerts)

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('initial_data', {
        'stocks': recent_data[-50:],
        'predictions': recent_predictions[-20:],
        'alerts': alerts,
        'total_messages': total_messages_count
    })

if __name__ == '__main__':
    # Start background consumers
    stock_thread = threading.Thread(target=consume_stock_data, daemon=True)
    prediction_thread = threading.Thread(target=consume_predictions, daemon=True)
    
    stock_thread.start()
    prediction_thread.start()
    
    print("Starting Real-Time Stock Analysis Dashboard...")
    print("Open http://localhost:5001 in your browser")
    
    socketio.run(app, debug=True, host='0.0.0.0', port=5001, allow_unsafe_werkzeug=True)
