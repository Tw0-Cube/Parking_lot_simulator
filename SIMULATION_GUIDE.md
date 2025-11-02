# Parking Lot Simulation Guide

## Understanding the Simulation

### Visual Legend

| Color | Meaning |
|-------|---------|
| **Grey with numbers** | Road segments (numbers show current weight) |
| **Green** | Empty parking space (available) |
| **Yellow** | Reserved parking space (car on the way) |
| **Red** | Occupied parking space (car parked) |
| **Blue circles** | Cars in motion |

### Grid Layout (31x31)

```
Perimeter: All roads (entry/exit points)
Inside Pattern:
  - 2 rows of parking
  - 1 row of roads
  - Repeat...

Each parking row:
  - 5 parking spaces
  - 1 road segment
  - Repeat...
```

**Total**: 500 parking spaces, 461 road segments

### How the Algorithm Works

#### 1. Path Finding (Modified Dijkstra's Algorithm)
When a car enters the parking lot:
1. Starts at a random entry point on the perimeter
2. Uses weighted BFS to find the shortest path to the nearest empty parking space
3. Path cost = sum of all road segment weights in the path
4. Chooses the path with minimum total cost

#### 2. Weight Update System

**When path is chosen** (affects future cars):
- All road segments in the chosen path: **+1.5**
- This discourages other cars from using the same route

**When car enters a segment** (real-time):
- That specific segment: **+10.5**
- This prevents other cars from entering the same segment

**When car leaves a segment** (real-time):
- That specific segment: **-12**
- This opens up the segment for other cars
- Minimum weight is always 1.0

#### 3. Parking Space Reservation
1. **Empty (Green)**: Available for any car
2. **Reserved (Yellow)**: Assigned to a specific car (no other car can reserve it)
3. **Occupied (Red)**: Car has parked (no other car can use it)

### Example Scenario

```
Car A enters at top-left corner:
1. Algorithm finds shortest weighted path to nearest empty space
2. Space is marked YELLOW (reserved for Car A)
3. All segments in path get +1.5 weight
4. Car A starts moving

As Car A moves:
- Enters segment (0,0): weight becomes 1.0 + 10.5 = 11.5
- Moves to (0,1): 
  - (0,0) weight becomes 11.5 - 12 = 1.0 (can't go below 1.0)
  - (0,1) weight becomes 2.5 + 10.5 = 13.0
- Continues until reaching parking space
- Parking space turns RED (occupied)

Car B enters while Car A is moving:
- Sees updated weights (Car A's path has +1.5)
- Sees Car A's current segment has very high weight (10.5+)
- Algorithm naturally avoids Car A's route and current position
- Finds alternative path to different parking space
```

### Statistics Display

At the bottom of the window:
- **Cars in lot**: Number of cars currently moving
- **Parked cars**: Number of cars that have parked
- **Total cars spawned**: Total cars that have entered
- **Empty spaces**: Available parking spaces remaining

### Simulation Parameters

**Cars per minute**: You set this at startup
- Example: 10 cars/minute = 1 car every 6 seconds
- Example: 30 cars/minute = 1 car every 2 seconds
- Example: 60 cars/minute = 1 car every second

**Frame rate**: 60 FPS (smooth animation)

**Car movement**: Cars move every 10 frames (6 times per second)

### Key Features

✅ **No collisions**: Only one car per road segment at a time
✅ **No parking conflicts**: Each space can only be reserved/occupied by one car
✅ **Dynamic routing**: Later cars see updated weights and route around congestion
✅ **Realistic behavior**: Cars can't teleport or use parking spaces as roads
✅ **Fair distribution**: Weight system naturally distributes cars across the lot

### Tips for Testing

1. **Start with low rate** (5-10 cars/minute): Watch individual car behavior
2. **Increase gradually** (20-30 cars/minute): See how routing adapts to congestion
3. **Stress test** (60+ cars/minute): Watch the lot fill up and routing become more complex
4. **Watch the weights**: Grey road numbers show how traffic affects routing

### Understanding Weight Numbers

- **1.0**: Unused road segment
- **2.5-5.0**: Lightly used (1-2 cars have used this path)
- **5.0-10.0**: Moderately used (multiple cars have used this path)
- **10.0+**: Currently occupied by a car OR heavily used path

The weight system creates a natural "traffic flow" where cars avoid congested areas!

## Exiting the Simulation

Simply close the Pygame window. The simulation will terminate gracefully.
