# Check for Java
try {
    $javaVersion = java -version 2>&1
    if ($LastExitCode -eq 0) {
        Write-Host "Java found." -ForegroundColor Green
    }
    else {
        throw "Java not found"
    }
}
catch {
    Write-Host "Java not found. Downloading Portable JDK (Amazon Corretto 17)..." -ForegroundColor Yellow
    $jdkUrl = "https://corretto.aws/downloads/latest/amazon-corretto-17-x64-windows-jdk.zip"
    $jdkZip = "$PSScriptRoot\jdk.zip"
    $javaInstallDir = "$PSScriptRoot\java_local"
    
    if (-not (Test-Path $javaInstallDir)) {
        Invoke-WebRequest -Uri $jdkUrl -OutFile $jdkZip
        Write-Host "Extracting JDK..." -ForegroundColor Cyan
        Expand-Archive -Path $jdkZip -DestinationPath $javaInstallDir -Force
        Remove-Item $jdkZip
    }
    
    # Find the bin directory
    $jdkBin = Get-ChildItem -Path $javaInstallDir -Recurse -Directory -Filter "bin" | Select-Object -First 1
    if ($jdkBin) {
        $env:PATH = "$($jdkBin.FullName);$env:PATH"
        $env:JAVA_HOME = $jdkBin.Parent.FullName
        Write-Host "Java configured temporarily for this session." -ForegroundColor Green
    }
    else {
        Write-Host "Failed to setup Java automatically." -ForegroundColor Red
        exit 1
    }
}

# Define versions and paths
$kafkaVersion = "3.3.1"
$scalaVersion = "2.12"
$kafkaDirName = "kafka_$scalaVersion-$kafkaVersion"
$downloadUrl = "https://archive.apache.org/dist/kafka/$kafkaVersion/$kafkaDirName.tgz"
$installDir = "$PSScriptRoot\kafka_local"

# Create install directory
if (-not (Test-Path $installDir)) {
    New-Item -ItemType Directory -Path $installDir | Out-Null
}

# Download Kafka
$tgzPath = "$installDir\kafka.tgz"
if (-not (Test-Path "$installDir\$kafkaDirName")) {
    Write-Host "Downloading Kafka..." -ForegroundColor Cyan
    Invoke-WebRequest -Uri $downloadUrl -OutFile $tgzPath
    
    Write-Host "Extracting Kafka..." -ForegroundColor Cyan
    # Using tar (available in Windows 10/11)
    tar -xzf $tgzPath -C $installDir
    
    Remove-Item $tgzPath
}
else {
    Write-Host "Kafka already downloaded." -ForegroundColor Yellow
}

$kafkaRoot = "$installDir\$kafkaDirName"

# Create Helper Batch Files
$zookeeperBat = "$PSScriptRoot\run_zookeeper.bat"
$kafkaBat = "$PSScriptRoot\run_kafka.bat"

$zookeeperContent = @"
@echo off
set "SCRIPT_DIR=%~dp0"
if exist "%SCRIPT_DIR%java_local" (
    for /d %%i in ("%SCRIPT_DIR%java_local\jdk*") do set "JAVA_HOME=%%i"
    set "PATH=%JAVA_HOME%\bin;%PATH%"
)
cd "$kafkaRoot"
bin\windows\zookeeper-server-start.bat config\zookeeper.properties
"@

$kafkaContent = @"
@echo off
set "SCRIPT_DIR=%~dp0"
if exist "%SCRIPT_DIR%java_local" (
    for /d %%i in ("%SCRIPT_DIR%java_local\jdk*") do set "JAVA_HOME=%%i"
    set "PATH=%JAVA_HOME%\bin;%PATH%"
)
cd "$kafkaRoot"
bin\windows\kafka-server-start.bat config\server.properties
"@

Set-Content -Path $zookeeperBat -Value $zookeeperContent
Set-Content -Path $kafkaBat -Value $kafkaContent

Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "1. Open a new terminal and run: .\run_zookeeper.bat"
Write-Host "2. Open another terminal and run: .\run_kafka.bat"
