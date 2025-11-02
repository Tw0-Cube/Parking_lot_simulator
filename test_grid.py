"""Test script to verify the parking lot grid structure"""

class ParkingLot:
    def __init__(self):
        self.grid = [[None for _ in range(31)] for _ in range(31)]
        self.parking_status = {}
        self.initialize_grid()
        
    def initialize_grid(self):
        """Initialize the 31x31 parking lot grid"""
        GRID_SIZE = 31
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                # First and last rows are roads
                if row == 0 or row == GRID_SIZE - 1:
                    self.grid[row][col] = 'road'
                # First and last columns are roads
                elif col == 0 or col == GRID_SIZE - 1:
                    self.grid[row][col] = 'road'
                else:
                    # Inside the perimeter: alternating pattern
                    # 2 parking rows, 1 road row, repeat
                    inner_row = row - 1
                    row_type = inner_row % 3
                    
                    if row_type == 2:  # Road row
                        self.grid[row][col] = 'road'
                    else:  # Parking row
                        # 5 parking spaces, 1 road segment, repeat
                        col_type = (col - 1) % 6
                        if col_type == 5:  # Road segment
                            self.grid[row][col] = 'road'
                        else:  # Parking space
                            self.grid[row][col] = 'parking'
                            self.parking_status[(row, col)] = 'empty'

def print_grid(parking_lot):
    """Print the grid structure"""
    print("\nParking Lot Grid (31x31):")
    print("1 = Road, * = Empty Parking\n")
    
    for row in range(31):
        line = ""
        for col in range(31):
            if parking_lot.grid[row][col] == 'road':
                line += "1 "
            else:
                line += "* "
        print(line)
    
    # Count statistics
    road_count = sum(1 for row in parking_lot.grid for cell in row if cell == 'road')
    parking_count = sum(1 for row in parking_lot.grid for cell in row if cell == 'parking')
    
    print(f"\nStatistics:")
    print(f"Total cells: {31 * 31}")
    print(f"Road segments: {road_count}")
    print(f"Parking spaces: {parking_count}")
    print(f"Total: {road_count + parking_count}")

if __name__ == "__main__":
    lot = ParkingLot()
    print_grid(lot)
