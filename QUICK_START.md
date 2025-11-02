# Quick Start Guide - Enhanced Parking Lot Simulation

## 🚀 Installation

### Prerequisites
- Python 3.7 or higher
- pygame 2.5.2 or higher

### Install pygame
```bash
# Option 1: Using pip
pip install pygame

# Option 2: Using pip3
pip3 install pygame

# Option 3: Using python -m pip
python3 -m pip install pygame
```

---

## ▶️ Running the Simulation

### Basic Usage
```bash
python3 parking_lot_simulation.py
```

### When Prompted
```
How many cars should enter the lot per minute? 30
```

**Recommended values:**
- **5-10**: Watch individual car behavior and smooth movement
- **20-30**: See realistic traffic patterns
- **50-60**: Test deadlock detection and resolution under heavy load

---

## 🎨 What You'll See

### Visual Elements

| Element | Description |
|---------|-------------|
| **Grey squares with numbers** | Roads (numbers show congestion weight) |
| **Green squares** | Empty parking spaces |
| **Yellow squares** | Reserved parking spaces |
| **Red squares** | Occupied parking spaces |
| **Blue circles** | Cars entering the lot |
| **Orange circles** | Cars exiting the lot |

### Entry Points (Blue cars spawn here)
- **(0, 0)** - Top-left corner
- **(15, 0)** - Top-middle  
- **(30, 0)** - Top-right corner

### Exit Points (Orange cars leave here)
- **(30, 0)** - Top-right corner
- **(30, 15)** - Right-middle
- **(30, 30)** - Bottom-right corner

### Statistics Display (Bottom of window)
```
Entering: 5 | Parked: 120 | Exiting: 3 | Waiting: 2
Total spawned: 150 | Empty spaces: 380
Deadlocks resolved: 4
```

---

## 🎯 Key Features to Observe

### 1. **Smooth 60fps Movement**
- Watch cars glide smoothly between grid positions
- No jumping or teleporting
- Fluid, realistic motion

### 2. **Intelligent Pathfinding**
- Cars choose optimal routes based on congestion
- Weight numbers on roads increase with traffic
- Cars avoid heavily congested areas

### 3. **Entry and Exit Flow**
- Cars enter at 3 fixed points
- After parking (5-15 seconds), cars automatically exit
- Cars pathfind to nearest exit point
- Orange color indicates exiting cars

### 4. **Traffic Management**
- Only one car per road segment
- Cars wait when segments are blocked
- Watch the "Waiting" counter

### 5. **Deadlock Detection & Resolution**
- System detects when cars are stuck in circular waits
- Automatically reroutes cars to resolve deadlocks
- Watch "Deadlocks resolved" counter increment
- Rerouted cars get priority routing

---

## 🧪 Testing the Features

### Test Smooth Movement
```bash
# Run with low traffic
python3 parking_lot_simulation.py
# Enter: 5

# Observe:
# - Cars move smoothly, not in jumps
# - Fluid transitions between segments
```

### Test Entry/Exit System
```bash
# Run with medium traffic
python3 parking_lot_simulation.py
# Enter: 20

# Observe:
# - Blue cars entering from 3 entry points
# - Cars parking (disappear into red squares)
# - Orange cars exiting to 3 exit points
# - "Entering", "Parked", "Exiting" counters
```

### Test Deadlock Detection
```bash
# Run with high traffic
python3 parking_lot_simulation.py
# Enter: 60

# Observe:
# - "Waiting" counter increases
# - "Deadlocks resolved" counter increments
# - Cars automatically reroute
# - Traffic continues flowing
```

### Verify Features Without Running
```bash
python3 test_features.py
```
This checks all features are implemented correctly.

---

## 🎮 Controls

- **Close Window**: Exit the simulation
- **No keyboard controls**: Simulation runs automatically

---

## 📊 Understanding the Weights

### Road Weight System
- **1.0**: Base weight (no traffic)
- **+1.5**: Added when car reserves path
- **+10.5**: Added when car enters segment
- **-12**: Removed when car leaves segment

### Deadlock Weights (Special)
- **+3**: Path reservation for rerouted cars
- **+21**: Segment entry for rerouted cars
- **-24**: Segment exit for rerouted cars

**Higher weights = More congestion = Cars avoid this route**

---

## 🔍 Troubleshooting

### Simulation Runs Slowly
- **Cause**: Too many cars or slow hardware
- **Solution**: Reduce cars per minute (try 10-20)

### No Cars Spawning
- **Cause**: All parking spaces full or entry points blocked
- **Solution**: Wait for cars to exit, or restart with lower rate

### Pygame Not Found
```bash
# Install pygame
pip3 install pygame

# Or
python3 -m pip install pygame
```

### Display Issues
- **Cause**: No GUI support (headless environment)
- **Solution**: Run on system with display/X11 support

---

## 📖 More Information

- **Full Feature Documentation**: See `ENHANCED_FEATURES.md`
- **Installation Help**: See `INSTALL.md`
- **Algorithm Details**: See `SIMULATION_GUIDE.md`
- **Original README**: See `readme.md`

---

## 🎯 Quick Tips

1. **Start Small**: Begin with 5-10 cars/minute to understand behavior
2. **Watch Weights**: Road numbers show congestion in real-time
3. **Color Coding**: Blue = entering, Orange = exiting
4. **Deadlock Counter**: Shows system is working to prevent gridlock
5. **Waiting Counter**: Normal to see some waiting, system handles it
6. **Empty Spaces**: When this reaches 0, no new cars can enter

---

## 🏁 Example Session

```bash
$ python3 parking_lot_simulation.py

==================================================
PARKING LOT SIMULATION
==================================================

This simulation uses a 31x31 grid with:
- Grey roads with weight numbers
- Green = Empty parking spaces
- Yellow = Reserved parking spaces
- Red = Occupied parking spaces
- Blue circles = Cars in motion

==================================================

How many cars should enter the lot per minute? 30

Starting simulation with 30 cars per minute...
Close the window to exit the simulation.

[Pygame window opens]

# Watch the simulation run!
# - Blue cars enter from top
# - Cars park (turn red)
# - Orange cars exit to the right
# - Smooth 60fps movement
# - Automatic deadlock resolution

[Close window when done]
```

---

## ✅ Success Indicators

You'll know it's working when you see:
- ✅ Smooth car movement (no jumping)
- ✅ Cars entering from 3 specific points
- ✅ Orange cars exiting to 3 specific points
- ✅ Weight numbers changing on roads
- ✅ Statistics updating in real-time
- ✅ Deadlocks being resolved automatically
- ✅ Consistent 60 FPS performance

---

**Enjoy the simulation!** 🚗💨
