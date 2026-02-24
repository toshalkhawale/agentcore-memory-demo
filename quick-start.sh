#!/bin/bash

echo "========================================"
echo "Agentcore Memory Demo - Quick Start"
echo "ACD Ahmedabad 2026"
echo "========================================"
echo ""

echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python not found. Please install Python 3.9+"
    exit 1
fi

python3 --version

echo ""
echo "Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "Virtual environment created."
else
    echo "Virtual environment already exists."
fi

echo ""
echo "Activating virtual environment..."
source venv/bin/activate

echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "========================================"
echo "Setup complete!"
echo "========================================"
echo ""
echo "Choose an option:"
echo "1. Run CLI Demo"
echo "2. Run Web Interface"
echo "3. Run Test Scenarios"
echo ""

read -p "Enter choice (1-3): " choice

case $choice in
    1)
        echo ""
        echo "Starting CLI Demo..."
        python main.py
        ;;
    2)
        echo ""
        echo "Starting Web Interface..."
        echo "Open browser to: http://localhost:5000"
        python app.py
        ;;
    3)
        echo ""
        echo "Running Test Scenarios..."
        python examples/test_scenarios.py
        ;;
    *)
        echo "Invalid choice. Exiting."
        ;;
esac
