import pygame
import random
import math
from settings import *

class Food:
    def __init__(self):
        """Initialize food at a random position"""
        self.spawn([])
        self.is_special = False
        self.power_up_type = None
        self.animation_angle = 0
        
    def spawn(self, occupied_positions):
        """Spawn food at a random position, avoiding the snake's body"""
        while True:
            # Calculate grid dimensions
            grid_width = SCREEN_WIDTH // GRID_SIZE
            grid_height = SCREEN_HEIGHT // GRID_SIZE
            
            # Generate random position aligned to the grid
            x = random.randint(0, grid_width - 1) * GRID_SIZE
            y = random.randint(0, grid_height - 1) * GRID_SIZE
            
            # The food position
            self.position = (x, y)
            
            # Make sure food doesn't spawn on snake
            if self.position not in occupied_positions:
                break
        
        # 20% chance to spawn special food
        self.is_special = random.random() < 0.2
        if self.is_special:
            self.power_up_type = random.choice([SPEED_BOOST, DOUBLE_POINTS, RAINBOW_MODE])
                
    def draw(self, surface):
        """Draw the food on the given surface"""
        x, y = self.position[0] + GRID_SIZE // 2, self.position[1] + GRID_SIZE // 2
        
        if self.is_special:
            # Animate special food
            self.animation_angle = (self.animation_angle + 2) % 360
            size = GRID_SIZE // 2 + int(math.sin(math.radians(self.animation_angle)) * 2)
            
            if self.power_up_type == SPEED_BOOST:
                color = BLUE
            elif self.power_up_type == DOUBLE_POINTS:
                color = GOLD
            else:  # RAINBOW_MODE
                color = PURPLE
                
            # Draw pulsing star shape
            points = []
            for i in range(5):
                angle = math.radians(self.animation_angle + i * 72)
                points.append((
                    x + size * math.cos(angle),
                    y + size * math.sin(angle)
                ))
                inner_angle = math.radians(self.animation_angle + i * 72 + 36)
                points.append((
                    x + (size/2) * math.cos(inner_angle),
                    y + (size/2) * math.sin(inner_angle)
                ))
            pygame.draw.polygon(surface, color, points)
        else:
            # Draw regular food as a red circle
            pygame.draw.circle(surface, RED, (x, y), GRID_SIZE // 2)