# Installation Guide

## Quick Start

### Step 1: Install Python
Make sure you have Python 3.7 or higher installed. Check your version:
```bash
python3 --version
```

### Step 2: Install Pygame
```bash
pip install pygame
```

Or use the requirements file:
```bash
pip install -r requirements.txt
```

### Step 3: Run the Simulation
```bash
python3 parking_lot_simulation.py
```

## Running in VSCode

1. Open this folder in VSCode
2. Open the integrated terminal (View → Terminal or Ctrl+`)
3. Install pygame: `pip install pygame`
4. Run: `python3 parking_lot_simulation.py`
5. Enter the number of cars per minute when prompted
6. A separate Pygame window will open with the simulation

## Troubleshooting

### "pygame not found"
Install pygame:
```bash
pip install pygame
# or
pip3 install pygame
# or
python3 -m pip install pygame
```

### "Python not found"
- **Windows**: Download from https://www.python.org/downloads/
- **Mac**: `brew install python3` or download from python.org
- **Linux**: `sudo apt-get install python3` (Ubuntu/Debian) or `sudo yum install python3` (RedHat/CentOS)

### Pygame window doesn't open
- Make sure you're not running in a headless environment
- Try running from a regular terminal instead of VSCode's integrated terminal
- On Linux, you may need: `sudo apt-get install python3-pygame`

### Performance issues
- Reduce the number of cars per minute
- The simulation runs at 60 FPS and should be smooth on most systems

## System Requirements

- **OS**: Windows, macOS, or Linux with GUI support
- **Python**: 3.7 or higher
- **RAM**: 512 MB minimum
- **Display**: Any resolution (simulation window is 775x875 pixels)

## Testing the Installation

Run the test script to verify the grid structure:
```bash
python3 test_grid.py
```

This should display the 31x31 grid layout with roads (1) and parking spaces (*).
