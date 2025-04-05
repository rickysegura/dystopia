"""
Chiraq Apocalypse - Main Game Module

This is the entry point for the Chiraq Apocalypse game. It initializes the game,
sets up the game world, and manages the main game loop.

Usage:
    Run this file directly to start the game:
    $ python main.py
"""

import pygame
import sys
import os
from entities.player import Player
from world.game_platform import Platform


def setup_display(width, height, title):
    """
    Initialize the game display with the specified dimensions and title.
    
    Args:
        width (int): The width of the game window in pixels
        height (int): The height of the game window in pixels
        title (str): The title to display in the window title bar
        
    Returns:
        pygame.Surface: The display surface
    """
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(title)
    
    try:
        # Load the image to use as the window icon
        icon = pygame.image.load(os.path.join('assets', 'game_icon.png'))
        pygame.display.set_icon(icon)
        print("Window icon set successfully")
    except Exception as e:
        print(f"Could not set window icon: {e}")
        
    return screen


def load_game_background(width, height):
    """
    Load and scale the game background image.
    
    Args:
        width (int): The width to scale the background to
        height (int): The height to scale the background to
        
    Returns:
        pygame.Surface or None: The scaled background image, or None if loading failed
    """
    try:
        background_img = pygame.image.load(os.path.join('assets', 'background.png')).convert()
        return pygame.transform.scale(background_img, (width, height))
    except Exception:
        return None


def create_platforms(screen_height, screen_width):
    """
    Create the platforms for the game world.
    
    Args:
        screen_height (int): The height of the game window
        screen_width (int): The width of the game window
        
    Returns:
        tuple: (all_sprites, platforms) pygame.sprite.Group objects
    """
    # Create sprite groups
    all_sprites = pygame.sprite.Group()
    platforms = pygame.sprite.Group()

    # Ground platform
    platform = Platform(0, screen_height - 25, screen_width, 50)
    platforms.add(platform)
    all_sprites.add(platform)

    # Additional platforms
    platform_positions = [
        (50, 465, 200, 20),
        (300, 350, 300, 20)
    ]

    for position in platform_positions:
        platform = Platform(*position)
        platforms.add(platform)
        all_sprites.add(platform)
        
    return all_sprites, platforms


def handle_events(player):
    """
    Process all game events.
    
    Args:
        player (Player): The player object to control
        
    Returns:
        bool: False if the game should quit, True otherwise
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w, pygame.K_SPACE):
                player.jump()
    
    # Handle player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player.go_left()
    elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player.go_right()
    else:
        player.stop()
        
    return True


def run_game():
    """
    Initialize and run the main game loop.
    
    This function contains the complete game lifecycle, from initialization
    to the main loop and cleanup.
    """
    # Initialize pygame
    pygame.init()
    
    # Game constants
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    
    # Colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    RED = (255, 0, 0)
    
    # Set up the display
    screen = setup_display(SCREEN_WIDTH, SCREEN_HEIGHT, "Chiraq Apocalypse")
    
    # Load background
    background_img = load_game_background(SCREEN_WIDTH, SCREEN_HEIGHT)
    
    # Create platforms and sprite groups
    all_sprites, platforms = create_platforms(SCREEN_HEIGHT, SCREEN_WIDTH)
    
    # Create player
    player = Player(100, 100, platforms, SCREEN_WIDTH, SCREEN_HEIGHT)
    all_sprites.add(player)
    
    # Game loop
    clock = pygame.time.Clock()
    running = True
    
    while running:
        # Process events
        running = handle_events(player)
        
        # Update game state
        all_sprites.update()
        
        # Draw everything
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
    
    # Clean up
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    run_game()