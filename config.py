"""
Configuration and Color Constants for Robot Pathfinding Simulator
"""

import pygame

# Initialize pygame to get display info
pygame.init()
display_info = pygame.display.Info()

# --- SCREEN DIMENSIONS ---
DISPLAY_WIDTH = display_info.current_w
DISPLAY_HEIGHT = display_info.current_h

# Window size: 85% of screen size
WINDOW_WIDTH = int(DISPLAY_WIDTH * 0.85)
WINDOW_HEIGHT = int(DISPLAY_HEIGHT * 0.85)

# Ensure minimum window size
WINDOW_WIDTH = max(1200, WINDOW_WIDTH)
WINDOW_HEIGHT = max(700, WINDOW_HEIGHT)

# --- LAYOUT CONFIGURATION ---
UI_PANEL_HEIGHT = 150
GRID_HEIGHT = WINDOW_HEIGHT - UI_PANEL_HEIGHT - 60

# Grid configuration
ROWS = 10
COLS = 10
MIN_FLOORS = 2
MAX_FLOORS = 6
DEFAULT_FLOORS = 3

# Calculate dimensions
def calculate_dimensions(floors):
    """Calculate floor width and tile size based on floor count"""
    usable_width = WINDOW_WIDTH - 60
    floor_width = usable_width // floors
    tile_size = min(floor_width // COLS, GRID_HEIGHT // ROWS)
    return floor_width, tile_size

# --- COLOR PALETTE (Dark Theme) ---
BG_DARK = (18, 18, 24)
PANEL_BG = (28, 32, 42)
GRID_BG = (35, 40, 52)
BUTTON_BG = (45, 55, 72)
BUTTON_HOVER = (66, 82, 110)
BUTTON_ACTIVE = (99, 179, 237)
ACCENT = (129, 230, 217)
TEXT_PRIMARY = (255, 255, 255)
TEXT_SECONDARY = (160, 170, 190)

# Node Colors
WHITE = (240, 245, 255)
BLACK = (30, 30, 40)
GREY = (60, 65, 80)
GREEN = (72, 207, 173)      # Start
RED = (252, 92, 101)        # End
BLUE = (69, 170, 242)       # Elevator
PURPLE = (165, 94, 234)     # Path
ORANGE = (253, 150, 68)     # Open/Scanning
TURQUOISE = (38, 222, 129)  # Closed/Visited
YELLOW = (254, 211, 48)     # Robot
STAIRS_COLOR = (255, 159, 243)  # Pink for stairs

# Algorithm costs
MOVE_COST = 1
ELEVATOR_COST = 8       # Elevator is faster
STAIRS_COST = 12        # Stairs take more time

# --- UI SCALING ---
SCALE_FACTOR = min(WINDOW_HEIGHT / 900, WINDOW_WIDTH / 1400)

def scale(value):
    """Scale a value based on window size"""
    return int(value * SCALE_FACTOR)

# Scaled UI dimensions
BUTTON_WIDTH = scale(120)
BUTTON_HEIGHT = scale(42)
BUTTON_SPACING = scale(12)
FONT_SIZE_LARGE = scale(20)
FONT_SIZE_MEDIUM = scale(15)
FONT_SIZE_SMALL = scale(12)
