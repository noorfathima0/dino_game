import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
GROUND_HEIGHT = SCREEN_HEIGHT - 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 60
GRAVITY = 1
JUMP_VELOCITY = -15

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dinosaur Game")

# Load images
dinosaur_img = pygame.image.load('dino.png').convert_alpha()
cactus_img = pygame.image.load('cactus.png').convert_alpha()

# Scale images
dinosaur_img = pygame.transform.scale(dinosaur_img, (35, 50))

# Game variables
ground_rect = pygame.Rect(0, GROUND_HEIGHT, SCREEN_WIDTH, 50)
dinosaur_rect = dinosaur_img.get_rect(midbottom=(100, GROUND_HEIGHT))
obstacles = []
next_spawn_time = pygame.time.get_ticks() + random.randint(1000, 2000)  # Initial random spawn time

# Game loop
clock = pygame.time.Clock()
score = 0
jump_velocity = 0
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    # Handle player input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and dinosaur_rect.bottom == GROUND_HEIGHT:
        jump_velocity = JUMP_VELOCITY
    
    # Apply gravity and jump velocity
    if dinosaur_rect.bottom < GROUND_HEIGHT or jump_velocity < 0:
        dinosaur_rect.y += jump_velocity
        jump_velocity += GRAVITY
    if dinosaur_rect.bottom > GROUND_HEIGHT:
        dinosaur_rect.bottom = GROUND_HEIGHT
        jump_velocity = 0
    
    # Spawn cactus at random intervals and sizes
    current_time = pygame.time.get_ticks()
    if current_time >= next_spawn_time:
        cactus_width = random.randint(30, 50)
        cactus_height = random.randint(40, 60)
        scaled_cactus_img = pygame.transform.scale(cactus_img, (cactus_width, cactus_height))
        obstacle_rect = scaled_cactus_img.get_rect(midbottom=(SCREEN_WIDTH, GROUND_HEIGHT))
        obstacles.append((scaled_cactus_img, obstacle_rect))
        next_spawn_time = current_time + random.randint(1000, 3000)  # Random time for next spawn
    
    # Update obstacles
    for obstacle in obstacles:
        obstacle[1].x -= 5  # Move obstacle towards left
        if obstacle[1].right < 0:
            obstacles.remove(obstacle)
            score += 1
        
        # Collision detection
        if dinosaur_rect.colliderect(obstacle[1]):
            running = False
    
    # Draw everything
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLACK, ground_rect)
    screen.blit(dinosaur_img, dinosaur_rect)
    for obstacle in obstacles:
        screen.blit(obstacle[0], obstacle[1]) 
    
    # Display score
    font = pygame.font.Font(None, 25)
    text = font.render(f'Score: {score}', True, BLACK)
    screen.blit(text, (10, 10))
    pygame.display.flip()
    clock.tick(FPS)

# Game over screen
game_over_font = pygame.font.Font(None, 72)
game_over_text = game_over_font.render('GAME OVER', True, BLACK)
game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
screen.blit(game_over_text, game_over_rect)
pygame.display.flip()

# Wait for a few seconds before quitting
pygame.time.wait(2000)
pygame.quit()
