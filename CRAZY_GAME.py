"""
Super Python Adventure - A Complete 2D Platformer
Classic Mario-inspired side-scrolling platformer with 20 unique levels
Using Tkinter (built into Python - no installation required!)
"""

import tkinter as tk
from tkinter import font as tkfont
from dataclasses import dataclass
from typing import List, Tuple
from enum import Enum
import random
import math

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
FRAME_DELAY = 1000 // FPS  # milliseconds
GRAVITY = 0.8
MAX_FALL_SPEED = 15

# Colors (Tkinter format)
WHITE = "#FFFFFF"
BLACK = "#000000"
RED = "#FF0000"
GREEN = "#00FF00"
BLUE = "#0064FF"
YELLOW = "#FFFF00"
ORANGE = "#FFA500"
PURPLE = "#800080"
BROWN = "#8B4513"
DARK_GREEN = "#228B22"
GRAY = "#808080"
SKY_BLUE = "#87CEEB"
PINK = "#FF69B4"
CYAN = "#00FFFF"


class EntityType(Enum):
    """Types of entities in the game"""
    PLATFORM = "platform"
    MOVING_PLATFORM = "moving_platform"
    HAZARD = "hazard"
    COIN = "coin"
    ENEMY = "enemy"
    GOAL = "goal"


@dataclass
class Entity:
    """Base entity for game objects"""
    x: float
    y: float
    width: int
    height: int
    entity_type: EntityType
    color: str = WHITE
    
    def get_bounds(self) -> Tuple[float, float, float, float]:
        """Get entity bounds (x1, y1, x2, y2)"""
        return (self.x, self.y, self.x + self.width, self.y + self.height)
    
    def collides_with(self, other_x: float, other_y: float, other_w: int, other_h: int) -> bool:
        """Check collision with another rectangle"""
        return not (self.x + self.width < other_x or
                   other_x + other_w < self.x or
                   self.y + self.height < other_y or
                   other_y + other_h < self.y)


class Player:
    """Player character with physics and controls"""
    
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.width = 32
        self.height = 40
        self.velocity_x = 0
        self.velocity_y = 0
        self.speed = 5
        self.jump_power = 15
        self.on_ground = False
        self.alive = True
        self.facing_right = True
        
    def collides_with(self, entity: Entity) -> bool:
        """Check collision with entity"""
        return entity.collides_with(self.x, self.y, self.width, self.height)
    
    def update(self, keys: set, platforms: List[Entity]):
        """Update player physics and position"""
        if not self.alive:
            return
        
        # Horizontal movement
        self.velocity_x = 0
        if 'Left' in keys or 'a' in keys:
            self.velocity_x = -self.speed
            self.facing_right = False
        if 'Right' in keys or 'd' in keys:
            self.velocity_x = self.speed
            self.facing_right = True
        
        # Apply horizontal movement
        self.x += self.velocity_x
        
        # Check horizontal collisions
        for platform in platforms:
            if platform.entity_type in [EntityType.PLATFORM, EntityType.MOVING_PLATFORM]:
                if self.collides_with(platform):
                    if self.velocity_x > 0:  # Moving right
                        self.x = platform.x - self.width
                    elif self.velocity_x < 0:  # Moving left
                        self.x = platform.x + platform.width
        
        # Apply gravity
        self.velocity_y += GRAVITY
        if self.velocity_y > MAX_FALL_SPEED:
            self.velocity_y = MAX_FALL_SPEED
        
        # Apply vertical movement
        self.y += self.velocity_y
        
        # Check vertical collisions
        self.on_ground = False
        
        for platform in platforms:
            if platform.entity_type in [EntityType.PLATFORM, EntityType.MOVING_PLATFORM]:
                if self.collides_with(platform):
                    if self.velocity_y > 0:  # Falling
                        self.y = platform.y - self.height
                        self.velocity_y = 0
                        self.on_ground = True
                    elif self.velocity_y < 0:  # Jumping
                        self.y = platform.y + platform.height
                        self.velocity_y = 0
        
        # Jumping
        if ('space' in keys or 'Up' in keys or 'w' in keys) and self.on_ground:
            self.velocity_y = -self.jump_power
            self.on_ground = False
        
        # Keep player on screen (left and right bounds)
        if self.x < 0:
            self.x = 0
        if self.x > SCREEN_WIDTH - self.width:
            self.x = SCREEN_WIDTH - self.width
        
        # Death if fall off screen
        if self.y > SCREEN_HEIGHT + 50:
            self.alive = False
    
    def draw(self, canvas: tk.Canvas, camera_x: int):
        """Draw the player"""
        if not self.alive:
            return
        
        draw_x = self.x - camera_x
        
        # Body
        canvas.create_rectangle(
            draw_x, self.y, 
            draw_x + self.width, self.y + self.height,
            fill=BLUE, outline=BLACK, width=2
        )
        
        # Head
        head_center_x = draw_x + self.width // 2
        head_center_y = self.y + 10
        canvas.create_oval(
            head_center_x - 8, head_center_y - 8,
            head_center_x + 8, head_center_y + 8,
            fill="#6496FF", outline=BLACK, width=2
        )
        
        # Eyes
        eye_y = self.y + 8
        if self.facing_right:
            canvas.create_oval(
                draw_x + self.width // 2 + 1, eye_y,
                draw_x + self.width // 2 + 5, eye_y + 4,
                fill=WHITE
            )
            canvas.create_oval(
                draw_x + self.width // 2 + 2, eye_y + 1,
                draw_x + self.width // 2 + 4, eye_y + 3,
                fill=BLACK
            )
        else:
            canvas.create_oval(
                draw_x + self.width // 2 - 5, eye_y,
                draw_x + self.width // 2 - 1, eye_y + 4,
                fill=WHITE
            )
            canvas.create_oval(
                draw_x + self.width // 2 - 4, eye_y + 1,
                draw_x + self.width // 2 - 2, eye_y + 3,
                fill=BLACK
            )


class Enemy:
    """Enemy with patrol or chase behavior"""
    
    def __init__(self, x: int, y: int, patrol_distance: int = 100, enemy_type: str = "patrol"):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 30
        self.velocity_x = 2
        self.start_x = x
        self.patrol_distance = patrol_distance
        self.enemy_type = enemy_type  # "patrol" or "chase"
        self.alive = True
        
    def collides_with(self, other_x: float, other_y: float, other_w: int, other_h: int) -> bool:
        """Check collision"""
        return not (self.x + self.width < other_x or
                   other_x + other_w < self.x or
                   self.y + self.height < other_y or
                   other_y + other_h < self.y)
    
    def update(self, player: Player, platforms: List[Entity]):
        """Update enemy AI and position"""
        if not self.alive:
            return
        
        if self.enemy_type == "patrol":
            self.x += self.velocity_x
            
            if self.x > self.start_x + self.patrol_distance or self.x < self.start_x:
                self.velocity_x *= -1
        
        elif self.enemy_type == "chase" and player.alive:
            if player.x > self.x:
                self.velocity_x = 1.5
            else:
                self.velocity_x = -1.5
            self.x += self.velocity_x
        
        # Basic ground collision
        on_ground = False
        for platform in platforms:
            if platform.entity_type == EntityType.PLATFORM:
                if self.collides_with(platform.x, platform.y, platform.width, platform.height):
                    if self.y + self.height <= platform.y + 10:
                        self.y = platform.y - self.height
                        on_ground = True
        
        if not on_ground:
            self.y += 2
    
    def draw(self, canvas: tk.Canvas, camera_x: int):
        """Draw the enemy"""
        if not self.alive:
            return
        
        draw_x = self.x - camera_x
        
        # Enemy body
        canvas.create_rectangle(
            draw_x, self.y,
            draw_x + self.width, self.y + self.height,
            fill=RED, outline=BLACK, width=2
        )
        
        # Eyes
        canvas.create_oval(draw_x + 6, self.y + 8, draw_x + 12, self.y + 14, fill=WHITE)
        canvas.create_oval(draw_x + 18, self.y + 8, draw_x + 24, self.y + 14, fill=WHITE)
        canvas.create_oval(draw_x + 8, self.y + 10, draw_x + 10, self.y + 12, fill=BLACK)
        canvas.create_oval(draw_x + 20, self.y + 10, draw_x + 22, self.y + 12, fill=BLACK)
        
        # Teeth (spiky look)
        for i in range(0, self.width, 8):
            canvas.create_polygon(
                draw_x + i, self.y + self.height,
                draw_x + i + 4, self.y + self.height - 5,
                draw_x + i + 8, self.y + self.height,
                fill=WHITE
            )


class MovingPlatform:
    """Platform that moves back and forth"""
    
    def __init__(self, entity: Entity, move_distance: int, speed: float, direction: str = "horizontal"):
        self.entity = entity
        self.start_x = entity.x
        self.start_y = entity.y
        self.move_distance = move_distance
        self.speed = speed
        self.direction = direction
        self.velocity = speed
        
    def update(self):
        """Update platform position"""
        if self.direction == "horizontal":
            self.entity.x += self.velocity
            if self.entity.x > self.start_x + self.move_distance or self.entity.x < self.start_x:
                self.velocity *= -1
        else:  # vertical
            self.entity.y += self.velocity
            if self.entity.y > self.start_y + self.move_distance or self.entity.y < self.start_y:
                self.velocity *= -1


class Level:
    """Level manager with all level data"""
    
    def __init__(self, level_number: int):
        self.level_number = level_number
        self.entities: List[Entity] = []
        self.enemies: List[Enemy] = []
        self.moving_platforms: List[MovingPlatform] = []
        self.player_start_x = 50
        self.player_start_y = 400
        self.coins_collected = 0
        self.total_coins = 0
        
        self._generate_level()
    
    def _generate_level(self):
        """Generate level based on level number"""
        self.entities.clear()
        self.enemies.clear()
        self.moving_platforms.clear()
        
        level_generators = {
            1: self._level_1, 2: self._level_2, 3: self._level_3, 4: self._level_4,
            5: self._level_5, 6: self._level_6, 7: self._level_7, 8: self._level_8,
            9: self._level_9, 10: self._level_10, 11: self._level_11, 12: self._level_12,
            13: self._level_13, 14: self._level_14, 15: self._level_15, 16: self._level_16,
            17: self._level_17, 18: self._level_18, 19: self._level_19, 20: self._level_20,
        }
        
        if self.level_number in level_generators:
            level_generators[self.level_number]()
        else:
            self._level_1()
        
        self.total_coins = sum(1 for e in self.entities if e.entity_type == EntityType.COIN)
    
    def _level_1(self):
        """Level 1 - Tutorial"""
        self.entities.append(Entity(0, 550, 800, 50, EntityType.PLATFORM, DARK_GREEN))
        self.entities.append(Entity(0, 450, 200, 20, EntityType.PLATFORM, BROWN))
        self.entities.append(Entity(250, 400, 100, 20, EntityType.PLATFORM, BROWN))
        self.entities.append(Entity(400, 350, 100, 20, EntityType.PLATFORM, BROWN))
        
        for i in range(3):
            self.entities.append(Entity(270 + i * 40, 350, 20, 20, EntityType.COIN, YELLOW))
        
        self.entities.append(Entity(700, 480, 40, 70, EntityType.GOAL, GREEN))
        self.player_start_x, self.player_start_y = 50, 400
    
    def _level_2(self):
        """Level 2 - Gaps"""
        self.entities.append(Entity(0, 550, 200, 50, EntityType.PLATFORM, DARK_GREEN))
        self.entities.append(Entity(300, 550, 200, 50, EntityType.PLATFORM, DARK_GREEN))
        self.entities.append(Entity(600, 550, 200, 50, EntityType.PLATFORM, DARK_GREEN))
        self.entities.append(Entity(150, 400, 120, 20, EntityType.PLATFORM, BROWN))
        self.entities.append(Entity(350, 350, 100, 20, EntityType.PLATFORM, BROWN))
        
        self.entities.append(Entity(230, 480, 20, 20, EntityType.COIN, YELLOW))
        self.entities.append(Entity(530, 480, 20, 20, EntityType.COIN, YELLOW))
        self.entities.append(Entity(370, 300, 20, 20, EntityType.COIN, YELLOW))
        
        self.entities.append(Entity(720, 480, 40, 70, EntityType.GOAL, GREEN))
        self.player_start_x, self.player_start_y = 50, 500
    
    def _level_3(self):
        """Level 3 - First enemy"""
        self.entities.append(Entity(0, 550, 800, 50, EntityType.PLATFORM, DARK_GREEN))
        self.entities.append(Entity(150, 450, 150, 20, EntityType.PLATFORM, BROWN))
        self.entities.append(Entity(400, 380, 200, 20, EntityType.PLATFORM, BROWN))
        
        self.enemies.append(Enemy(420, 350, 150, "patrol"))
        
        for i in range(5):
            self.entities.append(Entity(420 + i * 35, 330, 20, 20, EntityType.COIN, YELLOW))
        
        self.entities.append(Entity(720, 480, 40, 70, EntityType.GOAL, GREEN))
        self.player_start_x, self.player_start_y = 50, 500
    
    def _level_4(self):
        """Level 4 - Moving platform"""
        self.entities.append(Entity(0, 550, 150, 50, EntityType.PLATFORM, DARK_GREEN))
        self.entities.append(Entity(650, 550, 150, 50, EntityType.PLATFORM, DARK_GREEN))
        self.entities.append(Entity(200, 450, 80, 20, EntityType.PLATFORM, BROWN))
        self.entities.append(Entity(520, 450, 80, 20, EntityType.PLATFORM, BROWN))
        
        moving_entity = Entity(320, 400, 100, 20, EntityType.MOVING_PLATFORM, PURPLE)
        self.entities.append(moving_entity)
        self.moving_platforms.append(MovingPlatform(moving_entity, 100, 2, "horizontal"))
        
        self.entities.append(Entity(360, 350, 20, 20, EntityType.COIN, YELLOW))
        self.entities.append(Entity(390, 320, 20, 20, EntityType.COIN, YELLOW))
        
        self.entities.append(Entity(720, 480, 40, 70, EntityType.GOAL, GREEN))
        self.player_start_x, self.player_start_y = 50, 500
    
    def _level_5(self):
        """Level 5 - Hazards"""
        self.entities.append(Entity(0, 550, 250, 50, EntityType.PLATFORM, DARK_GREEN))
        self.entities.append(Entity(450, 550, 350, 50, EntityType.PLATFORM, DARK_GREEN))
        self.entities.append(Entity(250, 570, 200, 30, EntityType.HAZARD, ORANGE))
        self.entities.append(Entity(270, 450, 70, 20, EntityType.PLATFORM, BROWN))
        self.entities.append(Entity(370, 400, 70, 20, EntityType.PLATFORM, BROWN))
        
        self.entities.append(Entity(290, 410, 20, 20, EntityType.COIN, YELLOW))
        self.entities.append(Entity(390, 360, 20, 20, EntityType.COIN, YELLOW))
        
        self.entities.append(Entity(720, 480, 40, 70, EntityType.GOAL, GREEN))
        self.player_start_x, self.player_start_y = 50, 500
    
    def _level_6(self):
        """Level 6 - Vertical climb"""
        self.entities.append(Entity(0, 550, 800, 50, EntityType.PLATFORM, DARK_GREEN))
        self.entities.append(Entity(100, 480, 100, 20, EntityType.PLATFORM, BROWN))
        self.entities.append(Entity(250, 410, 100, 20, EntityType.PLATFORM, BROWN))
        self.entities.append(Entity(400, 340, 100, 20, EntityType.PLATFORM, BROWN))
        self.entities.append(Entity(550, 270, 100, 20, EntityType.PLATFORM, BROWN))
        
        self.enemies.append(Enemy(420, 310, 60, "patrol"))
        
        self.entities.append(Entity(120, 440, 20, 20, EntityType.COIN, YELLOW))
        self.entities.append(Entity(270, 370, 20, 20, EntityType.COIN, YELLOW))
        self.entities.append(Entity(420, 300, 20, 20, EntityType.COIN, YELLOW))
        self.entities.append(Entity(570, 230, 20, 20, EntityType.COIN, YELLOW))
        
        self.entities.append(Entity(720, 480, 40, 70, EntityType.GOAL, GREEN))
        self.player_start_x, self.player_start_y = 50, 500
    
    def _level_7(self):
        """Level 7 - Multiple moving platforms"""
        self.entities.append(Entity(0, 550, 100, 50, EntityType.PLATFORM, DARK_GREEN))
        self.entities.append(Entity(700, 550, 100, 50, EntityType.PLATFORM, DARK_GREEN))
        
        for i in range(3):
            x = 150 + i * 200
            moving_entity = Entity(x, 450 - i * 50, 90, 15, EntityType.MOVING_PLATFORM, PURPLE)
            self.entities.append(moving_entity)
            self.moving_platforms.append(MovingPlatform(moving_entity, 80, 1.5 + i * 0.5, "horizontal"))
        
        for i in range(4):
            self.entities.append(Entity(200 + i * 150, 350, 20, 20, EntityType.COIN, YELLOW))
        
        self.entities.append(Entity(730, 480, 40, 70, EntityType.GOAL, GREEN))
        self.player_start_x, self.player_start_y = 30, 500
    
    def _level_8(self):
        """Level 8 - Enemy gauntlet"""
        self.entities.append(Entity(0, 550, 800, 50, EntityType.PLATFORM, DARK_GREEN))
        self.entities.append(Entity(150, 450, 150, 20, EntityType.PLATFORM, BROWN))
        self.enemies.append(Enemy(170, 420, 100, "patrol"))
        
        self.entities.append(Entity(400, 400, 150, 20, EntityType.PLATFORM, BROWN))
        self.enemies.append(Enemy(420, 370, 100, "patrol"))
        
        for i in range(6):
            self.entities.append(Entity(150 + i * 100, 350, 20, 20, EntityType.COIN, YELLOW))
        
        self.entities.append(Entity(720, 480, 40, 70, EntityType.GOAL, GREEN))
        self.player_start_x, self.player_start_y = 50, 500
    
    def _level_9(self):
        """Level 9 - Vertical moving platform"""
        self.entities.append(Entity(0, 550, 200, 50, EntityType.PLATFORM, DARK_GREEN))
        self.entities.append(Entity(500, 300, 200, 20, EntityType.PLATFORM, BROWN))
        self.entities.append(Entity(600, 550, 200, 50, EntityType.PLATFORM, DARK_GREEN))
        
        moving_entity = Entity(300, 450, 100, 20, EntityType.MOVING_PLATFORM, PURPLE)
        self.entities.append(moving_entity)
        self.moving_platforms.append(MovingPlatform(moving_entity, 200, 2, "vertical"))
        
        self.entities.append(Entity(330, 400, 20, 20, EntityType.COIN, YELLOW))
        self.entities.append(Entity(330, 350, 20, 20, EntityType.COIN, YELLOW))
        self.entities.append(Entity(530, 260, 20, 20, EntityType.COIN, YELLOW))
        
        self.entities.append(Entity(720, 480, 40, 70, EntityType.GOAL, GREEN))
        self.player_start_x, self.player_start_y = 50, 500
    
    def _level_10(self):
        """Level 10 - The maze"""
        self.entities.append(Entity(0, 550, 800, 50, EntityType.PLATFORM, DARK_GREEN))
        self.entities.append(Entity(100, 480, 150, 20, EntityType.PLATFORM, BROWN))
        self.entities.append(Entity(300, 420, 150, 20, EntityType.PLATFORM, BROWN))
        self.entities.append(Entity(150, 360, 100, 20, EntityType.PLATFORM, BROWN))
        self.entities.append(Entity(350, 300, 120, 20, EntityType.PLATFORM, BROWN))
        self.entities.append(Entity(550, 380, 100, 20, EntityType.PLATFORM, BROWN))
        
        self.enemies.append(Enemy(320, 390, 100, "patrol"))
        self.enemies.append(Enemy(560, 350, 70, "patrol"))
        
        self.entities.append(Entity(250, 520, 80, 30, EntityType.HAZARD, ORANGE))
        
        for i in range(5):
            self.entities.append(Entity(120 + i * 110, 250, 20, 20, EntityType.COIN, YELLOW))
        
        self.entities.append(Entity(720, 480, 40, 70, EntityType.GOAL, GREEN))
        self.player_start_x, self.player_start_y = 50, 500
    
    def _level_11(self):
        """Level 11 - Speed run"""
        self.entities.append(Entity(0, 550, 120, 50, EntityType.PLATFORM, DARK_GREEN))
        self.entities.append(Entity(180, 520, 100, 30, EntityType.PLATFORM, BROWN))
        self.entities.append(Entity(340, 490, 100, 30, EntityType.PLATFORM, BROWN))
        self.entities.append(Entity(500, 460, 100, 30, EntityType.PLATFORM, BROWN))
        self.entities.append(Entity(660, 550, 140, 50, EntityType.PLATFORM, DARK_GREEN))
        
        for i in range(7):
            self.entities.append(Entity(140 + i * 90, 400, 20, 20, EntityType.COIN, YELLOW))
        
        self.entities.append(Entity(730, 480, 40, 70, EntityType.GOAL, GREEN))
        self.player_start_x, self.player_start_y = 50, 500
    
    def _level_12(self):
        """Level 12 - Chase enemy"""
        self.entities.append(Entity(0, 550, 800, 50, EntityType.PLATFORM, DARK_GREEN))
        self.entities.append(Entity(200, 450, 400, 20, EntityType.PLATFORM, BROWN))
        
        self.enemies.append(Enemy(300, 420, 0, "chase"))
        
        for i in range(6):
            self.entities.append(Entity(220 + i * 60, 410, 20, 20, EntityType.COIN, YELLOW))
        
        self.entities.append(Entity(720, 480, 40, 70, EntityType.GOAL, GREEN))
        self.player_start_x, self.player_start_y = 50, 500
    
    def _level_13(self):
        """Level 13 - Precision platforming"""
        self.entities.append(Entity(0, 550, 100, 50, EntityType.PLATFORM, DARK_GREEN))
        
        for i in range(8):
            x = 120 + i * 90
            y = 470 - (i % 2) * 40
            self.entities.append(Entity(x, y, 60, 15, EntityType.PLATFORM, BROWN))
        
        self.entities.append(Entity(700, 550, 100, 50, EntityType.PLATFORM, DARK_GREEN))
        
        for i in range(4):
            self.entities.append(Entity(140 + i * 180, 400, 20, 20, EntityType.COIN, YELLOW))
        
        self.entities.append(Entity(730, 480, 40, 70, EntityType.GOAL, GREEN))
        self.player_start_x, self.player_start_y = 30, 500
    
    def _level_14(self):
        """Level 14 - Hazard parkour"""
        self.entities.append(Entity(0, 550, 800, 50, EntityType.PLATFORM, DARK_GREEN))
        
        for i in range(4):
            self.entities.append(Entity(150 + i * 150, 530, 80, 20, EntityType.HAZARD, ORANGE))
        
        for i in range(4):
            self.entities.append(Entity(170 + i * 150, 450, 60, 15, EntityType.PLATFORM, BROWN))
        
        for i in range(5):
            self.entities.append(Entity(180 + i * 120, 410, 20, 20, EntityType.COIN, YELLOW))
        
        self.entities.append(Entity(720, 480, 40, 70, EntityType.GOAL, GREEN))
        self.player*_