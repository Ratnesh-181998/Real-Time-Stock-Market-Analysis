# run_project.ps1

Write-Host "=== Starting Real-Time Stock Analysis System ===" -ForegroundColor Cyan

# Define safe paths (workaround for paths with spaces)
$SafeKafkaDir = "C:\kafka_temp\kafka_2.12-3.3.1"
$SafeJavaDir = "C:\java_temp\jdk17.0.17_10"

# 1. Start Zookeeper (if not running)
$zk = Get-NetTCPConnection -LocalPort 2181 -ErrorAction SilentlyContinue
if ($zk) {
    Write-Host "✅ Zookeeper is already running." -ForegroundColor Green
}
else {
    Write-Host "🚀 Starting Zookeeper..." -ForegroundColor Yellow
    if (Test-Path $SafeKafkaDir) {
        Start-Process powershell -ArgumentList "-NoExit", "-Command", "`$env:JAVA_HOME='$SafeJavaDir'; `$env:PATH='$SafeJavaDir\bin;'+`$env:PATH; cd '$SafeKafkaDir'; .\bin\windows\zookeeper-server-start.bat .\config\zookeeper.properties"
        Start-Sleep -Seconds 10
    }
    else {
        Write-Error "Kafka temp directory not found at $SafeKafkaDir. Please check setup."
    }
}

# 2. Start Kafka (if not running)
$kafka = Get-NetTCPConnection -LocalPort 9092 -ErrorAction SilentlyContinue
if ($kafka) {
    Write-Host "✅ Kafka is already running." -ForegroundColor Green
}
else {
    Write-Host "🚀 Starting Kafka..." -ForegroundColor Yellow
    if (Test-Path $SafeKafkaDir) {
        Start-Process powershell -ArgumentList "-NoExit", "-Command", "`$env:JAVA_HOME='$SafeJavaDir'; `$env:PATH='$SafeJavaDir\bin;'+`$env:PATH; cd '$SafeKafkaDir'; .\bin\windows\kafka-server-start.bat .\config\server.properties"
        Start-Sleep -Seconds 10
    }
}

# 3. Start Application Components
Write-Host "🚀 Starting Application Components..." -ForegroundColor Magenta

# Producer
Start-Process powershell -ArgumentList "-NoExit", "-Command", "python src/producer.py"

# Predictor
Start-Process powershell -ArgumentList "-NoExit", "-Command", "python src/predictor.py"

# Dashboard
Start-Process powershell -ArgumentList "-NoExit", "-Command", "python src/dashboard.py"

# Alert System
Start-Process powershell -ArgumentList "-NoExit", "-Command", "python src/alert_system.py"

Write-Host "✅ All components launched!" -ForegroundColor Green
Write-Host "👉 Access Dashboard at: http://localhost:5001" -ForegroundColor Cyan
