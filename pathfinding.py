"""
Pathfinding Algorithm Module
- Elevator: Can go to ANY floor directly (1→2, 1→3, 2→3, etc.)
- Stairs: Can ONLY go to adjacent floor (floor by floor)
"""

import pygame
import heapq
import sys
from config import *


class Node:
    """Represents a single cell in the grid"""
    
    def __init__(self, row, col, floor, tile_size, floor_width):
        self.row = row
        self.col = col
        self.floor = floor
        self.tile_size = tile_size
        self.floor_width = floor_width
        self.x = col * tile_size + (floor * floor_width)
        self.y = row * tile_size
        self.color = WHITE
        self.neighbors = []
        self.is_elevator = False
        self.is_stairs = False
        self.stairs_position = None
        self.g = float('inf')
        self.f = float('inf')
        self.parent = None

    def get_pos(self):
        return self.row, self.col, self.floor

    def is_barrier(self):
        return self.color == BLACK

    def is_special(self):
        return self.is_elevator or self.is_stairs

    def reset(self):
        if self.is_elevator:
            self.color = BLUE
        elif self.is_stairs:
            self.color = STAIRS_COLOR
        else:
            self.color = WHITE
        self.parent = None
        self.g = float('inf')
        self.f = float('inf')

    def make_start(self):
        self.color = GREEN

    def make_closed(self):
        if self.color not in (GREEN, RED, BLUE, STAIRS_COLOR):
            self.color = TURQUOISE

    def make_open(self):
        if self.color not in (GREEN, RED, BLUE, STAIRS_COLOR):
            self.color = ORANGE

    def make_barrier(self):
        if self.color not in (GREEN, RED, BLUE, STAIRS_COLOR):
            self.color = BLACK

    def make_end(self):
        self.color = RED

    def make_path(self):
        if self.color not in (GREEN, RED, BLUE, STAIRS_COLOR):
            self.color = PURPLE

    def make_elevator(self):
        self.is_elevator = True
        self.color = BLUE

    def make_stairs(self, position):
        self.is_stairs = True
        self.stairs_position = position
        self.color = STAIRS_COLOR

    def draw(self, win, offset_x=0, offset_y=0):
        """Render the node with improved visuals"""
        gap = 2
        x_pos = self.x + offset_x
        y_pos = self.y + offset_y + scale(45)
        
        rect = pygame.Rect(x_pos, y_pos, self.tile_size - gap, self.tile_size - gap)
        pygame.draw.rect(win, self.color, rect, border_radius=scale(4))
        
        center_x = x_pos + self.tile_size // 2
        center_y = y_pos + self.tile_size // 2
        size = self.tile_size
        
        # ELEVATOR - Modern lift design
        if self.is_elevator:
            # Outer border
            pygame.draw.rect(win, (30, 80, 160), rect, 3, border_radius=scale(4))
            
            # Elevator doors (two vertical lines)
            door_gap = size // 8
            pygame.draw.line(win, TEXT_PRIMARY, 
                (center_x, y_pos + size // 5), 
                (center_x, y_pos + size - size // 5), 2)
            
            # Up/Down arrows
            arr = size // 7
            # Up arrow
            pygame.draw.polygon(win, (255, 255, 255), [
                (center_x - size//4, center_y - 2),
                (center_x - size//4 - arr, center_y + arr),
                (center_x - size//4 + arr, center_y + arr)
            ])
            # Down arrow
            pygame.draw.polygon(win, (255, 255, 255), [
                (center_x + size//4, center_y + 2),
                (center_x + size//4 - arr, center_y - arr),
                (center_x + size//4 + arr, center_y - arr)
            ])
        
        # STAIRS - Step design
        elif self.is_stairs:
            pygame.draw.rect(win, (180, 80, 160), rect, 2, border_radius=scale(4))
            
            # Draw 4 steps
            step_count = 4
            step_h = (size - scale(8)) // step_count
            step_w = (size - scale(12)) // step_count
            
            for i in range(step_count):
                sx = x_pos + scale(4) + i * step_w
                sy = y_pos + size - scale(6) - (i + 1) * step_h
                sw = size - scale(8) - i * step_w
                sh = step_h - 1
                pygame.draw.rect(win, TEXT_PRIMARY, (sx, sy, sw, sh), border_radius=1)

    def get_center(self, offset_x=0, offset_y=0):
        return (
            self.x + offset_x + self.tile_size // 2,
            self.y + offset_y + scale(45) + self.tile_size // 2
        )

    def update_neighbors(self, grid, floors, rows, cols):
        """Find neighbors - stairs go floor-by-floor, elevator can skip"""
        self.neighbors = []
        
        # Standard 4-directional movement
        if self.row < rows - 1 and not grid[self.floor][self.row + 1][self.col].is_barrier():
            self.neighbors.append((grid[self.floor][self.row + 1][self.col], MOVE_COST))
        if self.row > 0 and not grid[self.floor][self.row - 1][self.col].is_barrier():
            self.neighbors.append((grid[self.floor][self.row - 1][self.col], MOVE_COST))
        if self.col < cols - 1 and not grid[self.floor][self.row][self.col + 1].is_barrier():
            self.neighbors.append((grid[self.floor][self.row][self.col + 1], MOVE_COST))
        if self.col > 0 and not grid[self.floor][self.row][self.col - 1].is_barrier():
            self.neighbors.append((grid[self.floor][self.row][self.col - 1], MOVE_COST))

        # ELEVATOR - Can go to ANY floor (skip floors allowed)
        if self.is_elevator:
            for target_floor in range(floors):
                if target_floor != self.floor:
                    target_node = grid[target_floor][self.row][self.col]
                    if target_node.is_elevator:
                        # Cost based on floors traveled
                        floor_diff = abs(target_floor - self.floor)
                        cost = ELEVATOR_COST * floor_diff
                        self.neighbors.append((target_node, cost))
        
        # STAIRS - Only ADJACENT floors (floor by floor)
        if self.is_stairs:
            # Can only go to floor+1 or floor-1
            # Stairs at right edge connect to left edge of next floor
            # Stairs at left edge connect to right edge of previous floor
            
            if self.col == cols - 1:  # Right edge stairs
                if self.floor < floors - 1:
                    # Connect to left edge stairs of next floor
                    next_node = grid[self.floor + 1][self.row][0]
                    if next_node.is_stairs and next_node.stairs_position == self.stairs_position:
                        self.neighbors.append((next_node, STAIRS_COST))
            
            elif self.col == 0:  # Left edge stairs
                if self.floor > 0:
                    # Connect to right edge stairs of previous floor
                    prev_node = grid[self.floor - 1][self.row][cols - 1]
                    if prev_node.is_stairs and prev_node.stairs_position == self.stairs_position:
                        self.neighbors.append((prev_node, STAIRS_COST))


def heuristic(p1, p2):
    x1, y1, f1 = p1.row, p1.col, p1.floor
    x2, y2, f2 = p2.row, p2.col, p2.floor
    return abs(x1 - x2) + abs(y1 - y2) + (abs(f1 - f2) * 15)


def astar_algorithm(grid, start, end, floors, rows, cols, visualize_callback=None):
    count = 0
    open_set = []
    heapq.heappush(open_set, (0, count, start))
    start.g = 0
    start.f = heuristic(start, end)
    open_set_hash = {start}
    visited_nodes = []

    while open_set:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        current = heapq.heappop(open_set)[2]
        open_set_hash.remove(current)

        if current == end:
            path = []
            while current:
                path.append(current)
                if current != start and current != end:
                    current.make_path()
                current = current.parent
            return path[::-1], visited_nodes

        for neighbor, cost in current.neighbors:
            temp_g = current.g + cost

            if temp_g < neighbor.g:
                neighbor.parent = current
                neighbor.g = temp_g
                neighbor.f = temp_g + heuristic(neighbor, end)
                
                if neighbor not in open_set_hash:
                    count += 1
                    heapq.heappush(open_set, (neighbor.f, count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
                    visited_nodes.append(neighbor)

        if visualize_callback:
            visualize_callback()
            pygame.time.delay(20)

        if current != start:
            current.make_closed()

    return None, visited_nodes


def make_grid(floors, tile_size, floor_width, rows, cols):
    """Create grid with elevator (center) and stairs (at junctions)"""
    grid = []
    elevator_row = rows // 2
    elevator_col = cols // 2
    
    stairs_top_row = 1
    stairs_bottom_row = rows - 2
    
    for f in range(floors):
        floor_grid = []
        for i in range(rows):
            row = []
            for j in range(cols):
                node = Node(i, j, f, tile_size, floor_width)
                row.append(node)
            floor_grid.append(row)
        grid.append(floor_grid)
    
    # Elevator at center of each floor
    for f in range(floors):
        grid[f][elevator_row][elevator_col].make_elevator()
    
    # Stairs at floor junctions
    for f in range(floors):
        # Left edge stairs (for floors > 0)
        if f > 0:
            grid[f][stairs_top_row][0].make_stairs("top")
            grid[f][stairs_bottom_row][0].make_stairs("bottom")
        
        # Right edge stairs (for floors < last)
        if f < floors - 1:
            grid[f][stairs_top_row][cols - 1].make_stairs("top")
            grid[f][stairs_bottom_row][cols - 1].make_stairs("bottom")
    
    return grid
