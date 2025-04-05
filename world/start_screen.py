"""
Chiraq Apocalypse - Start Screen Module

This module handles the game's start screen, including the title,
buttons, and transitions to the main game.
"""

import pygame
import os
import sys
from utils import load_image


class Button:
    """A class to create interactive buttons for the start screen."""
    
    def __init__(self, x, y, width, height, text, font, text_color, bg_color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.text_color = text_color
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.is_hovered = False
        
        # Render text
        self.text_surf = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)
        
    def draw(self, surface):
        # Draw button with appropriate color
        color = self.hover_color if self.is_hovered else self.bg_color
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, self.text_color, self.rect, 2)  # Border
        
        # Draw text
        surface.blit(self.text_surf, self.text_rect)
        
    def check_hover(self, mouse_pos):
        # Check if mouse is hovering over button
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        return self.is_hovered
        
    def is_clicked(self, event):
        # Check if button is clicked
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.is_hovered
        return False


class StartScreen:
    """Manages the game's start screen interface."""
    
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.DARK_GRAY = (40, 40, 40)
        self.LIGHT_GRAY = (150, 150, 150)
        
        # Load background image
        try:
            self.background = load_image('background.png')
            self.background = pygame.transform.scale(self.background, (screen_width, screen_height))
        except:
            self.background = None
            
        # Load logo image
        try:
            self.logo = load_image('logo.png')
            # Scale logo to appropriate size (adjust as needed)
            logo_width = int(screen_width * 0.25)
            logo_height = int(logo_width * (self.logo.get_height() / self.logo.get_width()))
            self.logo = pygame.transform.scale(self.logo, (logo_width, logo_height))
            self.logo_rect = self.logo.get_rect(centerx=screen_width//2, y=screen_height//7)
        except:
            self.logo = None
            
        # Initialize fonts
        pygame.font.init()
        self.title_font = pygame.font.Font(None, 80)
        self.button_font = pygame.font.Font(None, 50)
        
        # Create title text if no logo
        if not self.logo:
            self.title_text = self.title_font.render("CHIRAQ APOCALYPSE", True, self.WHITE)
            self.title_rect = self.title_text.get_rect(centerx=screen_width//2, y=screen_height//6)
            
        # Create buttons
        button_width = 200
        button_height = 60
        button_spacing = 20
        
        # Position buttons in the center of the screen
        first_button_y = screen_height//2
        
        self.play_button = Button(
            screen_width//2 - button_width//2,
            first_button_y,
            button_width,
            button_height,
            "PLAY",
            self.button_font,
            self.WHITE,
            self.DARK_GRAY,
            self.RED
        )
        
        self.options_button = Button(
            screen_width//2 - button_width//2,
            first_button_y + button_height + button_spacing,
            button_width,
            button_height,
            "OPTIONS",
            self.button_font,
            self.WHITE,
            self.DARK_GRAY,
            self.RED
        )
        
        self.quit_button = Button(
            screen_width//2 - button_width//2,
            first_button_y + 2 * (button_height + button_spacing),
            button_width,
            button_height,
            "QUIT",
            self.button_font,
            self.WHITE,
            self.DARK_GRAY,
            self.RED
        )
        
    def draw(self, screen):
        """Draw the start screen on the provided surface."""
        # Draw background
        if self.background:
            screen.blit(self.background, (0, 0))
        else:
            screen.fill(self.BLACK)
            
        # Draw title/logo
        if self.logo:
            screen.blit(self.logo, self.logo_rect)
        else:
            screen.blit(self.title_text, self.title_rect)
            
        # Draw buttons
        self.play_button.draw(screen)
        self.options_button.draw(screen)
        self.quit_button.draw(screen)
        
        # Draw version info at bottom
        version_text = self.button_font.render("v0.1 Alpha", True, self.WHITE)
        version_rect = version_text.get_rect(bottomright=(self.screen_width - 10, self.screen_height - 10))
        screen.blit(version_text, version_rect)
        
    def update(self, events):
        """
        Update the start screen based on user input.
        
        Returns:
            str: Action to take ('play', 'options', 'quit', or None)
        """
        mouse_pos = pygame.mouse.get_pos()
        
        # Check for button hover
        self.play_button.check_hover(mouse_pos)
        self.options_button.check_hover(mouse_pos)
        self.quit_button.check_hover(mouse_pos)
        
        # Check for button clicks
        for event in events:
            if self.play_button.is_clicked(event):
                return 'play'
            elif self.options_button.is_clicked(event):
                return 'options'
            elif self.quit_button.is_clicked(event):
                return 'quit'
                
        return None