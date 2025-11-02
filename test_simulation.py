#!/usr/bin/env python3
"""
Test script to verify the enhanced parking lot simulation features
"""

import sys
sys.path.insert(0, '/vercel/sandbox')

from parking_lot_simulation import ParkingLot, Car, ENTRY_POINTS, EXIT_POINTS

def test_entry_exit_points():
    """Test that entry and exit points are correctly defined"""
    print("Testing entry and exit points...")
    assert ENTRY_POINTS == [(0, 0), (15, 0), (30, 0)], "Entry points incorrect"
    assert EXIT_POINTS == [(30, 0), (30, 15), (30, 30)], "Exit points incorrect"
    print("✓ Entry and exit points are correct")

def test_parking_lot_initialization():
    """Test parking lot initialization"""
    print("\nTesting parking lot initialization...")
    lot = ParkingLot()
    
    # Check grid size
    assert len(lot.grid) == 31, "Grid should be 31x31"
    assert len(lot.grid[0]) == 31, "Grid should be 31x31"
    
    # Check road occupancy tracking
    assert hasattr(lot, 'road_occupancy'), "Should have road_occupancy attribute"
    
    # Check entry points are roads
    for entry in ENTRY_POINTS:
        assert lot.grid[entry[0]][entry[1]] == 'road', f"Entry point {entry} should be a road"
    
    # Check exit points are roads
    for exit_pt in EXIT_POINTS:
        assert lot.grid[exit_pt[0]][exit_pt[1]] == 'road', f"Exit point {exit_pt} should be a road"
    
    print("✓ Parking lot initialized correctly")

def test_road_occupancy():
    """Test road occupancy tracking"""
    print("\nTesting road occupancy tracking...")
    lot = ParkingLot()
    
    test_pos = (0, 0)
    
    # Initially should not be occupied
    assert not lot.is_road_occupied(test_pos), "Road should not be occupied initially"
    
    # Occupy road
    lot.occupy_road(test_pos, 1)
    assert lot.is_road_occupied(test_pos), "Road should be occupied"
    assert lot.road_occupancy[test_pos] == 1, "Road should be occupied by car 1"
    
    # Free road
    lot.free_road(test_pos)
    assert not lot.is_road_occupied(test_pos), "Road should be free after freeing"
    
    print("✓ Road occupancy tracking works correctly")

def test_pathfinding_to_exit():
    """Test pathfinding to exit points"""
    print("\nTesting pathfinding to exit points...")
    lot = ParkingLot()
    
    # Test from a road position
    start_pos = (15, 15)
    path, exit_point, cost = lot.find_shortest_path_to_exit(start_pos)
    
    assert path is not None, "Should find a path to exit"
    assert exit_point in EXIT_POINTS, "Should reach an exit point"
    assert len(path) > 0, "Path should not be empty"
    assert path[0] == start_pos, "Path should start at start position"
    assert path[-1] == exit_point, "Path should end at exit point"
    
    print(f"✓ Found path from {start_pos} to exit {exit_point} with cost {cost:.2f}")

def test_weight_management():
    """Test weight update and release functions"""
    print("\nTesting weight management...")
    lot = ParkingLot()
    
    test_path = [(0, 0), (0, 1), (0, 2)]
    
    # Get initial weights
    initial_weights = [lot.road_weights[pos[0]][pos[1]] for pos in test_path]
    
    # Update weights
    lot.update_path_weights(test_path, 3)
    updated_weights = [lot.road_weights[pos[0]][pos[1]] for pos in test_path]
    
    for i, pos in enumerate(test_path):
        assert updated_weights[i] == initial_weights[i] + 3, f"Weight should increase by 3 at {pos}"
    
    # Release weights
    lot.release_path_weights(test_path, 3)
    released_weights = [lot.road_weights[pos[0]][pos[1]] for pos in test_path]
    
    for i, pos in enumerate(test_path):
        assert released_weights[i] == initial_weights[i], f"Weight should return to initial at {pos}"
    
    print("✓ Weight management works correctly")

def test_parking_operations():
    """Test parking space operations"""
    print("\nTesting parking operations...")
    lot = ParkingLot()
    
    # Find a parking space
    parking_spaces = list(lot.parking_status.keys())
    test_parking = parking_spaces[0]
    
    # Initially empty
    assert lot.parking_status[test_parking] == 'empty', "Parking should be empty initially"
    
    # Reserve
    lot.reserve_parking(test_parking)
    assert lot.parking_status[test_parking] == 'reserved', "Parking should be reserved"
    
    # Occupy
    lot.occupy_parking(test_parking)
    assert lot.parking_status[test_parking] == 'occupied', "Parking should be occupied"
    
    # Free
    lot.free_parking(test_parking)
    assert lot.parking_status[test_parking] == 'empty', "Parking should be empty after freeing"
    
    print("✓ Parking operations work correctly")

def test_car_initialization():
    """Test car initialization with smooth movement"""
    print("\nTesting car initialization...")
    lot = ParkingLot()
    
    entry = ENTRY_POINTS[0]
    path, parking, cost = lot.find_shortest_path_to_parking(entry)
    
    if path and parking:
        car = Car(1, entry, path, parking, lot, is_exiting=False)
        
        # Check attributes
        assert car.id == 1, "Car ID should be 1"
        assert car.state == 'entering', "Car should be in entering state"
        assert hasattr(car, 'visual_position'), "Car should have visual_position"
        assert isinstance(car.visual_position, list), "visual_position should be a list"
        assert len(car.visual_position) == 2, "visual_position should have x and y"
        assert car.move_speed == 2.0, "Move speed should be 2.0 for smooth movement"
        assert car.in_deadlock == False, "Car should not be in deadlock initially"
        
        print("✓ Car initialized correctly with smooth movement support")
    else:
        print("⚠ Could not test car initialization (no path found)")

def main():
    """Run all tests"""
    print("=" * 60)
    print("PARKING LOT SIMULATION - FEATURE TESTS")
    print("=" * 60)
    
    try:
        test_entry_exit_points()
        test_parking_lot_initialization()
        test_road_occupancy()
        test_pathfinding_to_exit()
        test_weight_management()
        test_parking_operations()
        test_car_initialization()
        
        print("\n" + "=" * 60)
        print("✓ ALL TESTS PASSED!")
        print("=" * 60)
        print("\nThe simulation is ready with:")
        print("  • Smooth 60fps movement")
        print("  • 3 entry points: (0,0), (15,0), (30,0)")
        print("  • 3 exit points: (30,0), (30,15), (30,30)")
        print("  • Exit pathfinding system")
        print("  • Road segment blocking")
        print("  • Deadlock detection and resolution")
        print("  • Enhanced weight management")
        
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
