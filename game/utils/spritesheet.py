"""
Spritesheet utilities for the Chiraq Apocalypse game.

This module provides functions for extracting frames from spritesheets.
"""

import pygame

def get_frames_from_spritesheet(spritesheet, frame_width, frame_height, colorkey=None):
    """
    Extract individual frames from a horizontal spritesheet.
    
    Args:
        spritesheet (pygame.Surface): The spritesheet image
        frame_width (int): Width of each frame in the spritesheet
        frame_height (int): Height of each frame in the spritesheet
        colorkey (tuple, optional): Color to make transparent
        
    Returns:
        list: List of pygame.Surface objects, one for each frame
    """
    sheet_width = spritesheet.get_width()
    
    # Calculate number of frames in the sheet
    num_frames = sheet_width // frame_width
    
    frames = []
    for i in range(num_frames):
        # Calculate position of sprite on sheet
        x = i * frame_width
        y = 0
        
        # Create a new surface for the frame
        frame = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
        
        # Copy the sprite from the sheet
        frame.blit(spritesheet, (0, 0), (x, y, frame_width, frame_height))
        
        if colorkey:
            frame.set_colorkey(colorkey)
        
        frames.append(frame)
    
    return frames