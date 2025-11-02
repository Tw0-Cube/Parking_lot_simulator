# Parking Lot Simulation with Weighted Path Finding

An intelligent parking lot simulation that uses a modified BFS (Dijkstra's) algorithm with dynamic weight updates to optimize parking space allocation and traffic flow.

## 🚗 Quick Start

```bash
# Install dependencies
pip install pygame

# Run the simulation
python3 parking_lot_simulation.py
```

When prompted, enter how many cars should enter per minute (e.g., 10, 30, 60).

## 📋 Files

- **parking_lot_simulation.py** - Main simulation program
- **test_grid.py** - Test script to verify grid structure
- **requirements.txt** - Python dependencies
- **README.md** - This file
- **INSTALL.md** - Detailed installation instructions
- **SIMULATION_GUIDE.md** - Complete guide to understanding the simulation

## 🎯 Features

- ✅ 31x31 grid with 500 parking spaces and 461 road segments
- ✅ Modified Dijkstra's algorithm for optimal path finding
- ✅ Dynamic weight system that adapts to traffic
- ✅ Real-time visualization with color-coded states
- ✅ Collision prevention (one car per segment)
- ✅ Configurable car spawn rate
- ✅ Smooth 60 FPS animation

## 🎨 Visual Guide

| Color | Meaning |
|-------|---------|
| Grey + numbers | Road segments (weight displayed) |
| Green | Empty parking space |
| Yellow | Reserved parking space |
| Red | Occupied parking space |
| Blue circles | Cars in motion |

## 🧮 Algorithm

The simulation uses a weighted shortest-path algorithm where:

1. **Path Selection**: +1.5 to all segments in chosen path
2. **Car Entry**: +10.5 to segment when car enters
3. **Car Exit**: -12 to segment when car leaves
4. **Minimum Weight**: Always 1.0

This creates natural traffic distribution and prevents collisions!

## 📊 Grid Structure

```
Perimeter: All roads (entry/exit points)
Interior Pattern:
  - 2 parking rows
  - 1 road row
  - Repeat

Each parking row:
  - 5 parking spaces
  - 1 road segment
  - Repeat
```

## 🔧 Requirements

- Python 3.7+
- Pygame 2.5.2+
- Display with GUI support

## 📖 Documentation

- See **INSTALL.md** for installation help
- See **SIMULATION_GUIDE.md** for detailed algorithm explanation
- Run **test_grid.py** to verify grid structure

## 🎮 Running in VSCode

1. Open folder in VSCode
2. Open terminal (Ctrl+` or Cmd+`)
3. Install: `pip install pygame`
4. Run: `python3 parking_lot_simulation.py`
5. Pygame window opens separately

## 🧪 Testing

```bash
# Verify grid structure
python3 test_grid.py

# Check for syntax errors
python3 -m py_compile parking_lot_simulation.py
```

## 💡 Tips

- Start with 5-10 cars/minute to watch individual behavior
- Try 30-60 cars/minute to see congestion handling
- Watch the weight numbers on roads to see traffic patterns
- Close the window to exit

## 🏗️ Technical Details

- **Language**: Python 3
- **Graphics**: Pygame
- **Algorithm**: Modified Dijkstra's with priority queue
- **Data Structures**: 2D arrays, dictionaries, heaps
- **Frame Rate**: 60 FPS
- **Window Size**: 775x875 pixels

---

Created for optimal parking lot simulation with intelligent traffic management!
