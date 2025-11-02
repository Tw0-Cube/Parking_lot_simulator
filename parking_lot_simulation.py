import pygame
import heapq
import random
import copy
from collections import deque
import sys

# Constants
GRID_SIZE = 31
CELL_SIZE = 25
WINDOW_WIDTH = GRID_SIZE * CELL_SIZE
WINDOW_HEIGHT = GRID_SIZE * CELL_SIZE + 100

# Colors
ROAD_COLOR = (128, 128, 128)  # Grey
EMPTY_PARKING_COLOR = (0, 255, 0)  # Green
RESERVED_PARKING_COLOR = (255, 255, 0)  # Yellow
OCCUPIED_PARKING_COLOR = (255, 0, 0)  # Red
CAR_COLOR = (0, 0, 255)  # Blue
TEXT_COLOR = (255, 255, 255)  # White
BLACK = (0, 0, 0)

class ParkingLot:
    def __init__(self):
        self.grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.road_weights = [[1.0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.parking_status = {}  # (row, col): 'empty', 'reserved', 'occupied'
        self.initialize_grid()
        
    def initialize_grid(self):
        """Initialize the 31x31 parking lot grid"""
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
    
    def get_entry_points(self):
        """Get all entry points (perimeter road segments)"""
        entry_points = []
        # Top row
        for col in range(GRID_SIZE):
            entry_points.append((0, col))
        # Bottom row
        for col in range(GRID_SIZE):
            entry_points.append((GRID_SIZE - 1, col))
        # Left column (excluding corners already added)
        for row in range(1, GRID_SIZE - 1):
            entry_points.append((row, 0))
        # Right column (excluding corners already added)
        for row in range(1, GRID_SIZE - 1):
            entry_points.append((row, GRID_SIZE - 1))
        return entry_points
    
    def get_neighbors(self, pos):
        """Get valid neighboring road segments"""
        row, col = pos
        neighbors = []
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < GRID_SIZE and 0 <= new_col < GRID_SIZE:
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
            if 0 <= new_row < GRID_SIZE and 0 <= new_col < GRID_SIZE:
                if self.grid[new_row][new_col] == 'parking':
                    parking_spaces.append((new_row, new_col))
        return parking_spaces
    
    def find_shortest_path_to_parking(self, start_pos):
        """Modified BFS with weights to find shortest path to closest empty parking"""
        # Priority queue: (cost, position, path)
        pq = [(0, start_pos, [start_pos])]
        visited = {start_pos: 0}
        
        while pq:
            cost, pos, path = heapq.heappop(pq)
            
            # Check if we can reach an empty parking space from this position
            adjacent_parking = self.get_adjacent_parking(pos)
            for parking_pos in adjacent_parking:
                if self.parking_status.get(parking_pos) == 'empty':
                    return path, parking_pos, cost
            
            # Explore neighbors
            for neighbor in self.get_neighbors(pos):
                new_cost = cost + self.road_weights[neighbor[0]][neighbor[1]]
                
                if neighbor not in visited or new_cost < visited[neighbor]:
                    visited[neighbor] = new_cost
                    new_path = path + [neighbor]
                    heapq.heappush(pq, (new_cost, neighbor, new_path))
        
        return None, None, float('inf')
    
    def reserve_parking(self, parking_pos):
        """Reserve a parking space"""
        if parking_pos in self.parking_status:
            self.parking_status[parking_pos] = 'reserved'
    
    def occupy_parking(self, parking_pos):
        """Occupy a parking space"""
        if parking_pos in self.parking_status:
            self.parking_status[parking_pos] = 'occupied'
    
    def update_path_weights(self, path):
        """Update road weights after path is chosen (increment by 1.5)"""
        for pos in path:
            if self.grid[pos[0]][pos[1]] == 'road':
                self.road_weights[pos[0]][pos[1]] += 1.5
    
    def increment_segment(self, pos):
        """Increment road segment when car enters (by 10.5)"""
        if self.grid[pos[0]][pos[1]] == 'road':
            self.road_weights[pos[0]][pos[1]] += 10.5
    
    def decrement_segment(self, pos):
        """Decrement road segment when car leaves (by 12)"""
        if self.grid[pos[0]][pos[1]] == 'road':
            self.road_weights[pos[0]][pos[1]] -= 12
            # Ensure weight doesn't go below 1
            self.road_weights[pos[0]][pos[1]] = max(1.0, self.road_weights[pos[0]][pos[1]])


class Car:
    def __init__(self, car_id, entry_point, path, parking_spot, parking_lot):
        self.id = car_id
        self.path = path
        self.parking_spot = parking_spot
        self.current_index = 0
        self.position = entry_point
        self.parking_lot = parking_lot
        self.state = 'moving'  # 'moving', 'parked'
        self.move_timer = 0
        self.move_delay = 10  # Frames between moves
        
    def update(self):
        """Update car position"""
        if self.state == 'parked':
            return
        
        self.move_timer += 1
        if self.move_timer < self.move_delay:
            return
        
        self.move_timer = 0
        
        if self.current_index < len(self.path):
            # Leave current segment
            if self.current_index > 0:
                self.parking_lot.decrement_segment(self.position)
            
            # Move to next position
            self.position = self.path[self.current_index]
            self.current_index += 1
            
            # Enter new segment
            if self.current_index < len(self.path):
                self.parking_lot.increment_segment(self.position)
        else:
            # Reached destination
            self.parking_lot.decrement_segment(self.position)
            self.parking_lot.occupy_parking(self.parking_spot)
            self.state = 'parked'
            self.position = self.parking_spot


class Simulation:
    def __init__(self, cars_per_minute):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Parking Lot Simulation")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 20)
        self.small_font = pygame.font.Font(None, 16)
        
        self.parking_lot = ParkingLot()
        self.cars = []
        self.car_counter = 0
        self.cars_per_minute = cars_per_minute
        self.spawn_rate = 60 / cars_per_minute if cars_per_minute > 0 else float('inf')
        self.spawn_timer = 0
        self.running = True
        
        self.entry_points = self.parking_lot.get_entry_points()
        
    def spawn_car(self):
        """Spawn a new car at a random entry point"""
        # Check if there are empty parking spaces
        empty_spaces = [pos for pos, status in self.parking_lot.parking_status.items() 
                       if status == 'empty']
        if not empty_spaces:
            return
        
        # Choose random entry point
        entry_point = random.choice(self.entry_points)
        
        # Find shortest path to parking
        path, parking_spot, cost = self.parking_lot.find_shortest_path_to_parking(entry_point)
        
        if path and parking_spot:
            # Reserve the parking spot
            self.parking_lot.reserve_parking(parking_spot)
            
            # Update path weights
            self.parking_lot.update_path_weights(path)
            
            # Create car
            car = Car(self.car_counter, entry_point, path, parking_spot, self.parking_lot)
            self.cars.append(car)
            self.car_counter += 1
    
    def draw(self):
        """Draw the parking lot and cars"""
        self.screen.fill(BLACK)
        
        # Draw grid
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                x = col * CELL_SIZE
                y = row * CELL_SIZE
                
                if self.parking_lot.grid[row][col] == 'road':
                    # Draw road with weight
                    pygame.draw.rect(self.screen, ROAD_COLOR, (x, y, CELL_SIZE, CELL_SIZE))
                    weight = self.parking_lot.road_weights[row][col]
                    text = self.small_font.render(f"{weight:.1f}", True, TEXT_COLOR)
                    text_rect = text.get_rect(center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2))
                    self.screen.blit(text, text_rect)
                elif self.parking_lot.grid[row][col] == 'parking':
                    status = self.parking_lot.parking_status.get((row, col), 'empty')
                    if status == 'empty':
                        color = EMPTY_PARKING_COLOR
                    elif status == 'reserved':
                        color = RESERVED_PARKING_COLOR
                    else:  # occupied
                        color = OCCUPIED_PARKING_COLOR
                    pygame.draw.rect(self.screen, color, (x, y, CELL_SIZE, CELL_SIZE))
                
                # Draw grid lines
                pygame.draw.rect(self.screen, BLACK, (x, y, CELL_SIZE, CELL_SIZE), 1)
        
        # Draw cars
        for car in self.cars:
            if car.state == 'moving':
                x = car.position[1] * CELL_SIZE + CELL_SIZE // 2
                y = car.position[0] * CELL_SIZE + CELL_SIZE // 2
                pygame.draw.circle(self.screen, CAR_COLOR, (x, y), CELL_SIZE // 3)
        
        # Draw statistics
        stats_y = GRID_SIZE * CELL_SIZE + 10
        stats = [
            f"Cars in lot: {len([c for c in self.cars if c.state == 'moving'])}",
            f"Parked cars: {len([c for c in self.cars if c.state == 'parked'])}",
            f"Total cars spawned: {self.car_counter}",
            f"Empty spaces: {len([s for s in self.parking_lot.parking_status.values() if s == 'empty'])}"
        ]
        
        for i, stat in enumerate(stats):
            text = self.font.render(stat, True, TEXT_COLOR)
            self.screen.blit(text, (10, stats_y + i * 20))
        
        pygame.display.flip()
    
    def run(self):
        """Main simulation loop"""
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            # Spawn cars
            self.spawn_timer += 1
            if self.spawn_timer >= self.spawn_rate:
                self.spawn_car()
                self.spawn_timer = 0
            
            # Update cars
            for car in self.cars:
                car.update()
            
            # Draw
            self.draw()
            
            # Control frame rate
            self.clock.tick(60)
        
        pygame.quit()


def main():
    print("=" * 50)
    print("PARKING LOT SIMULATION")
    print("=" * 50)
    print("\nThis simulation uses a 31x31 grid with:")
    print("- Grey roads with weight numbers")
    print("- Green = Empty parking spaces")
    print("- Yellow = Reserved parking spaces")
    print("- Red = Occupied parking spaces")
    print("- Blue circles = Cars in motion")
    print("\n" + "=" * 50)
    
    while True:
        try:
            cars_per_minute = int(input("\nHow many cars should enter the lot per minute? "))
            if cars_per_minute <= 0:
                print("Please enter a positive number.")
                continue
            break
        except ValueError:
            print("Please enter a valid number.")
    
    print(f"\nStarting simulation with {cars_per_minute} cars per minute...")
    print("Close the window to exit the simulation.\n")
    
    sim = Simulation(cars_per_minute)
    sim.run()


if __name__ == "__main__":
    main()
