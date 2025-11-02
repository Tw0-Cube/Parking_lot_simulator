import pygame
import heapq
import random
import copy
from collections import deque, defaultdict
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
EXIT_CAR_COLOR = (255, 165, 0)  # Orange for exiting cars
TEXT_COLOR = (255, 255, 255)  # White
BLACK = (0, 0, 0)

# Entry and Exit points
ENTRY_POINTS = [(0, 0), (15, 0), (30, 0)]
EXIT_POINTS = [(30, 0), (30, 15), (30, 30)]

# Deadlock detection
DEADLOCK_THRESHOLD = 180  # 3 seconds at 60fps

class ParkingLot:
    def __init__(self):
        self.grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.road_weights = [[1.0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.parking_status = {}  # (row, col): 'empty', 'reserved', 'occupied'
        self.road_occupancy = {}  # (row, col): car_id or None
        self.road_reservations = {}  # (row, col): car_id or None - prevents multiple cars targeting same segment
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
    
    def is_road_occupied(self, pos):
        """Check if a road segment is occupied or reserved by another car"""
        return self.road_occupancy.get(pos) is not None or self.road_reservations.get(pos) is not None
    
    def is_road_occupied_by_other(self, pos, car_id):
        """Check if a road segment is occupied or reserved by a different car"""
        occupant = self.road_occupancy.get(pos)
        reserver = self.road_reservations.get(pos)
        return (occupant is not None and occupant != car_id) or (reserver is not None and reserver != car_id)
    
    def occupy_road(self, pos, car_id):
        """Mark a road segment as occupied by a car"""
        if self.grid[pos[0]][pos[1]] == 'road':
            self.road_occupancy[pos] = car_id
            # Clear reservation when actually occupying
            if pos in self.road_reservations and self.road_reservations[pos] == car_id:
                self.road_reservations[pos] = None
    
    def free_road(self, pos):
        """Free a road segment"""
        if pos in self.road_occupancy:
            self.road_occupancy[pos] = None
    
    def reserve_road(self, pos, car_id):
        """Reserve a road segment for a car to prevent conflicts"""
        if self.grid[pos[0]][pos[1]] == 'road':
            # Only reserve if not already occupied or reserved by another car
            if not self.is_road_occupied_by_other(pos, car_id):
                self.road_reservations[pos] = car_id
                return True
        return False
    
    def free_road_reservation(self, pos, car_id):
        """Free a road segment reservation"""
        if pos in self.road_reservations and self.road_reservations[pos] == car_id:
            self.road_reservations[pos] = None
    
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
    
    def find_shortest_path_to_parking(self, start_pos, exclude_parking=False):
        """Modified BFS with weights to find shortest path to closest empty parking"""
        # Priority queue: (cost, position, path)
        pq = [(0, start_pos, [start_pos])]
        visited = {start_pos: 0}
        
        while pq:
            cost, pos, path = heapq.heappop(pq)
            
            # Check if we can reach an empty parking space from this position
            if not exclude_parking:
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
    
    def find_shortest_path_to_exit(self, start_pos):
        """Find shortest path from parking to nearest exit point"""
        # Priority queue: (cost, position, path)
        pq = [(0, start_pos, [start_pos])]
        visited = {start_pos: 0}
        
        while pq:
            cost, pos, path = heapq.heappop(pq)
            
            # Check if we reached an exit point
            if pos in EXIT_POINTS:
                return path, pos, cost
            
            # Explore neighbors (only roads, no parking spaces)
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
    
    def free_parking(self, parking_pos):
        """Free a parking space"""
        if parking_pos in self.parking_status:
            self.parking_status[parking_pos] = 'empty'
    
    def update_path_weights(self, path, increment=1.5):
        """Update road weights after path is chosen"""
        for pos in path:
            if self.grid[pos[0]][pos[1]] == 'road':
                self.road_weights[pos[0]][pos[1]] += increment
    
    def release_path_weights(self, path, decrement=1.5):
        """Release road weights when path is abandoned"""
        for pos in path:
            if self.grid[pos[0]][pos[1]] == 'road':
                self.road_weights[pos[0]][pos[1]] -= decrement
                self.road_weights[pos[0]][pos[1]] = max(1.0, self.road_weights[pos[0]][pos[1]])
    
    def increment_segment(self, pos, increment=10.5):
        """Increment road segment when car enters"""
        if self.grid[pos[0]][pos[1]] == 'road':
            self.road_weights[pos[0]][pos[1]] += increment
    
    def decrement_segment(self, pos, decrement=12):
        """Decrement road segment when car leaves"""
        if self.grid[pos[0]][pos[1]] == 'road':
            self.road_weights[pos[0]][pos[1]] -= decrement
            # Ensure weight doesn't go below 1
            self.road_weights[pos[0]][pos[1]] = max(1.0, self.road_weights[pos[0]][pos[1]])


class Car:
    def __init__(self, car_id, entry_point, path, destination, parking_lot, is_exiting=False):
        self.id = car_id
        self.path = path
        self.destination = destination  # parking spot or exit point
        self.current_path_index = 0
        self.position = entry_point  # Grid position (row, col)
        self.visual_position = [entry_point[1] * CELL_SIZE + CELL_SIZE // 2, 
                               entry_point[0] * CELL_SIZE + CELL_SIZE // 2]  # [x, y] for smooth rendering
        self.parking_lot = parking_lot
        self.state = 'entering' if not is_exiting else 'exiting'  # 'entering', 'parked', 'exiting', 'waiting'
        self.parking_duration = random.randint(300, 900)  # 5-15 seconds at 60fps
        self.parked_timer = 0
        self.is_exiting = is_exiting
        self.waiting_timer = 0
        self.target_segment = None
        self.move_speed = 2.0  # Pixels per frame for smooth movement
        self.in_deadlock = False
        self.original_path = None
        self.original_destination = None
        
        # Occupy initial position and reserve next segment
        if self.path and len(self.path) > 0:
            self.parking_lot.occupy_road(self.position, self.id)
            if len(self.path) > 1:
                self.target_segment = self.path[1]
                # Reserve the next segment to prevent other cars from targeting it
                self.parking_lot.reserve_road(self.target_segment, self.id)
        
    def update(self):
        """Update car position with smooth movement"""
        if self.state == 'parked':
            self.parked_timer += 1
            if self.parked_timer >= self.parking_duration:
                # Time to exit
                self.start_exit()
            return
        
        if self.state == 'waiting':
            self.waiting_timer += 1
            # Check if target segment is now free
            if self.target_segment and not self.parking_lot.is_road_occupied_by_other(self.target_segment, self.id):
                # Try to reserve the segment
                if self.parking_lot.reserve_road(self.target_segment, self.id):
                    self.state = 'entering' if not self.is_exiting else 'exiting'
                    self.waiting_timer = 0
            return
        
        # Calculate target visual position
        if self.current_path_index < len(self.path):
            target_grid_pos = self.path[self.current_path_index]
            target_visual_x = target_grid_pos[1] * CELL_SIZE + CELL_SIZE // 2
            target_visual_y = target_grid_pos[0] * CELL_SIZE + CELL_SIZE // 2
            
            # Calculate distance
            dx = target_visual_x - self.visual_position[0]
            dy = target_visual_y - self.visual_position[1]
            distance = (dx**2 + dy**2)**0.5
            
            if distance < self.move_speed:
                # Reached target grid position
                self.visual_position[0] = target_visual_x
                self.visual_position[1] = target_visual_y
                
                # Free previous road segment
                self.parking_lot.free_road(self.position)
                self.parking_lot.decrement_segment(self.position, 12 if not self.in_deadlock else 24)
                
                # Update grid position
                self.position = target_grid_pos
                self.current_path_index += 1
                
                # Check if we have more segments to traverse
                if self.current_path_index < len(self.path):
                    self.target_segment = self.path[self.current_path_index]
                    
                    # Check if next segment is occupied or reserved by another car
                    if self.parking_lot.is_road_occupied_by_other(self.target_segment, self.id):
                        self.state = 'waiting'
                        self.parking_lot.occupy_road(self.position, self.id)
                        self.parking_lot.increment_segment(self.position, 10.5 if not self.in_deadlock else 21)
                    else:
                        # Reserve next segment and occupy current segment
                        self.parking_lot.reserve_road(self.target_segment, self.id)
                        self.parking_lot.occupy_road(self.position, self.id)
                        self.parking_lot.increment_segment(self.position, 10.5 if not self.in_deadlock else 21)
                else:
                    # Reached final destination
                    self.reach_destination()
            else:
                # Move towards target
                self.visual_position[0] += (dx / distance) * self.move_speed
                self.visual_position[1] += (dy / distance) * self.move_speed
        else:
            # Path completed
            if self.state != 'parked':
                self.reach_destination()
    
    def reach_destination(self):
        """Handle reaching the destination"""
        # Clean up any remaining reservations
        if self.target_segment:
            self.parking_lot.free_road_reservation(self.target_segment, self.id)
            self.target_segment = None
        
        if self.is_exiting:
            # Car exits the lot
            self.state = 'exited'
        else:
            # Car parks
            self.parking_lot.occupy_parking(self.destination)
            self.state = 'parked'
            self.position = self.destination
            self.visual_position = [self.destination[1] * CELL_SIZE + CELL_SIZE // 2,
                                   self.destination[0] * CELL_SIZE + CELL_SIZE // 2]
    
    def start_exit(self):
        """Start the exit process"""
        # Find path to nearest exit
        # First, find adjacent road segment
        adjacent_roads = self.parking_lot.get_neighbors(self.destination)
        if not adjacent_roads:
            return
        
        # Find best exit path from adjacent roads
        best_path = None
        best_exit = None
        best_cost = float('inf')
        
        for road_pos in adjacent_roads:
            path, exit_point, cost = self.parking_lot.find_shortest_path_to_exit(road_pos)
            if path and cost < best_cost:
                best_path = path
                best_exit = exit_point
                best_cost = cost
        
        if best_path and best_exit:
            # Free parking space
            self.parking_lot.free_parking(self.destination)
            
            # Set up exit path
            self.path = best_path
            self.destination = best_exit
            self.current_path_index = 0
            self.position = best_path[0]
            self.visual_position = [self.position[1] * CELL_SIZE + CELL_SIZE // 2,
                                   self.position[0] * CELL_SIZE + CELL_SIZE // 2]
            self.is_exiting = True
            self.state = 'exiting'
            self.target_segment = best_path[1] if len(best_path) > 1 else None
            
            # Reserve path
            self.parking_lot.update_path_weights(best_path, 1.5)
            
            # Occupy first segment and reserve next
            self.parking_lot.occupy_road(self.position, self.id)
            self.parking_lot.increment_segment(self.position, 10.5)
            if self.target_segment:
                self.parking_lot.reserve_road(self.target_segment, self.id)


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
        self.deadlock_check_timer = 0
        self.total_deadlocks_resolved = 0
        
    def spawn_car(self):
        """Spawn a new car at a fixed entry point"""
        # Check if there are empty parking spaces
        empty_spaces = [pos for pos, status in self.parking_lot.parking_status.items() 
                       if status == 'empty']
        if not empty_spaces:
            return
        
        # Try each entry point until we find an available one
        available_entries = [ep for ep in ENTRY_POINTS if not self.parking_lot.is_road_occupied(ep)]
        if not available_entries:
            return
        
        # Choose random entry point from available entry points
        entry_point = random.choice(available_entries)
        
        # Find shortest path to parking
        path, parking_spot, cost = self.parking_lot.find_shortest_path_to_parking(entry_point)
        
        if path and parking_spot:
            # Verify the first segment of the path is available
            if len(path) > 1 and self.parking_lot.is_road_occupied(path[1]):
                return
            
            # Reserve the parking spot
            self.parking_lot.reserve_parking(parking_spot)
            
            # Update path weights
            self.parking_lot.update_path_weights(path, 1.5)
            
            # Create car
            car = Car(self.car_counter, entry_point, path, parking_spot, self.parking_lot, is_exiting=False)
            self.cars.append(car)
            self.car_counter += 1
    
    def detect_deadlock(self):
        """Detect if there's a deadlock among waiting cars"""
        waiting_cars = [car for car in self.cars if car.state == 'waiting' and car.waiting_timer > DEADLOCK_THRESHOLD]
        
        if len(waiting_cars) < 2:
            return []
        
        # Build dependency graph: car -> car it's waiting for
        dependencies = {}
        for car in waiting_cars:
            if car.target_segment:
                blocking_car_id = self.parking_lot.road_occupancy.get(car.target_segment)
                if blocking_car_id is not None:
                    blocking_car = next((c for c in self.cars if c.id == blocking_car_id), None)
                    if blocking_car and blocking_car.state == 'waiting':
                        dependencies[car.id] = blocking_car.id
        
        # Detect cycles using DFS
        def has_cycle(car_id, visited, rec_stack):
            visited.add(car_id)
            rec_stack.add(car_id)
            
            if car_id in dependencies:
                neighbor = dependencies[car_id]
                if neighbor not in visited:
                    if has_cycle(neighbor, visited, rec_stack):
                        return True
                elif neighbor in rec_stack:
                    return True
            
            rec_stack.remove(car_id)
            return False
        
        # Find all cars in deadlock
        deadlocked_cars = []
        visited = set()
        
        for car in waiting_cars:
            if car.id not in visited:
                rec_stack = set()
                if has_cycle(car.id, visited, rec_stack):
                    # Find all cars in the cycle
                    cycle_cars = [c for c in waiting_cars if c.id in visited]
                    deadlocked_cars.extend(cycle_cars)
                    break
        
        return deadlocked_cars
    
    def count_empty_neighbors(self, car):
        """Count how many empty road segments are accessible from car's position"""
        neighbors = self.parking_lot.get_neighbors(car.position)
        empty_count = sum(1 for n in neighbors if not self.parking_lot.is_road_occupied(n))
        return empty_count
    
    def resolve_deadlock(self, deadlocked_cars):
        """Resolve deadlock by rerouting cars with priority"""
        if not deadlocked_cars:
            return
        
        # Sort by number of empty neighbors (descending)
        deadlocked_cars.sort(key=lambda c: self.count_empty_neighbors(c), reverse=True)
        
        for car in deadlocked_cars:
            # Store original path and destination
            car.original_path = car.path.copy()
            car.original_destination = car.destination
            
            # Release old path weights and reservations
            remaining_path = car.path[car.current_path_index:]
            self.parking_lot.release_path_weights(remaining_path, 1.5)
            
            # Clear any existing target segment reservation
            if car.target_segment:
                self.parking_lot.free_road_reservation(car.target_segment, car.id)
            
            # Find new destination
            if car.is_exiting:
                # Find next closest exit
                best_path = None
                best_exit = None
                best_cost = float('inf')
                
                for exit_point in EXIT_POINTS:
                    if exit_point == car.original_destination:
                        continue
                    path, exit_pt, cost = self.parking_lot.find_shortest_path_to_exit(car.position)
                    if path and exit_pt == exit_point and cost < best_cost:
                        best_path = path
                        best_exit = exit_point
                        best_cost = cost
                
                if best_path and best_exit:
                    car.path = best_path
                    car.destination = best_exit
                    car.current_path_index = 0
                    car.target_segment = best_path[1] if len(best_path) > 1 else None
                    car.state = 'exiting'
                    car.waiting_timer = 0
                    car.in_deadlock = True
                    
                    # Reserve new path with higher weight
                    self.parking_lot.update_path_weights(best_path, 3)
                    
                    # Reserve next segment
                    if car.target_segment:
                        self.parking_lot.reserve_road(car.target_segment, car.id)
            else:
                # Find next closest empty parking
                best_path = None
                best_parking = None
                best_cost = float('inf')
                
                # Release old parking reservation
                if car.destination in self.parking_lot.parking_status:
                    if self.parking_lot.parking_status[car.destination] == 'reserved':
                        self.parking_lot.parking_status[car.destination] = 'empty'
                
                path, parking_spot, cost = self.parking_lot.find_shortest_path_to_parking(car.position)
                
                if path and parking_spot:
                    car.path = path
                    car.destination = parking_spot
                    car.current_path_index = 0
                    car.target_segment = path[1] if len(path) > 1 else None
                    car.state = 'entering'
                    car.waiting_timer = 0
                    car.in_deadlock = True
                    
                    # Reserve new parking and path
                    self.parking_lot.reserve_parking(parking_spot)
                    self.parking_lot.update_path_weights(path, 3)
                    
                    # Reserve next segment
                    if car.target_segment:
                        self.parking_lot.reserve_road(car.target_segment, car.id)
            
            # Only reroute one car at a time for simplicity
            self.total_deadlocks_resolved += 1
            break
    
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
            if car.state in ['entering', 'exiting', 'waiting']:
                x = int(car.visual_position[0])
                y = int(car.visual_position[1])
                color = EXIT_CAR_COLOR if car.is_exiting else CAR_COLOR
                pygame.draw.circle(self.screen, color, (x, y), CELL_SIZE // 3)
        
        # Draw statistics
        stats_y = GRID_SIZE * CELL_SIZE + 10
        entering_cars = len([c for c in self.cars if c.state in ['entering', 'waiting'] and not c.is_exiting])
        exiting_cars = len([c for c in self.cars if c.state in ['exiting', 'waiting'] and c.is_exiting])
        parked_cars = len([c for c in self.cars if c.state == 'parked'])
        waiting_cars = len([c for c in self.cars if c.state == 'waiting'])
        
        stats = [
            f"Entering: {entering_cars} | Parked: {parked_cars} | Exiting: {exiting_cars} | Waiting: {waiting_cars}",
            f"Total spawned: {self.car_counter} | Empty spaces: {len([s for s in self.parking_lot.parking_status.values() if s == 'empty'])}",
            f"Deadlocks resolved: {self.total_deadlocks_resolved}"
        ]
        
        for i, stat in enumerate(stats):
            text = self.font.render(stat, True, TEXT_COLOR)
            self.screen.blit(text, (10, stats_y + i * 25))
        
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
            
            # Remove exited cars
            self.cars = [car for car in self.cars if car.state != 'exited']
            
            # Check for deadlocks periodically
            self.deadlock_check_timer += 1
            if self.deadlock_check_timer >= 30:  # Check every 0.5 seconds
                deadlocked_cars = self.detect_deadlock()
                if deadlocked_cars:
                    self.resolve_deadlock(deadlocked_cars)
                self.deadlock_check_timer = 0
            
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
