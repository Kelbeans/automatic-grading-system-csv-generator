#!/bin/bash

# SF10 Grade Automation - Easy Startup Script
# Double-click this file to start the web interface

cd "$(dirname "$0")"

echo "================================================================"
echo "        SF10 Grade Automation - Starting..."
echo "================================================================"
echo ""
echo "Please wait while the system starts..."
echo ""
echo "The web browser will open automatically in a few seconds..."
echo ""

# Start the Flask app in the background
python3 sf10_web_app.py &
SERVER_PID=$!

# Wait for server to start
sleep 3

# Open the browser
open http://localhost:8080

echo ""
echo "================================================================"
echo "Web interface is now running!"
echo "================================================================"
echo ""
echo "If the browser didn't open automatically, go to:"
echo "http://localhost:8080"
echo ""
echo "Press CTRL+C to stop the server"
echo "================================================================"
echo ""

# Wait for the server process
wait $SERVER_PID

echo ""
echo "System stopped. You can close this window."
read -p "Press Enter to exit..."
