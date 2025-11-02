#!/usr/bin/env python3
"""
Visual verification script to demonstrate no car overlaps
This runs a simulation check without GUI to verify collision prevention
"""

import sys
from parking_lot_simulation import ParkingLot, Car, ENTRY_POINTS

def simulate_steps(parking_lot, cars, steps=100):
    """Simulate a number of steps and check for overlaps"""
    overlaps_detected = []
    
    for step in range(steps):
        # Update all cars
        for car in cars:
            if car.state not in ['parked', 'exited']:
                car.update()
        
        # Check for overlaps
        occupied_positions = {}
        for car in cars:
            if car.state in ['entering', 'exiting', 'waiting']:
                pos = car.position
                if pos in occupied_positions:
                    overlaps_detected.append({
                        'step': step,
                        'position': pos,
                        'car1': occupied_positions[pos],
                        'car2': car.id
                    })
                else:
                    occupied_positions[pos] = car.id
        
        # Remove exited cars
        cars[:] = [car for car in cars if car.state != 'exited']
    
    return overlaps_detected

def main():
    print("=" * 60)
    print("VISUAL VERIFICATION - NO CAR OVERLAPS")
    print("=" * 60)
    print()
    
    parking_lot = ParkingLot()
    cars = []
    
    # Spawn multiple cars at different entry points
    print("Spawning test cars...")
    car_id = 0
    for entry_point in ENTRY_POINTS[:2]:  # Use first 2 entry points
        path, parking_spot, cost = parking_lot.find_shortest_path_to_parking(entry_point)
        if path and parking_spot:
            parking_lot.reserve_parking(parking_spot)
            parking_lot.update_path_weights(path, 1.5)
            car = Car(car_id, entry_point, path, parking_spot, parking_lot, is_exiting=False)
            cars.append(car)
            print(f"  ✓ Car {car_id} spawned at {entry_point}")
            car_id += 1
    
    print(f"\nTotal cars spawned: {len(cars)}")
    print("\nSimulating 100 steps...")
    
    # Run simulation
    overlaps = simulate_steps(parking_lot, cars, steps=100)
    
    print(f"\nSimulation complete!")
    print(f"Steps simulated: 100")
    print(f"Overlaps detected: {len(overlaps)}")
    
    if len(overlaps) == 0:
        print("\n" + "=" * 60)
        print("✅ SUCCESS! No car overlaps detected!")
        print("=" * 60)
        print()
        print("The fix is working correctly:")
        print("  • Cars reserve segments before moving")
        print("  • Multiple cars cannot target the same segment")
        print("  • Collision detection prevents overlaps")
        print()
        return 0
    else:
        print("\n" + "=" * 60)
        print("❌ OVERLAPS DETECTED!")
        print("=" * 60)
        for overlap in overlaps[:5]:  # Show first 5
            print(f"  Step {overlap['step']}: Cars {overlap['car1']} and {overlap['car2']} at {overlap['position']}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
