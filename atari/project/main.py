import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SPEED = 5
BULLET_SPEED = 7
ENEMY_SPEED = 2

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Shooter")
clock = pygame.time.Clock()

# Player
player_width = 50
player_height = 40
player = pygame.Rect(SCREEN_WIDTH//2 - player_width//2, 
                    SCREEN_HEIGHT - player_height - 10,
                    player_width, player_height)

# Game objects
bullets = []
enemies = []
score = 0
high_score = 0
lives = 3
level = 1
font = pygame.font.SysFont(None, 36)
big_font = pygame.font.SysFont(None, 72)

def spawn_enemy():
    enemy_width = 40
    enemy_height = 40
    x = random.randint(0, SCREEN_WIDTH - enemy_width)
    enemy = pygame.Rect(x, -enemy_height, enemy_width, enemy_height)
    enemies.append(enemy)

def draw_player():
    # Draw player ship (triangle)
    points = [
        (player.centerx, player.top),
        (player.left, player.bottom),
        (player.right, player.bottom)
    ]
    pygame.draw.polygon(screen, YELLOW, points)

def draw_enemies():
    for enemy in enemies:
        pygame.draw.rect(screen, RED, enemy)

def draw_bullets():
    for bullet in bullets:
        pygame.draw.rect(screen, WHITE, bullet)

def show_game_stats():
    # Score
    score_text = font.render(f'Score: {score}', True, WHITE)
    screen.blit(score_text, (10, 10))
    
    # High Score
    high_score_text = font.render(f'High Score: {high_score}', True, WHITE)
    screen.blit(high_score_text, (10, 40))
    
    # Lives
    lives_text = font.render(f'Lives: {lives}', True, WHITE)
    screen.blit(lives_text, (SCREEN_WIDTH - 100, 10))
    
    # Level
    level_text = font.render(f'Level: {level}', True, WHITE)
    screen.blit(level_text, (SCREEN_WIDTH - 100, 40))

def show_death_menu():
    # Semi-transparent overlay
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.fill(BLACK)
    overlay.set_alpha(128)
    screen.blit(overlay, (0, 0))
    
    # Game Over text
    game_over_text = big_font.render('GAME OVER', True, RED)
    screen.blit(game_over_text, 
                (SCREEN_WIDTH//2 - game_over_text.get_width()//2, 
                 SCREEN_HEIGHT//2 - 100))
    
    # Final Score
    final_score_text = font.render(f'Final Score: {score}', True, WHITE)
    screen.blit(final_score_text, 
                (SCREEN_WIDTH//2 - final_score_text.get_width()//2, 
                 SCREEN_HEIGHT//2))
    
    # Press Space to restart
    restart_text = font.render('Press SPACE to restart', True, WHITE)
    screen.blit(restart_text, 
                (SCREEN_WIDTH//2 - restart_text.get_width()//2, 
                 SCREEN_HEIGHT//2 + 50))

def reset_game():
    global score, lives, level, enemies, bullets, player
    score = 0
    lives = 3
    level = 1
    player.centerx = SCREEN_WIDTH // 2
    player.bottom = SCREEN_HEIGHT - 10
    bullets.clear()
    enemies.clear()

def main():
    global score, high_score, lives, level
    enemy_spawn_timer = 0
    running = True
    game_active = True

    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if game_active:
                        # Create bullet
                        bullet = pygame.Rect(
                            player.centerx - 2,
                            player.top,
                            4, 10
                        )
                        bullets.append(bullet)
                    else:
                        # Restart game
                        game_active = True
                        reset_game()

        if game_active:
            # Player movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player.left > 0:
                player.x -= PLAYER_SPEED
            if keys[pygame.K_RIGHT] and player.right < SCREEN_WIDTH:
                player.x += PLAYER_SPEED

            # Bullet movement
            for bullet in bullets[:]:
                bullet.y -= BULLET_SPEED
                if bullet.bottom < 0:
                    bullets.remove(bullet)

            # Enemy spawning (faster with higher levels)
            enemy_spawn_timer += 1
            spawn_threshold = max(20, 60 - (level * 5))  # Spawn faster at higher levels
            if enemy_spawn_timer >= spawn_threshold:
                spawn_enemy()
                enemy_spawn_timer = 0

            # Enemy movement
            for enemy in enemies[:]:
                enemy.y += ENEMY_SPEED + (level * 0.5)  # Enemies move faster with higher levels
                if enemy.top > SCREEN_HEIGHT:
                    enemies.remove(enemy)
                    lives -= 1
                    if lives <= 0:
                        if score > high_score:
                            high_score = score
                        game_active = False

            # Collision detection
            for enemy in enemies[:]:
                for bullet in bullets[:]:
                    if enemy.colliderect(bullet):
                        enemies.remove(enemy)
                        bullets.remove(bullet)
                        score += 10
                        # Level up every 100 points
                        if score % 100 == 0:
                            level += 1
                        break

                if enemy.colliderect(player):
                    lives -= 1
                    enemies.remove(enemy)
                    if lives <= 0:
                        if score > high_score:
                            high_score = score
                        game_active = False

            # Drawing game screen
            screen.fill(BLACK)
            draw_player()
            draw_enemies()
            draw_bullets()
            show_game_stats()
        else:
            # Show death menu
            show_death_menu()

        # Update display
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
