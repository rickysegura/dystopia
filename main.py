"""
Dystopia - Main Game Module

This is the entry point for the Dystopia game. It initializes the game,
sets up the game world, and manages the main game loop.

Usage:
    Run this file directly to start the game:
    $ python main.py
"""


# Imports
import pygame
import sys
import os
from entities.player import Player
from world.game_platform import Platform
from world.start_screen import StartScreen


# Setup game display
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
        icon = pygame.image.load(os.path.join('assets', 'logo.png'))
        pygame.display.set_icon(icon)
        print("Window icon set successfully")
    except Exception as e:
        print(f"Could not set window icon: {e}")
        
    return screen


# Load game background
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


# Create platforms
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


# Handle events
def handle_events(player):
    """
    Process all game events.
    
    Args:
        player (Player): The player object to control
        
    Returns:
        str: 'quit' to exit program, 'menu' to return to menu, or None to continue
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return 'quit'
        
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w, pygame.K_SPACE):
                player.jump()
            elif event.key == pygame.K_ESCAPE:
                return 'menu'
    
    # Handle player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player.go_left()
    elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player.go_right()
    else:
        player.stop()
        
    return None


# Main game loop
def run_game_loop(screen, screen_width, screen_height):
    """
    Run the main gameplay loop.
    
    Args:
        screen (pygame.Surface): The display surface
        screen_width (int): Width of the game window
        screen_height (int): Height of the game window
        
    Returns:
        str: 'quit' to exit program, 'menu' to return to menu
    """

    # Pause menu music
    pygame.mixer.music.pause()

    # Colors
    BLACK = (0, 0, 0)
    
    # Load background
    background_img = load_game_background(screen_width, screen_height)
    
    # Create platforms and sprite groups
    all_sprites, platforms = create_platforms(screen_height, screen_width)
    
    # Create player
    player = Player(100, 100, platforms, screen_width, screen_height)
    all_sprites.add(player)
    
    # Game loop
    clock = pygame.time.Clock()
    running = True
    result = 'menu'  # Default return to menu
    
    while running:
        # Process events
        event_result = handle_events(player)
        
        if event_result == 'quit':
            result = 'quit'
            running = False
        elif event_result == 'menu':
            result = 'menu'
            running = False
        
        # Update game state
        all_sprites.update()
        
        # Draw everything
        if background_img:
            screen.blit(background_img, (0, 0))
        else:
            screen.fill(BLACK)
        
        all_sprites.draw(screen)
        
        # Add ESC key hint
        hint_font = pygame.font.Font(None, 24)
        hint_text = hint_font.render("Press ESC to return to menu", True, (255, 255, 255))
        screen.blit(hint_text, (10, 10))
        
        # Uncomment to debug collision boxes
        #player.draw_collision_box(screen)
    
        # Update display
        pygame.display.flip()
        
        # Control game speed
        clock.tick(60)
        
    return result


def run_game():
    """
    Initialize and run the game with start screen.
    
    This function contains the complete game lifecycle, from initialization
    to the main loop and cleanup.
    """
    # Initialize pygame
    pygame.init()
    
    # Game constants
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    
    # Set up the display
    screen = setup_display(SCREEN_WIDTH, SCREEN_HEIGHT, "Dystopia")
    
    # Create start screen
    start_screen = StartScreen(SCREEN_WIDTH, SCREEN_HEIGHT)
    
    # Game states
    MENU = 0
    PLAYING = 1
    OPTIONS = 2
    
    # Current game state
    game_state = MENU
    previous_state = None
    
    # Main game loop
    clock = pygame.time.Clock()
    running = True
    
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
        
        # Check if state changed
        if previous_state != game_state:
            if game_state == MENU:
                # Potentially restart menu music if it was stopped
                if not pygame.mixer.music.get_busy() and start_screen.music_playing:
                    pygame.mixer.music.unpause()
            
            previous_state = game_state
        
        # Handle different game states
        if game_state == MENU:
            action = start_screen.update(events)
            
            if action == 'play':
                game_state = PLAYING
            elif action == 'options':
                game_state = OPTIONS
            elif action == 'quit':
                running = False
                
            start_screen.draw(screen)
            
        elif game_state == PLAYING:
            # Run the main gameplay loop and get the result
            result = run_game_loop(screen, SCREEN_WIDTH, SCREEN_HEIGHT)
            
            if result == 'quit':
                running = False
            elif result == 'menu':
                game_state = MENU
            
        elif game_state == OPTIONS:
            # In the future, you can add options menu handling here
            # For now, just go back to menu if any key is pressed
            keys = pygame.key.get_pressed()
            if any(keys):
                game_state = MENU
            
            # Draw a simple options screen placeholder
            screen.fill((50, 50, 50))
            font = pygame.font.Font(None, 50)
            text = font.render("Options Menu (Coming Soon)", True, (255, 255, 255))
            text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            screen.blit(text, text_rect)
            
            back_text = font.render("Press any key to return", True, (200, 200, 200))
            back_rect = back_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))
            screen.blit(back_text, back_rect)
        
        # Update display
        pygame.display.flip()
        
        # Control menu animation speed
        clock.tick(60)
    
    # Clean up
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    run_game()