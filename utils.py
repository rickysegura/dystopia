import pygame
import os

# Helper function to load images
def load_image(name, colorkey=None, scale=1):
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

# Function to extract frames from a horizontal sprite sheet
def get_frames_from_spritesheet(spritesheet, frame_width, frame_height, colorkey=None):
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