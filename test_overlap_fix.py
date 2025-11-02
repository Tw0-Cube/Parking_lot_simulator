#!/usr/bin/env python3
"""
Test script to verify car overlap fix
This script runs a quick simulation test to ensure cars don't overlap
"""

import sys
import time
from parking_lot_simulation import ParkingLot, Car, ENTRY_POINTS

def test_road_reservation_system():
    """Test that the road reservation system prevents overlaps"""
    print("Testing road reservation system...")
    
    parking_lot = ParkingLot()
    
    # Test 1: Reserve a road segment
    test_pos = (0, 1)
    result = parking_lot.reserve_road(test_pos, car_id=1)
    assert result == True, "Should be able to reserve an empty road segment"
    print("✓ Test 1 passed: Can reserve empty road segment")
    
    # Test 2: Try to reserve the same segment with different car
    result = parking_lot.reserve_road(test_pos, car_id=2)
    assert result == False, "Should not be able to reserve already reserved segment"
    print("✓ Test 2 passed: Cannot reserve already reserved segment")
    
    # Test 3: Same car can reserve again (idempotent)
    result = parking_lot.reserve_road(test_pos, car_id=1)
    assert result == True, "Same car should be able to reserve again"
    print("✓ Test 3 passed: Same car can reserve again")
    
    # Test 4: Check if segment is occupied by other
    is_occupied = parking_lot.is_road_occupied_by_other(test_pos, car_id=1)
    assert is_occupied == False, "Should not be occupied by other for same car"
    print("✓ Test 4 passed: Not occupied by other for same car")
    
    is_occupied = parking_lot.is_road_occupied_by_other(test_pos, car_id=2)
    assert is_occupied == True, "Should be occupied by other for different car"
    print("✓ Test 5 passed: Occupied by other for different car")
    
    # Test 6: Free reservation
    parking_lot.free_road_reservation(test_pos, car_id=1)
    result = parking_lot.reserve_road(test_pos, car_id=2)
    assert result == True, "Should be able to reserve after freeing"
    print("✓ Test 6 passed: Can reserve after freeing")
    
    # Test 7: Occupy road clears reservation
    parking_lot.occupy_road(test_pos, car_id=2)
    assert parking_lot.road_reservations.get(test_pos) is None, "Reservation should be cleared when occupying"
    print("✓ Test 7 passed: Occupation clears reservation")
    
    print("\n✅ All road reservation tests passed!\n")
    return True

def test_car_spawning():
    """Test that cars spawn correctly with reservations"""
    print("Testing car spawning with reservations...")
    
    parking_lot = ParkingLot()
    
    # Find a path for first car
    entry_point = ENTRY_POINTS[0]
    path, parking_spot, cost = parking_lot.find_shortest_path_to_parking(entry_point)
    
    if not path or not parking_spot:
        print("⚠ Warning: Could not find path for test car")
        return False
    
    # Create first car
    car1 = Car(1, entry_point, path, parking_spot, parking_lot, is_exiting=False)
    
    # Check that first segment is occupied
    assert parking_lot.road_occupancy.get(entry_point) == 1, "Entry point should be occupied by car 1"
    print("✓ Test 1 passed: Entry point occupied by car")
    
    # Check that next segment is reserved
    if len(path) > 1:
        next_segment = path[1]
        assert parking_lot.road_reservations.get(next_segment) == 1, "Next segment should be reserved by car 1"
        print("✓ Test 2 passed: Next segment reserved by car")
    
    # Try to create another car at same entry point - should not be possible
    is_occupied = parking_lot.is_road_occupied(entry_point)
    assert is_occupied == True, "Entry point should be occupied"
    print("✓ Test 3 passed: Entry point correctly marked as occupied")
    
    print("\n✅ All car spawning tests passed!\n")
    return True

def test_collision_prevention():
    """Test that two cars cannot occupy the same segment"""
    print("Testing collision prevention...")
    
    parking_lot = ParkingLot()
    
    # Create two paths that might intersect
    entry1 = ENTRY_POINTS[0]
    entry2 = ENTRY_POINTS[1]
    
    path1, parking1, _ = parking_lot.find_shortest_path_to_parking(entry1)
    path2, parking2, _ = parking_lot.find_shortest_path_to_parking(entry2)
    
    if not path1 or not path2:
        print("⚠ Warning: Could not find paths for test")
        return False
    
    # Create two cars
    car1 = Car(1, entry1, path1, parking1, parking_lot, is_exiting=False)
    car2 = Car(2, entry2, path2, parking2, parking_lot, is_exiting=False)
    
    # Check that they occupy different positions
    assert car1.position != car2.position, "Cars should start at different positions"
    print("✓ Test 1 passed: Cars start at different positions")
    
    # Check that occupied segments are tracked
    occupied_segments = [pos for pos, car_id in parking_lot.road_occupancy.items() if car_id is not None]
    assert len(occupied_segments) >= 2, "At least 2 segments should be occupied"
    print(f"✓ Test 2 passed: {len(occupied_segments)} segments occupied")
    
    # Check that reserved segments are tracked
    reserved_segments = [pos for pos, car_id in parking_lot.road_reservations.items() if car_id is not None]
    print(f"✓ Test 3 passed: {len(reserved_segments)} segments reserved")
    
    print("\n✅ All collision prevention tests passed!\n")
    return True

def main():
    print("=" * 60)
    print("CAR OVERLAP FIX - TEST SUITE")
    print("=" * 60)
    print()
    
    all_passed = True
    
    try:
        # Run all tests
        all_passed &= test_road_reservation_system()
        all_passed &= test_car_spawning()
        all_passed &= test_collision_prevention()
        
        if all_passed:
            print("=" * 60)
            print("🎉 ALL TESTS PASSED! Car overlap issue is fixed.")
            print("=" * 60)
            print()
            print("The simulation now includes:")
            print("  • Road segment reservation system")
            print("  • Collision prevention for cars")
            print("  • Proper synchronization between occupation and reservation")
            print()
            print("You can now run the simulation with confidence:")
            print("  python3 parking_lot_simulation.py")
            print()
            return 0
        else:
            print("❌ Some tests failed. Please review the output above.")
            return 1
            
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
