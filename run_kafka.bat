@echo off
setlocal enabledelayedexpansion

set "SCRIPT_DIR=%~dp0"

REM Set Java if portable version exists
if exist "%SCRIPT_DIR%java_local" (
    for /d %%i in ("%SCRIPT_DIR%java_local\jdk*") do set "JAVA_HOME=%%i"
    set "PATH=!JAVA_HOME!\bin;!PATH!"
)

REM Change to Kafka directory using relative path
cd /d "%SCRIPT_DIR%kafka_local\kafka_2.12-3.3.1"

REM Start Kafka
bin\windows\kafka-server-start.bat config\server.properties
