# Start Zookeeper
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$kafkaDir = Join-Path $scriptDir "kafka_local\kafka_2.12-3.3.1"

# Set Java if portable version exists
$javaLocal = Join-Path $scriptDir "java_local"
if (Test-Path $javaLocal) {
    $jdkDir = Get-ChildItem -Path $javaLocal -Directory -Filter "jdk*" | Select-Object -First 1
    if ($jdkDir) {
        $env:JAVA_HOME = $jdkDir.FullName
        $env:PATH = "$($jdkDir.FullName)\bin;$env:PATH"
    }
}

Set-Location $kafkaDir

Write-Host "Starting Zookeeper..." -ForegroundColor Green
& ".\bin\windows\zookeeper-server-start.bat" ".\config\zookeeper.properties"
