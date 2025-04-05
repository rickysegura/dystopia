import pygame
from utils import load_image, get_frames_from_spritesheet

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, platforms, screen_width, screen_height):
        super().__init__()
        
        # Constants for physics
        self.GRAVITY = 1
        self.JUMP_POWER = 17
        self.PLAYER_SPEED = 5
        
        # Store screen boundaries
        self.SCREEN_WIDTH = screen_width
        self.SCREEN_HEIGHT = screen_height
        
        # Store platforms for collision detection
        self.platforms = platforms
        
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
            self.image.fill((0, 0, 255))  # Blue
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
        self.velocity_y += self.GRAVITY
        
        # Store original positions
        original_x = self.rect.x
        original_y = self.rect.y
        
        # Move horizontally - main rect first
        self.rect.x += self.velocity_x
        
        # Update collision rect horizontal position
        self.collision_rect.x = self.rect.x + (self.frame_width - self.collision_width) // 2
        
        # Check for horizontal collisions using collision_rect
        platform_hit_list = []
        for platform in self.platforms:
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
        for platform in self.platforms:
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
        if self.collision_rect.right > self.SCREEN_WIDTH:
            self.collision_rect.right = self.SCREEN_WIDTH
            self.rect.x = self.collision_rect.x - (self.frame_width - self.collision_width) // 2
        
        # Check for falling off the bottom
        if self.collision_rect.top > self.SCREEN_HEIGHT:
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
            self.velocity_y = -self.JUMP_POWER
            
    def go_left(self):
        self.velocity_x = -self.PLAYER_SPEED
        self.facing_right = False
        
    def go_right(self):
        self.velocity_x = self.PLAYER_SPEED
        self.facing_right = True
        
    def stop(self):
        self.velocity_x = 0
        
    # Method to draw collision box for debugging if needed
    def draw_collision_box(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), self.collision_rect, 2)  # Red