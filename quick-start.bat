@echo off
echo ========================================
echo Agentcore Memory Demo - Quick Start
echo ACD Ahmedabad 2026
echo ========================================
echo.

echo Checking Python installation...
python --version
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.9+
    pause
    exit /b 1
)

echo.
echo Creating virtual environment...
if not exist venv (
    python -m venv venv
    echo Virtual environment created.
) else (
    echo Virtual environment already exists.
)

echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo ========================================
echo Setup complete!
echo ========================================
echo.
echo Choose an option:
echo 1. Run CLI Demo
echo 2. Run Web Interface
echo 3. Run Test Scenarios
echo.

set /p choice="Enter choice (1-3): "

if "%choice%"=="1" (
    echo.
    echo Starting CLI Demo...
    python main.py
) else if "%choice%"=="2" (
    echo.
    echo Starting Web Interface...
    echo Open browser to: http://localhost:5000
    python app.py
) else if "%choice%"=="3" (
    echo.
    echo Running Test Scenarios...
    python examples\test_scenarios.py
) else (
    echo Invalid choice. Exiting.
)

pause
