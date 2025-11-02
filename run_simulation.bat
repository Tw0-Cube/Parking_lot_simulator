@echo off
REM Quick start script for parking lot simulation (Windows)

echo ==========================================
echo Parking Lot Simulation - Quick Start
echo ==========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo X Python is not installed!
    echo Please install Python 3.7 or higher from python.org
    pause
    exit /b 1
)

echo [OK] Python found
python --version

REM Check if pygame is installed
python -c "import pygame" >nul 2>&1
if errorlevel 1 (
    echo.
    echo [!] Pygame is not installed
    echo Installing pygame...
    pip install pygame
   
    if errorlevel 1 (
        echo X Failed to install pygame
        echo Please run: pip install pygame
        pause
        exit /b 1
    )
    echo [OK] Pygame installed successfully
) else (
    echo [OK] Pygame is already installed
)

echo.
echo ==========================================
echo Starting simulation...
echo ==========================================
echo.

REM Run the simulation
python parking_lot_simulation.py

pause