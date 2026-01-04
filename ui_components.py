"""
UI Components for Robot Pathfinding Simulator
Contains Button class, Robot class, and drawing functions
"""

import pygame
import math
from config import *


class Button:
    """Interactive button with hover and active states"""
    
    def __init__(self, x, y, width, height, text, icon=None, color=BUTTON_BG):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.icon = icon
        self.base_color = color
        self.is_hovered = False
        self.is_active = False
        self.font = pygame.font.SysFont('Segoe UI', FONT_SIZE_MEDIUM, bold=True)
        self.border_radius = scale(8)

    def draw(self, surface):
        """Render the button"""
        if self.is_active:
            color = BUTTON_ACTIVE
        elif self.is_hovered:
            color = BUTTON_HOVER
        else:
            color = self.base_color

        pygame.draw.rect(surface, color, self.rect, border_radius=self.border_radius)
        
        if self.is_active:
            pygame.draw.rect(surface, ACCENT, self.rect, 2, border_radius=self.border_radius)

        # Draw icon + text
        if self.icon:
            icon_surf = self.font.render(self.icon, True, TEXT_PRIMARY)
            text_surf = self.font.render(self.text, True, TEXT_PRIMARY)
            total_width = icon_surf.get_width() + scale(6) + text_surf.get_width()
            icon_x = self.rect.centerx - total_width // 2
            surface.blit(icon_surf, (icon_x, self.rect.centery - icon_surf.get_height() // 2))
            surface.blit(text_surf, (icon_x + icon_surf.get_width() + scale(6), 
                                      self.rect.centery - text_surf.get_height() // 2))
        else:
            text_surf = self.font.render(self.text, True, TEXT_PRIMARY)
            surface.blit(text_surf, (self.rect.centerx - text_surf.get_width() // 2, 
                                      self.rect.centery - text_surf.get_height() // 2))

    def handle_event(self, event, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered:
                return True
        return False


class Robot:
    """Animated robot with smooth movement and trail"""
    
    def __init__(self):
        self.x = 0
        self.y = 0
        self.target_x = 0
        self.target_y = 0
        self.visible = False
        self.animation_offset = 0
        self.trail = []

    def set_position(self, x, y):
        self.x = x
        self.y = y
        self.target_x = x
        self.target_y = y
        self.visible = True
        self.trail = []

    def move_to(self, x, y):
        self.target_x = x
        self.target_y = y

    def update(self):
        speed = 0.18
        self.x += (self.target_x - self.x) * speed
        self.y += (self.target_y - self.y) * speed
        self.animation_offset = math.sin(pygame.time.get_ticks() * 0.012) * 2
        
        if self.visible:
            self.trail.append((self.x, self.y))
            if len(self.trail) > 18:
                self.trail.pop(0)

    def draw(self, surface):
        if not self.visible:
            return

        # Trail
        trail_size = scale(7)
        for i, (tx, ty) in enumerate(self.trail):
            alpha = int((i / len(self.trail)) * 100) if self.trail else 0
            trail_surface = pygame.Surface((trail_size, trail_size), pygame.SRCALPHA)
            pygame.draw.circle(trail_surface, (*YELLOW[:3], alpha), (trail_size//2, trail_size//2), trail_size//2)
            surface.blit(trail_surface, (tx - trail_size//2, ty - trail_size//2))

        x = int(self.x)
        y = int(self.y + self.animation_offset)
        
        # Robot body
        body_w, body_h = scale(24), scale(28)
        body_rect = pygame.Rect(x - body_w//2, y - body_h//2 - scale(2), body_w, body_h)
        pygame.draw.rect(surface, (60, 60, 80), body_rect, border_radius=scale(5))
        pygame.draw.rect(surface, YELLOW, body_rect, 2, border_radius=scale(5))
        
        # Face screen
        screen_w, screen_h = scale(18), scale(12)
        screen_rect = pygame.Rect(x - screen_w//2, y - body_h//2 + scale(3), screen_w, screen_h)
        pygame.draw.rect(surface, (30, 30, 40), screen_rect, border_radius=scale(3))
        
        # Eyes
        eye_offset = math.sin(pygame.time.get_ticks() * 0.005) * 1.5
        pygame.draw.circle(surface, ACCENT, (int(x - scale(4) + eye_offset), y - body_h//2 + scale(9)), scale(3))
        pygame.draw.circle(surface, ACCENT, (int(x + scale(4) + eye_offset), y - body_h//2 + scale(9)), scale(3))
        
        # Antenna
        pygame.draw.line(surface, YELLOW, (x, y - body_h//2 - scale(2)), (x, y - body_h//2 - scale(10)), 2)
        pygame.draw.circle(surface, RED, (x, y - body_h//2 - scale(12)), scale(4))
        
        # Wheels
        pygame.draw.rect(surface, (80, 80, 100), (x - body_w//2 - scale(2), y + body_h//2 - scale(6), scale(5), scale(7)), border_radius=2)
        pygame.draw.rect(surface, (80, 80, 100), (x + body_w//2 - scale(3), y + body_h//2 - scale(6), scale(5), scale(7)), border_radius=2)

    def is_at_target(self):
        return abs(self.x - self.target_x) < 2 and abs(self.y - self.target_y) < 2

    def hide(self):
        self.visible = False
        self.trail = []


def draw_grid(win, grid, floors, floor_width, tile_size, grid_offset_y=0):
    """Render the grid with all floors"""
    offset_x = scale(20)
    
    # Floor backgrounds
    for f in range(floors):
        floor_rect = pygame.Rect(f * floor_width + offset_x, scale(38) + grid_offset_y, 
                                 floor_width - scale(6), GRID_HEIGHT - scale(5))
        pygame.draw.rect(win, GRID_BG, floor_rect, border_radius=scale(6))
        pygame.draw.rect(win, (50, 55, 70), floor_rect, 1, border_radius=scale(6))
    
    # Nodes
    for f in range(floors):
        for row in grid[f]:
            for node in row:
                node.draw(win, offset_x, grid_offset_y)
    
    # Floor labels
    font = pygame.font.SysFont('Segoe UI', FONT_SIZE_LARGE, bold=True)
    for f in range(floors):
        label = f"Floor {f + 1}"
        label_surf = font.render(label, True, TEXT_PRIMARY)
        label_x = f * floor_width + offset_x + (floor_width - label_surf.get_width()) // 2 - scale(3)
        label_bg = pygame.Rect(label_x - scale(6), scale(44) + grid_offset_y, 
                               label_surf.get_width() + scale(12), label_surf.get_height() + scale(6))
        pygame.draw.rect(win, PANEL_BG, label_bg, border_radius=scale(4))
        pygame.draw.rect(win, ACCENT, label_bg, 1, border_radius=scale(4))
        win.blit(label_surf, (label_x, scale(47) + grid_offset_y))


def draw_ui_panel(win, buttons, floors, current_tool, status, width, height):
    """Render the control panel"""
    panel_y = GRID_HEIGHT + scale(25)
    
    # Panel background
    panel_rect = pygame.Rect(scale(10), panel_y, width - scale(20), UI_PANEL_HEIGHT - scale(10))
    pygame.draw.rect(win, PANEL_BG, panel_rect, border_radius=scale(10))
    pygame.draw.rect(win, ACCENT, panel_rect, 1, border_radius=scale(10))
    
    # Buttons
    for button in buttons:
        button.draw(win)
    
    # Right side info
    font = pygame.font.SysFont('Segoe UI', FONT_SIZE_MEDIUM, bold=True)
    small_font = pygame.font.SysFont('Segoe UI', FONT_SIZE_SMALL)
    
    info_x = width - scale(280)
    
    # Floor count
    floor_label = font.render(f"Floors: {floors}", True, TEXT_PRIMARY)
    win.blit(floor_label, (info_x, panel_y + scale(15)))
    
    # Current tool
    tool_label = font.render(f"Tool: {current_tool}", True, YELLOW)
    win.blit(tool_label, (info_x, panel_y + scale(40)))
    
    # Status
    status_bg = pygame.Rect(info_x - scale(10), panel_y + scale(68), scale(260), scale(30))
    pygame.draw.rect(win, (35, 40, 52), status_bg, border_radius=scale(5))
    status_surf = small_font.render(f"Status: {status[:35]}", True, ACCENT)
    win.blit(status_surf, (info_x - scale(5), panel_y + scale(74)))
    
    # Legend (bottom)
    legend_y = panel_y + scale(105)
    legend_font = pygame.font.SysFont('Segoe UI', FONT_SIZE_SMALL)
    
    # Elevator legend
    pygame.draw.rect(win, BLUE, (scale(25), legend_y, scale(12), scale(12)), border_radius=2)
    win.blit(legend_font.render("Elevator", True, TEXT_SECONDARY), (scale(42), legend_y - scale(2)))
    
    # Stairs legend
    pygame.draw.rect(win, STAIRS_COLOR, (scale(110), legend_y, scale(12), scale(12)), border_radius=2)
    win.blit(legend_font.render("Stairs", True, TEXT_SECONDARY), (scale(127), legend_y - scale(2)))
    
    # Path legend
    pygame.draw.rect(win, PURPLE, (scale(185), legend_y, scale(12), scale(12)), border_radius=2)
    win.blit(legend_font.render("Path", True, TEXT_SECONDARY), (scale(202), legend_y - scale(2)))
    
    # Title
    title_font = pygame.font.SysFont('Segoe UI', FONT_SIZE_LARGE, bold=True)
    title = "🤖 Robot Pathfinding Simulator"
    title_surf = title_font.render(title, True, ACCENT)
    win.blit(title_surf, (scale(25), scale(8)))
