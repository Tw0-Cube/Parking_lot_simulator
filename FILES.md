# Project Files

## Main Files

### parking_lot_simulation.py
**Purpose**: Main simulation program with full Pygame visualization
**Size**: ~450 lines
**Contains**:
- `ParkingLot` class - Grid management and pathfinding
- `Car` class - Individual car behavior and movement
- `Simulation` class - Pygame visualization and main loop
- Modified Dijkstra's algorithm implementation
- Dynamic weight update system
- Real-time graphics rendering

**Run**: `python3 parking_lot_simulation.py`

---

### test_grid.py
**Purpose**: Verify the parking lot grid structure
**Size**: ~70 lines
**Contains**:
- Grid initialization logic
- Visual grid printer (1 = road, * = parking)
- Statistics counter

**Run**: `python3 test_grid.py`
**Output**: Displays 31x31 grid and counts (500 parking, 461 roads)

---

### demo_pathfinding.py
**Purpose**: Demonstrate pathfinding algorithm without GUI
**Size**: ~180 lines
**Contains**:
- Simplified pathfinding implementation
- Weight update demonstration
- Example scenarios with 3 cars
- Statistics and analysis

**Run**: `python3 demo_pathfinding.py`
**Output**: Shows path finding, weight updates, and statistics

---

## Quick Start Scripts

### run_simulation.sh
**Purpose**: Automated setup and launch script for Linux/Mac
**Features**:
- Checks for Python 3
- Installs Pygame if needed
- Launches simulation
- Error handling

**Run**: `./run_simulation.sh`
**Permissions**: Executable (chmod +x applied)

---

### run_simulation.bat
**Purpose**: Automated setup and launch script for Windows
**Features**:
- Checks for Python
- Installs Pygame if needed
- Launches simulation
- Error handling

**Run**: `run_simulation.bat` (double-click or run in cmd)

---

## Documentation Files

### README.md
**Purpose**: Main project documentation
**Contains**:
- Project overview
- Features list
- Installation instructions
- Quick start guide
- Usage examples
- Technical details
- Grid structure explanation
- Algorithm description

**Audience**: All users (primary documentation)

---

### INSTALL.md
**Purpose**: Detailed installation guide
**Contains**:
- Step-by-step installation
- Platform-specific instructions
- Troubleshooting section
- System requirements
- VSCode setup guide

**Audience**: Users having installation issues

---

### SIMULATION_GUIDE.md
**Purpose**: Deep dive into simulation mechanics
**Contains**:
- Visual legend
- Grid layout details
- Algorithm explanation with examples
- Weight update system
- Parking space states
- Example scenarios
- Statistics explanation
- Testing tips

**Audience**: Users wanting to understand the algorithm

---

### PROJECT_SUMMARY.md
**Purpose**: Technical overview for developers
**Contains**:
- Architecture overview
- Algorithm pseudocode
- Weight update examples
- Performance characteristics
- Technical decisions and rationale
- Future enhancements
- Testing procedures
- Complete file structure

**Audience**: Developers and technical reviewers

---

### FILES.md
**Purpose**: This file - complete file listing
**Contains**:
- Description of each file
- Purpose and contents
- How to use each file
- Target audience

**Audience**: Anyone exploring the project structure

---

## Configuration Files

### requirements.txt
**Purpose**: Python package dependencies
**Contains**:
```
pygame==2.5.2
```

**Usage**: `pip install -r requirements.txt`

---

### readme.md (lowercase)
**Purpose**: Original readme file (now updated)
**Contains**: Project overview and quick start guide
**Note**: Same content as README.md (for compatibility)

---

## Directory Structure

```
/vercel/sandbox/
├── parking_lot_simulation.py    [Main simulation - 450 lines]
├── test_grid.py                  [Grid verification - 70 lines]
├── demo_pathfinding.py           [Algorithm demo - 180 lines]
├── run_simulation.sh             [Linux/Mac launcher]
├── run_simulation.bat            [Windows launcher]
├── requirements.txt              [Dependencies]
├── README.md                     [Main documentation]
├── readme.md                     [Compatibility readme]
├── INSTALL.md                    [Installation guide]
├── SIMULATION_GUIDE.md           [Algorithm guide]
├── PROJECT_SUMMARY.md            [Technical overview]
├── FILES.md                      [This file]
└── __pycache__/                  [Python cache - auto-generated]
```

---

## File Relationships

```
User wants to run simulation
    ↓
Quick Start: run_simulation.sh/.bat
    ↓
Installs: requirements.txt (pygame)
    ↓
Runs: parking_lot_simulation.py
    ↓
User sees: Pygame window with simulation

User wants to understand
    ↓
Start: README.md (overview)
    ↓
Details: SIMULATION_GUIDE.md (how it works)
    ↓
Technical: PROJECT_SUMMARY.md (architecture)

User has problems
    ↓
Check: INSTALL.md (troubleshooting)
    ↓
Test: test_grid.py (verify setup)
    ↓
Demo: demo_pathfinding.py (see algorithm)
```

---

## Quick Reference

| Want to... | Use this file |
|------------|---------------|
| Run simulation | `run_simulation.sh` or `.bat` |
| Understand algorithm | `SIMULATION_GUIDE.md` |
| Install manually | `INSTALL.md` |
| See code structure | `PROJECT_SUMMARY.md` |
| Test grid layout | `test_grid.py` |
| See pathfinding demo | `demo_pathfinding.py` |
| Check dependencies | `requirements.txt` |
| Get overview | `README.md` |
| Explore files | `FILES.md` (this file) |

---

## Total Project Stats

- **Total Python files**: 3 (main + 2 tests/demos)
- **Total documentation**: 6 markdown files
- **Total scripts**: 2 (shell + batch)
- **Total lines of code**: ~700 lines
- **Total documentation**: ~2000+ lines
- **Dependencies**: 1 (pygame)
- **Supported platforms**: Windows, macOS, Linux

---

## For Developers

### To modify the simulation:
1. Edit `parking_lot_simulation.py`
2. Test with `python3 parking_lot_simulation.py`
3. Verify grid with `python3 test_grid.py`
4. Check algorithm with `python3 demo_pathfinding.py`

### To add features:
1. Read `PROJECT_SUMMARY.md` for architecture
2. Read `SIMULATION_GUIDE.md` for algorithm details
3. Modify appropriate class in `parking_lot_simulation.py`
4. Test thoroughly

### To contribute documentation:
1. Update relevant .md file
2. Keep FILES.md in sync
3. Update README.md if needed

---

**Last Updated**: November 2, 2025
**Project Status**: ✅ Complete and tested
**Language**: Python 3.7+
**License**: Not specified (add if needed)
