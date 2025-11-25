// Initialize Socket.IO
const socket = io();

// State
let stockData = {};
let priceHistory = {};
let chart = null;
let totalMessages = 0;
let alertCount = 0;

// DOM Elements
const statusDot = document.getElementById('statusDot');
const statusText = document.getElementById('statusText');
const stockList = document.getElementById('stockList');
const predictionList = document.getElementById('predictionList');
const alertList = document.getElementById('alertList');
const feedCount = document.getElementById('feedCount');
const stockSelector = document.getElementById('stockSelector');
const totalMessagesEl = document.getElementById('totalMessages');
const activeStocksEl = document.getElementById('activeStocks');
const avgVolumeEl = document.getElementById('avgVolume');
const highVolumeEventsEl = document.getElementById('highVolumeEvents');
const alertCountEl = document.getElementById('alertCount');

// Initialize Chart
function initChart() {
    const ctx = document.getElementById('priceChart').getContext('2d');
    chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Price',
                data: [],
                borderColor: '#667eea',
                backgroundColor: 'rgba(102, 126, 234, 0.1)',
                borderWidth: 3,
                tension: 0.4,
                fill: true,
                pointRadius: 0,
                pointHoverRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    mode: 'index',
                    intersect: false,
                    backgroundColor: 'rgba(15, 23, 42, 0.9)',
                    titleColor: '#f1f5f9',
                    bodyColor: '#f1f5f9',
                    borderColor: '#667eea',
                    borderWidth: 1,
                    padding: 12,
                    displayColors: false
                }
            },
            scales: {
                x: {
                    display: true,
                    grid: {
                        color: 'rgba(51, 65, 85, 0.3)'
                    },
                    ticks: {
                        color: '#94a3b8',
                        maxTicksLimit: 10
                    }
                },
                y: {
                    display: true,
                    grid: {
                        color: 'rgba(51, 65, 85, 0.3)'
                    },
                    ticks: {
                        color: '#94a3b8'
                    }
                }
            },
            interaction: {
                mode: 'nearest',
                axis: 'x',
                intersect: false
            }
        }
    });
}

// Socket Events
socket.on('connect', () => {
    statusDot.classList.add('connected');
    statusText.textContent = 'Connected';
    console.log('Connected to server');
});

socket.on('disconnect', () => {
    statusDot.classList.remove('connected');
    statusText.textContent = 'Disconnected';
    console.log('Disconnected from server');
});

socket.on('initial_data', (data) => {
    console.log('Received initial data:', data);

    // Process stocks
    if (data.stocks && data.stocks.length > 0) {
        data.stocks.forEach(stock => processStockUpdate(stock));
    }

    // Process predictions
    if (data.predictions && data.predictions.length > 0) {
        data.predictions.forEach(pred => processPrediction(pred));
    }

    // Process alerts
    if (data.alerts && data.alerts.length > 0) {
        data.alerts.forEach(alert => processAlert(alert));
    }

    // Process total messages
    if (data.total_messages) {
        totalMessages = data.total_messages;
    }

    updateStats();
});

socket.on('stock_update', (data) => {
    processStockUpdate(data);
    updateStats();
});

socket.on('prediction_update', (data) => {
    processPrediction(data);
});

socket.on('alert', (data) => {
    processAlert(data);
    alertCount++;
    alertCountEl.textContent = alertCount;
    highVolumeEventsEl.textContent = alertCount;
});

// Process Stock Update
function processStockUpdate(data) {
    if (data.total_messages) {
        totalMessages = data.total_messages;
    } else {
        totalMessages++;
    }

    // Update stock data
    if (!stockData[data.symbol]) {
        stockData[data.symbol] = [];

        // Add to selector
        const option = document.createElement('option');
        option.value = data.symbol;
        option.textContent = data.symbol;
        stockSelector.appendChild(option);
    }

    stockData[data.symbol].push(data);

    // Keep only last 100 points
    if (stockData[data.symbol].length > 100) {
        stockData[data.symbol].shift();
    }

    // Update price history for chart
    if (!priceHistory[data.symbol]) {
        priceHistory[data.symbol] = { labels: [], prices: [] };
    }

    const time = new Date(data.timestamp).toLocaleTimeString();
    priceHistory[data.symbol].labels.push(time);
    priceHistory[data.symbol].prices.push(data.price);

    if (priceHistory[data.symbol].labels.length > 50) {
        priceHistory[data.symbol].labels.shift();
        priceHistory[data.symbol].prices.shift();
    }

    // Update chart if this stock is selected
    const selectedStock = stockSelector.value;
    if (selectedStock === data.symbol && chart) {
        updateChart(data.symbol);
    } else if (!selectedStock && chart) {
        // Auto-select first stock
        stockSelector.value = data.symbol;
        updateChart(data.symbol);
    }

    // Update live feed
    updateLiveFeed();
}

// Process Prediction
function processPrediction(data) {
    const predItem = document.createElement('div');
    predItem.className = 'prediction-item';
    predItem.innerHTML = `
        <div class="prediction-symbol">${data.symbol}</div>
        <div class="prediction-value">$${data.predicted_price.toFixed(2)}</div>
        <div class="stock-time">${new Date(data.timestamp).toLocaleTimeString()}</div>
    `;

    if (predictionList.querySelector('.empty-state')) {
        predictionList.innerHTML = '';
    }

    predictionList.insertBefore(predItem, predictionList.firstChild);

    // Keep only last 20
    while (predictionList.children.length > 20) {
        predictionList.removeChild(predictionList.lastChild);
    }
}

// Process Alert
function processAlert(data) {
    const alertItem = document.createElement('div');
    alertItem.className = 'alert-item';
    alertItem.innerHTML = `
        <div class="alert-symbol">⚠️ ${data.symbol}</div>
        <div>Volume: ${data.volume.toLocaleString()}</div>
        <div>Price: $${data.price.toFixed(2)}</div>
        <div class="stock-time">${new Date(data.timestamp).toLocaleTimeString()}</div>
    `;

    if (alertList.querySelector('.empty-state')) {
        alertList.innerHTML = '';
    }

    alertList.insertBefore(alertItem, alertList.firstChild);

    // Keep only last 20
    while (alertList.children.length > 20) {
        alertList.removeChild(alertList.lastChild);
    }
}

// Update Live Feed
function updateLiveFeed() {
    const allStocks = [];

    for (const symbol in stockData) {
        const stocks = stockData[symbol];
        if (stocks.length > 0) {
            allStocks.push(stocks[stocks.length - 1]);
        }
    }

    // Sort by timestamp (newest first)
    allStocks.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));

    stockList.innerHTML = '';

    allStocks.slice(0, 20).forEach(stock => {
        const stockItem = document.createElement('div');
        stockItem.className = 'stock-item';
        stockItem.innerHTML = `
            <div>
                <div class="stock-symbol">${stock.symbol}</div>
                <div class="stock-volume">Vol: ${stock.volume.toLocaleString()}</div>
            </div>
            <div style="text-align: right;">
                <div class="stock-price">$${stock.price.toFixed(2)}</div>
                <div class="stock-time">${new Date(stock.timestamp).toLocaleTimeString()}</div>
            </div>
        `;
        stockList.appendChild(stockItem);
    });

    feedCount.textContent = `${totalMessages} updates`;
}

// Update Chart
function updateChart(symbol) {
    if (!priceHistory[symbol] || !chart) return;

    chart.data.labels = priceHistory[symbol].labels;
    chart.data.datasets[0].data = priceHistory[symbol].prices;
    chart.data.datasets[0].label = `${symbol} Price`;
    chart.update('none');
}

// Update Statistics
function updateStats() {
    totalMessagesEl.textContent = totalMessages.toLocaleString();
    activeStocksEl.textContent = Object.keys(stockData).length;

    // Calculate average volume
    let totalVolume = 0;
    let count = 0;

    for (const symbol in stockData) {
        stockData[symbol].forEach(stock => {
            totalVolume += stock.volume;
            count++;
        });
    }

    const avgVolume = count > 0 ? Math.round(totalVolume / count) : 0;
    avgVolumeEl.textContent = avgVolume.toLocaleString();
}

// Stock Selector Change
stockSelector.addEventListener('change', (e) => {
    const symbol = e.target.value;
    if (symbol && chart) {
        updateChart(symbol);
    }
});

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    initChart();
});
