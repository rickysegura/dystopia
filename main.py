import pygame
import sys
import os

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

# Physics settings
GRAVITY = 1
JUMP_POWER = 17
PLAYER_SPEED = 5

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

# Load background
try:
    background_img = pygame.image.load(os.path.join('assets', 'background.png')).convert()
    background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
except Exception:
    background_img = None

# Player class with animation from separate sprite sheets and smaller collision box
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        
        # Animation variables
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = 5  # frames to wait before changing animation frame
        self.facing_right = True
        
        try:
            # Adjust these values to match your sprite sheets!
            self.frame_width = 128  # Width of each sprite frame
            self.frame_height = 128  # Height of each sprite frame
            
            # Load each animation sprite sheet separately
            idle_sheet = load_image('player_idle.png')
            run_sheet = load_image('player_run.png')
            jump_img = load_image('player_jump.png')
            
            # Extract animation frames from each sprite sheet
            self.idle_frames = get_frames_from_spritesheet(idle_sheet, self.frame_width, self.frame_height)
            self.run_frames_right = get_frames_from_spritesheet(run_sheet, self.frame_width, self.frame_height)
            
            # Create left-facing animations by flipping right-facing ones
            self.run_frames_left = []
            for frame in self.run_frames_right:
                self.run_frames_left.append(pygame.transform.flip(frame, True, False))
            
            # Set jump frame
            self.jump_frame = jump_img
            
            self.using_sprites = True
            self.image = self.idle_frames[0]  # Start with first idle frame
            
        except Exception:
            # Fallback if sprite sheets not found
            self.image = pygame.Surface((30, 50))
            self.image.fill(BLUE)
            self.using_sprites = False
        
        # Create main sprite rectangle
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Create smaller collision rectangle
        # Adjust these values to make the hitbox fit your character properly
        self.collision_width = int(self.frame_width * 0.3)  # 30% of sprite width
        self.collision_height = int(self.frame_height * 0.6)  # 60% of sprite height
        
        # Center the collision box horizontally, align with bottom of sprite
        self.collision_rect = pygame.Rect(
            x + (self.frame_width - self.collision_width) // 2,
            y + self.frame_height - self.collision_height,
            self.collision_width,
            self.collision_height
        )
        
        self.velocity_y = 0
        self.velocity_x = 0
        self.on_ground = False
        
    def update(self):
        # Apply gravity
        self.velocity_y += GRAVITY
        
        # Store original positions
        original_x = self.rect.x
        original_y = self.rect.y
        
        # Move horizontally - main rect first
        self.rect.x += self.velocity_x
        
        # Update collision rect horizontal position
        self.collision_rect.x = self.rect.x + (self.frame_width - self.collision_width) // 2
        
        # Check for horizontal collisions using collision_rect
        platform_hit_list = []
        for platform in platforms:
            if self.collision_rect.colliderect(platform.rect):
                platform_hit_list.append(platform)
                
        for platform in platform_hit_list:
            if self.velocity_x > 0:  # Moving right
                self.collision_rect.right = platform.rect.left
                # Update main rect based on collision rect
                self.rect.x = self.collision_rect.x - (self.frame_width - self.collision_width) // 2
            elif self.velocity_x < 0:  # Moving left
                self.collision_rect.left = platform.rect.right
                # Update main rect based on collision rect
                self.rect.x = self.collision_rect.x - (self.frame_width - self.collision_width) // 2
        
        # Move vertically - main rect first
        self.rect.y += self.velocity_y
        
        # Update collision rect vertical position
        self.collision_rect.y = self.rect.y + self.frame_height - self.collision_height
        
        # Check for vertical collisions using collision_rect
        self.on_ground = False
        platform_hit_list = []
        for platform in platforms:
            if self.collision_rect.colliderect(platform.rect):
                platform_hit_list.append(platform)
                
        for platform in platform_hit_list:
            if self.velocity_y > 0:  # Moving down
                self.collision_rect.bottom = platform.rect.top
                self.on_ground = True
            elif self.velocity_y < 0:  # Moving up
                self.collision_rect.top = platform.rect.bottom
                
            self.velocity_y = 0
            # Update main rect based on collision rect
            self.rect.y = self.collision_rect.y - (self.frame_height - self.collision_height)
            
        # Keep player on screen
        if self.collision_rect.left < 0:
            self.collision_rect.left = 0
            self.rect.x = self.collision_rect.x - (self.frame_width - self.collision_width) // 2
        if self.collision_rect.right > SCREEN_WIDTH:
            self.collision_rect.right = SCREEN_WIDTH
            self.rect.x = self.collision_rect.x - (self.frame_width - self.collision_width) // 2
        
        # Check for falling off the bottom
        if self.collision_rect.top > SCREEN_HEIGHT:
            # Reset position
            self.rect.x = 100
            self.rect.y = 100
            self.collision_rect.x = 100 + (self.frame_width - self.collision_width) // 2
            self.collision_rect.y = 100 + self.frame_height - self.collision_height
            self.velocity_y = 0
        
        # Update animation
        if self.using_sprites:
            self.animation_timer += 1
            
            if self.animation_timer >= self.animation_speed:
                self.animation_timer = 0
                self.current_frame = (self.current_frame + 1) % len(self.idle_frames)
                
            # Set correct animation frame based on state
            if not self.on_ground:
                self.image = self.jump_frame
                if not self.facing_right:
                    self.image = pygame.transform.flip(self.jump_frame, True, False)
            elif self.velocity_x > 0:
                self.facing_right = True
                self.image = self.run_frames_right[self.current_frame % len(self.run_frames_right)]
            elif self.velocity_x < 0:
                self.facing_right = False
                self.image = self.run_frames_left[self.current_frame % len(self.run_frames_left)]
            else:
                # Idle animation
                self.image = self.idle_frames[self.current_frame % len(self.idle_frames)]
                if not self.facing_right:
                    self.image = pygame.transform.flip(self.idle_frames[self.current_frame % len(self.idle_frames)], True, False)
        
    def jump(self):
        if self.on_ground:
            self.velocity_y = -JUMP_POWER
            
    def go_left(self):
        self.velocity_x = -PLAYER_SPEED
        self.facing_right = False
        
    def go_right(self):
        self.velocity_x = PLAYER_SPEED
        self.facing_right = True
        
    def stop(self):
        self.velocity_x = 0
        
    # Method to draw collision box for debugging if needed
    def draw_collision_box(self, surface):
        pygame.draw.rect(surface, RED, self.collision_rect, 2)

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
            self.image.fill(GREEN)
            self.using_texture = False
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Create sprite groups
all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()

# Create player
player = Player(100, 100)
all_sprites.add(player)

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
    
    #player.draw_collision_box(screen)

    # Update display
    pygame.display.flip()
    
    # Control game speed
    clock.tick(60)

pygame.quit()
sys.exit()