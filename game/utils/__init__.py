"""
Utilities package for Chiraq Apocalypse.

This package contains utility functions and helpers for the game.
"""

# Import and expose key functions from the modules
from .image import load_image
from .spritesheet import get_frames_from_spritesheet

# Define what gets imported with "from utils import *"
__all__ = [
    'load_image',
    'get_frames_from_spritesheet'
]

# Version information
__version__ = '0.1.0'