import pygame
import sys
import os
from entities.player import Player
from world.game_platform import Platform

# Initialize pygame
pygame.init()

# Set up the display
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Chiraq Apocalypse")

# Add this code after initializing pygame and before creating the display
try:
    # Load the image you want to use as the icon
    icon = pygame.image.load(os.path.join('assets', 'game_icon.png'))
    
    # Set the window icon
    pygame.display.set_icon(icon)
    
    # Optional: Print confirmation
    print("Window icon set successfully")
except Exception as e:
    # If there's an error, print it but continue with the game
    print(f"Could not set window icon: {e}")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Load background
try:
    background_img = pygame.image.load(os.path.join('assets', 'background.png')).convert()
    background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
except Exception:
    background_img = None

# Platform class is now imported from platform.py

# Create sprite groups
all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()

# Create platforms
# Ground
platform = Platform(0, SCREEN_HEIGHT - 25, SCREEN_WIDTH, 50)
platforms.add(platform)
all_sprites.add(platform)

# Platforms
platform_positions = [
    (50, 465, 200, 20),
    (300, 350, 300, 20)
]

for position in platform_positions:
    platform = Platform(*position)
    platforms.add(platform)
    all_sprites.add(platform)

# Create player - now with platforms passed in
player = Player(100, 100, platforms, SCREEN_WIDTH, SCREEN_HEIGHT)
all_sprites.add(player)

# Game loop
clock = pygame.time.Clock()
running = True

while running:
    # Process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w or event.key == pygame.K_SPACE:
                player.jump()
    
    # Handle player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player.go_left()
    elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player.go_right()
    else:
        player.stop()
    
    # Update
    all_sprites.update()
    
    # Draw
    if background_img:
        screen.blit(background_img, (0, 0))
    else:
        screen.fill(BLACK)
    
    all_sprites.draw(screen)
    
    # Uncomment to debug collision boxes
    #player.draw_collision_box(screen)

    # Update display
    pygame.display.flip()
    
    # Control game speed
    clock.tick(60)

pygame.quit()
sys.exit()