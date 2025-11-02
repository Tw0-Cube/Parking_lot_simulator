#!/bin/bash

# Quick start script for parking lot simulation

echo "=========================================="
echo "Parking Lot Simulation - Quick Start"
echo "=========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed!"
    echo "Please install Python 3.7 or higher"
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"

# Check if pygame is installed
if ! python3 -c "import pygame" 2>/dev/null; then
    echo ""
    echo "⚠️  Pygame is not installed"
    echo "Installing pygame..."
    pip install pygame
    
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install pygame"
        echo "Please run: pip install pygame"
        exit 1
    fi
    echo "✓ Pygame installed successfully"
else
    echo "✓ Pygame is already installed"
fi

echo ""
echo "=========================================="
echo "Starting simulation..."
echo "=========================================="
echo ""

# Run the simulation
python3 parking_lot_simulation.py
