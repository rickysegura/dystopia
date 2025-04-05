"""
Image handling utilities for the Chiraq Apocalypse game.

This module provides functions for loading and processing game images.
"""

import pygame
import os

def load_image(name, colorkey=None, scale=1):
    """
    Load an image from the assets directory with optional color key and scaling.
    
    Args:
        name (str): The filename of the image in the assets directory
        colorkey (tuple or int, optional): Color to make transparent. If -1, uses top-left pixel color
        scale (float, optional): Scale factor to resize the image
        
    Returns:
        pygame.Surface: The loaded and processed image
        
    Raises:
        SystemExit: If the image couldn't be loaded
    """
    fullname = os.path.join('assets', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print(f"Cannot load image: {name}")
        raise SystemExit(message)
    
    image = image.convert_alpha()
    if scale != 1:
        size = image.get_width() * scale, image.get_height() * scale
        image = pygame.transform.scale(image, size)
    
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image