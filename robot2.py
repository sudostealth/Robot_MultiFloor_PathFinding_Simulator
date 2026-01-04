"""
Advanced Robot Pathfinding Simulator
=====================================
Main entry point - demonstrates A* pathfinding with elevator and stairs.

Features:
- Multiple floors (2-6)
- Elevator at center (faster)
- Stairs at top and bottom (slower but alternative route)
- Robot finds shortest path using any combination
"""

import pygame
import sys
from config import *
from pathfinding import make_grid, astar_algorithm
from ui_components import Button, Robot, draw_grid, draw_ui_panel


def main():
    pygame.init()
    
    floors = DEFAULT_FLOORS
    floor_width, tile_size = calculate_dimensions(floors)
    
    # Grid dimensions
    rows = min(12, max(8, (GRID_HEIGHT - scale(50)) // tile_size))
    cols = min(12, max(8, (floor_width - scale(25)) // tile_size))
    tile_size = min((GRID_HEIGHT - scale(50)) // rows, (floor_width - scale(25)) // cols)
    
    # Create window
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("🤖 Robot Pathfinding Simulator")
    clock = pygame.time.Clock()
    
    # Create grid with elevator and stairs
    grid = make_grid(floors, tile_size, floor_width, rows, cols)
    
    # State
    start = None
    end = None
    current_tool = "WALL"
    status = "Draw walls, set Start/End, then Run"
    is_running = False
    path = None
    
    robot = Robot()
    path_index = 0
    
    # --- BUTTONS (single row layout) ---
    panel_y = GRID_HEIGHT + scale(40)
    btn_x = scale(25)
    
    buttons = {
        "WALL": Button(btn_x, panel_y, BUTTON_WIDTH, BUTTON_HEIGHT, "Wall", "🧱"),
        "START": Button(btn_x + (BUTTON_WIDTH + BUTTON_SPACING) * 1, panel_y, 
                        BUTTON_WIDTH, BUTTON_HEIGHT, "Start", "🟢"),
        "END": Button(btn_x + (BUTTON_WIDTH + BUTTON_SPACING) * 2, panel_y, 
                      BUTTON_WIDTH, BUTTON_HEIGHT, "End", "🔴"),
        "ERASER": Button(btn_x + (BUTTON_WIDTH + BUTTON_SPACING) * 3, panel_y, 
                         BUTTON_WIDTH, BUTTON_HEIGHT, "Erase", "🧽"),
        "CLEAR": Button(btn_x + (BUTTON_WIDTH + BUTTON_SPACING) * 4, panel_y, 
                        BUTTON_WIDTH, BUTTON_HEIGHT, "Clear", "🗑️"),
        "RUN": Button(btn_x + (BUTTON_WIDTH + BUTTON_SPACING) * 5, panel_y, 
                      BUTTON_WIDTH, BUTTON_HEIGHT, "Run", "▶️", GREEN),
    }
    
    # Floor buttons (right side)
    floor_x = WINDOW_WIDTH - scale(200)
    buttons["FLOOR_DOWN"] = Button(floor_x, panel_y, scale(45), BUTTON_HEIGHT, "−")
    buttons["FLOOR_UP"] = Button(floor_x + scale(55), panel_y, scale(45), BUTTON_HEIGHT, "+")
    
    buttons["WALL"].is_active = True
    
    grid_offset_x = scale(20)
    
    def update_grid():
        nonlocal floor_width, tile_size, rows, cols, grid, start, end, path
        floor_width, tile_size = calculate_dimensions(floors)
        rows = min(12, max(8, (GRID_HEIGHT - scale(50)) // tile_size))
        cols = min(12, max(8, (floor_width - scale(25)) // tile_size))
        tile_size = min((GRID_HEIGHT - scale(50)) // rows, (floor_width - scale(25)) // cols)
        grid = make_grid(floors, tile_size, floor_width, rows, cols)
        start = None
        end = None
        path = None
        robot.hide()

    def get_node_from_pos(pos):
        x, y = pos
        y_adj = y - scale(45)
        if y_adj < 0 or y_adj >= rows * tile_size:
            return None
        x_adj = x - grid_offset_x
        if x_adj < 0:
            return None
        floor = x_adj // floor_width
        if floor >= floors:
            return None
        local_x = x_adj % floor_width
        col = local_x // tile_size
        row = y_adj // tile_size
        if 0 <= row < rows and 0 <= col < cols:
            return grid[floor][row][col]
        return None

    def visualize():
        screen.fill(BG_DARK)
        draw_grid(screen, grid, floors, floor_width, tile_size)
        draw_ui_panel(screen, buttons.values(), floors, current_tool, "Searching...", WINDOW_WIDTH, WINDOW_HEIGHT)
        pygame.display.update()

    def handle_tool(name):
        nonlocal current_tool, status
        for t in ["WALL", "START", "END", "ERASER"]:
            buttons[t].is_active = (t == name)
        current_tool = name
        status = f"{name} tool selected"

    def handle_clear():
        nonlocal grid, start, end, path
        grid = make_grid(floors, tile_size, floor_width, rows, cols)
        start = None
        end = None
        path = None
        robot.hide()
        return "Grid cleared"

    def handle_run():
        nonlocal is_running, path, path_index, status
        if start and end:
            is_running = True
            status = "Running A*..."
            for f in range(floors):
                for r in grid[f]:
                    for n in r:
                        n.update_neighbors(grid, floors, rows, cols)
            result, _ = astar_algorithm(grid, start, end, floors, rows, cols, visualize)
            if result:
                path = result
                path_index = 0
                rx, ry = path[0].get_center(grid_offset_x, 0)
                robot.set_position(rx, ry)
                status = f"Path found! {len(path)} steps"
            else:
                status = "No path found!"
            is_running = False
        else:
            status = "Set START and END first!"

    def handle_floor_change(delta):
        nonlocal floors, status
        new_floors = floors + delta
        if MIN_FLOORS <= new_floors <= MAX_FLOORS:
            floors = new_floors
            update_grid()
            status = f"Floors: {floors}"

    def handle_grid_click(node):
        nonlocal start, end, status
        if not node or is_running:
            return
        if current_tool == "START" and not node.is_special():
            if start:
                start.reset()
            start = node
            start.make_start()
            status = "Start set"
        elif current_tool == "END" and not node.is_special():
            if end:
                end.reset()
            end = node
            end.make_end()
            status = "End set"
        elif current_tool == "WALL":
            if node != start and node != end and not node.is_special():
                node.make_barrier()
        elif current_tool == "ERASER":
            if node == start:
                start = None
            if node == end:
                end = None
            if not node.is_special():
                node.reset()

    def handle_erase(node):
        nonlocal start, end
        if node and not node.is_special():
            if node == start:
                start = None
            if node == end:
                end = None
            node.reset()

    # Main loop
    running = True
    mouse_held = False
    
    while running:
        clock.tick(60)
        mouse_pos = pygame.mouse.get_pos()
        
        for btn in buttons.values():
            btn.is_hovered = btn.rect.collidepoint(mouse_pos)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_held = True
                    for name, btn in buttons.items():
                        if btn.handle_event(event, mouse_pos):
                            if name in ["WALL", "START", "END", "ERASER"]:
                                handle_tool(name)
                            elif name == "CLEAR":
                                status = handle_clear()
                            elif name == "RUN":
                                handle_run()
                            elif name == "FLOOR_DOWN":
                                handle_floor_change(-1)
                            elif name == "FLOOR_UP":
                                handle_floor_change(1)
                    
                    node = get_node_from_pos(mouse_pos)
                    handle_grid_click(node)
                
                elif event.button == 3:
                    node = get_node_from_pos(mouse_pos)
                    handle_erase(node)
            
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_held = False
        
        # Continuous drawing
        if mouse_held and not is_running:
            node = get_node_from_pos(mouse_pos)
            if node:
                if current_tool == "WALL" and not node.is_special():
                    if node != start and node != end:
                        node.make_barrier()
                elif current_tool == "ERASER":
                    handle_erase(node)
        
        # Robot animation
        if path and robot.visible:
            robot.update()
            if robot.is_at_target() and path_index < len(path) - 1:
                path_index += 1
                rx, ry = path[path_index].get_center(grid_offset_x, 0)
                robot.move_to(rx, ry)
        
        # Render
        screen.fill(BG_DARK)
        draw_grid(screen, grid, floors, floor_width, tile_size)
        robot.draw(screen)
        draw_ui_panel(screen, buttons.values(), floors, current_tool, status, WINDOW_WIDTH, WINDOW_HEIGHT)
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()