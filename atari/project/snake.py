import pygame
import random
from settings import *

class Snake:
    def __init__(self):
        """Initialize snake with default starting position and direction"""
        # Start at the center of the screen
        start_x = (SCREEN_WIDTH // GRID_SIZE) // 2 * GRID_SIZE
        start_y = (SCREEN_HEIGHT // GRID_SIZE) // 2 * GRID_SIZE
        
        # Snake body - list of positions (x, y)
        self.positions = [(start_x, start_y)]
        
        # Add two more segments to the snake
        self.positions.append((start_x - GRID_SIZE, start_y))
        self.positions.append((start_x - 2 * GRID_SIZE, start_y))
        
        # Starting direction
        self.direction = RIGHT
        
        # Flag to indicate if snake should grow
        self.should_grow = False
        
        # Power-up effects
        self.speed_boost = 0
        self.double_points = 0
        self.rainbow_mode = 0
        self.rainbow_colors = [(random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)) 
                             for _ in range(10)]
        
    def change_direction(self, new_direction):
        """Change snake direction"""
        self.direction = new_direction
        
    def move(self):
        """Move the snake in the current direction"""
        # Get current head position
        head_x, head_y = self.positions[0]
        
        # Calculate new head position
        dir_x, dir_y = self.direction
        new_head = (head_x + dir_x, head_y + dir_y)
        
        # Add new head to the beginning of the list
        self.positions.insert(0, new_head)
        
        # If snake shouldn't grow, remove the last segment
        if not self.should_grow:
            self.positions.pop()
        else:
            self.should_grow = False
            
        # Update power-up timers
        if self.speed_boost > 0:
            self.speed_boost -= 1
        if self.double_points > 0:
            self.double_points -= 1
        if self.rainbow_mode > 0:
            self.rainbow_mode -= 1
            if self.rainbow_mode % 5 == 0:  # Update colors every 5 frames
                self.rainbow_colors = self.rainbow_colors[1:] + [self.rainbow_colors[0]]
            
    def grow(self):
        """Make the snake grow on the next move"""
        self.should_grow = True
        
    def apply_power_up(self, power_up_type):
        """Apply power-up effect"""
        if power_up_type == SPEED_BOOST:
            self.speed_boost = 100  # Last for 100 frames
        elif power_up_type == DOUBLE_POINTS:
            self.double_points = 150  # Last for 150 frames
        elif power_up_type == RAINBOW_MODE:
            self.rainbow_mode = 200  # Last for 200 frames
        
    def draw(self, surface):
        """Draw the snake on the given surface"""
        # Draw head
        head = self.positions[0]
        pygame.draw.rect(surface, GREEN, 
                        (head[0], head[1], GRID_SIZE, GRID_SIZE))
        
        # Draw body
        for i, position in enumerate(self.positions[1:]):
            if self.rainbow_mode > 0:
                # Use cycling rainbow colors
                color = self.rainbow_colors[i % len(self.rainbow_colors)]
            else:
                color = WHITE
                
            pygame.draw.rect(surface, color, 
                           (position[0], position[1], GRID_SIZE, GRID_SIZE))
            
            # Add a small black border to make segments distinct
            pygame.draw.rect(surface, BLACK, 
                           (position[0], position[1], GRID_SIZE, GRID_SIZE), 1)