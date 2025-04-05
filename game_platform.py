import pygame
from utils import load_image, get_frames_from_spritesheet

# Platform class with texture from sprite sheet
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        
        try:
            # Load platform tiles sprite sheet
            tile_sheet = load_image('platform_tile.png')
            
            # Define tile dimensions
            tile_width = 32  # Width of each tile in sprite sheet
            tile_height = 32  # Height of each tile in sprite sheet
            
            # Extract tiles from the sprite sheet
            platform_tiles = get_frames_from_spritesheet(tile_sheet, tile_width, tile_height)
            
            # Create a surface that tiles the texture
            self.image = pygame.Surface((width, height), pygame.SRCALPHA)
            
            # Assume first tile is left edge, second is middle, third is right edge
            left_tile = platform_tiles[0] if len(platform_tiles) > 0 else None
            middle_tile = platform_tiles[1] if len(platform_tiles) > 1 else left_tile
            right_tile = platform_tiles[2] if len(platform_tiles) > 2 else left_tile
            
            if left_tile and middle_tile and right_tile:
                # Left edge
                self.image.blit(left_tile, (0, 0))
                
                # Middle tiles
                for i in range(tile_width, width - tile_width, tile_width):
                    self.image.blit(middle_tile, (i, 0))
                
                # Right edge
                self.image.blit(right_tile, (width - tile_width, 0))
                
                # Fill in bottom part if height > tile_height
                if height > tile_height and len(platform_tiles) > 3:
                    bottom_tile = platform_tiles[3]
                    for j in range(tile_height, height, tile_height):
                        for i in range(0, width, tile_width):
                            self.image.blit(bottom_tile, (i, j))
                
                self.using_texture = True
            else:
                raise Exception("Not enough tiles in platform sprite sheet")
                
        except Exception:
            # Fallback if texture not found or other error
            self.image = pygame.Surface((width, height))
            self.image.fill((0, 255, 0))  # GREEN
            self.using_texture = False
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y