"""
Demo script showing the pathfinding algorithm without GUI
This demonstrates how the weighted BFS works
"""

import heapq

class SimpleParkingLot:
    def __init__(self):
        self.grid = [[None for _ in range(31)] for _ in range(31)]
        self.road_weights = [[1.0 for _ in range(31)] for _ in range(31)]
        self.parking_status = {}
        self.initialize_grid()
        
    def initialize_grid(self):
        """Initialize the 31x31 parking lot grid"""
        GRID_SIZE = 31
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if row == 0 or row == GRID_SIZE - 1:
                    self.grid[row][col] = 'road'
                elif col == 0 or col == GRID_SIZE - 1:
                    self.grid[row][col] = 'road'
                else:
                    inner_row = row - 1
                    row_type = inner_row % 3
                    
                    if row_type == 2:
                        self.grid[row][col] = 'road'
                    else:
                        col_type = (col - 1) % 6
                        if col_type == 5:
                            self.grid[row][col] = 'road'
                        else:
                            self.grid[row][col] = 'parking'
                            self.parking_status[(row, col)] = 'empty'
    
    def get_neighbors(self, pos):
        """Get valid neighboring road segments"""
        row, col = pos
        neighbors = []
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 31 and 0 <= new_col < 31:
                if self.grid[new_row][new_col] == 'road':
                    neighbors.append((new_row, new_col))
        return neighbors
    
    def get_adjacent_parking(self, pos):
        """Get adjacent parking spaces from a road position"""
        row, col = pos
        parking_spaces = []
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 31 and 0 <= new_col < 31:
                if self.grid[new_row][new_col] == 'parking':
                    parking_spaces.append((new_row, new_col))
        return parking_spaces
    
    def find_shortest_path_to_parking(self, start_pos):
        """Modified BFS with weights to find shortest path to closest empty parking"""
        pq = [(0, start_pos, [start_pos])]
        visited = {start_pos: 0}
        
        while pq:
            cost, pos, path = heapq.heappop(pq)
            
            adjacent_parking = self.get_adjacent_parking(pos)
            for parking_pos in adjacent_parking:
                if self.parking_status.get(parking_pos) == 'empty':
                    return path, parking_pos, cost
            
            for neighbor in self.get_neighbors(pos):
                new_cost = cost + self.road_weights[neighbor[0]][neighbor[1]]
                
                if neighbor not in visited or new_cost < visited[neighbor]:
                    visited[neighbor] = new_cost
                    new_path = path + [neighbor]
                    heapq.heappush(pq, (new_cost, neighbor, new_path))
        
        return None, None, float('inf')
    
    def update_path_weights(self, path):
        """Update road weights after path is chosen"""
        for pos in path:
            if self.grid[pos[0]][pos[1]] == 'road':
                self.road_weights[pos[0]][pos[1]] += 1.5

def main():
    print("=" * 70)
    print("PARKING LOT PATHFINDING DEMO")
    print("=" * 70)
    
    lot = SimpleParkingLot()
    
    print(f"\nGrid initialized:")
    print(f"  - Total parking spaces: {len(lot.parking_status)}")
    print(f"  - All weights start at: 1.0")
    
    # Simulate 3 cars
    entry_points = [(0, 0), (0, 15), (0, 30)]
    
    for i, entry in enumerate(entry_points, 1):
        print(f"\n{'=' * 70}")
        print(f"CAR {i}: Entering at position {entry}")
        print(f"{'=' * 70}")
        
        path, parking, cost = lot.find_shortest_path_to_parking(entry)
        
        if path and parking:
            print(f"✓ Found parking space at: {parking}")
            print(f"✓ Path length: {len(path)} segments")
            print(f"✓ Total path cost: {cost:.2f}")
            print(f"✓ Path: {' → '.join([f'({r},{c})' for r, c in path[:5]])}{'...' if len(path) > 5 else ''}")
            
            # Reserve parking and update weights
            lot.parking_status[parking] = 'reserved'
            lot.update_path_weights(path)
            
            print(f"\n  Weight updates applied:")
            print(f"  - All {len(path)} segments in path increased by 1.5")
            print(f"  - Parking space {parking} marked as RESERVED")
            
            # Show some weight examples
            if len(path) >= 3:
                print(f"\n  Sample weights after Car {i}:")
                for j, pos in enumerate(path[:3]):
                    weight = lot.road_weights[pos[0]][pos[1]]
                    print(f"    Segment {pos}: {weight:.1f}")
        else:
            print(f"✗ No parking space found!")
    
    print(f"\n{'=' * 70}")
    print("SUMMARY")
    print(f"{'=' * 70}")
    
    reserved = sum(1 for status in lot.parking_status.values() if status == 'reserved')
    empty = sum(1 for status in lot.parking_status.values() if status == 'empty')
    
    print(f"Reserved spaces: {reserved}")
    print(f"Empty spaces: {empty}")
    print(f"Total spaces: {len(lot.parking_status)}")
    
    # Show weight distribution
    all_weights = [lot.road_weights[r][c] for r in range(31) for c in range(31) 
                   if lot.grid[r][c] == 'road']
    avg_weight = sum(all_weights) / len(all_weights)
    max_weight = max(all_weights)
    
    print(f"\nRoad weight statistics:")
    print(f"  Average weight: {avg_weight:.2f}")
    print(f"  Maximum weight: {max_weight:.2f}")
    print(f"  Minimum weight: 1.0")
    
    print(f"\n{'=' * 70}")
    print("This demonstrates how the algorithm finds optimal paths and updates")
    print("weights to influence future car routing. In the full simulation,")
    print("weights also change dynamically as cars move (+10.5 entry, -12 exit).")
    print(f"{'=' * 70}\n")

if __name__ == "__main__":
    main()
