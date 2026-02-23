@echo off
REM SF10 Grade Automation - Windows Startup Script
REM Double-click this file to start the web application

echo ========================================
echo SF10 Grade Automation System
echo ========================================
echo.
echo Starting web server...
echo.

REM Change to the script's directory
cd /d "%~dp0"

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

REM Check if virtual environment exists, create if not
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Activate virtual environment and install dependencies
echo Installing/updating dependencies...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip >nul 2>&1
pip install -r requirements.txt >nul 2>&1

if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo ========================================
echo Server Starting...
echo ========================================
echo.
echo Open your browser to: http://localhost:8080
echo.
echo Press CTRL+C to stop the server
echo ========================================
echo.

REM Start the Flask app
python sf10_web_app.py

REM If we get here, the server has stopped
echo.
echo Server stopped.
pause
