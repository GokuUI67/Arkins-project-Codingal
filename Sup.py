import pygame
import sys

pygame.init()

# Screen
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini Geometry Dash")

clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLUE = (50, 150, 255)
RED = (255, 50, 50)
BLACK = (0, 0, 0)

# Player
player = pygame.Rect(100, 300, 40, 40)
velocity_y = 0
gravity = 1
jump_power = -15
on_ground = True

# Ground
ground_y = 340

# Obstacles
obstacles = []
spawn_timer = 0

def spawn_obstacle():
    return pygame.Rect(WIDTH, 310, 30, 30)

def reset_game():
    global player, velocity_y, obstacles
    player.y = 300
    velocity_y = 0
    obstacles.clear()

# Game loop
running = True
while running:
    screen.fill(BLACK)

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and on_ground:
                velocity_y = jump_power

    # Gravity
    velocity_y += gravity
    player.y += velocity_y

    if player.y >= 300:
        player.y = 300
        velocity_y = 0
        on_ground = True
    else:
        on_ground = False

    # Spawn obstacles
    spawn_timer += 1
    if spawn_timer > 90:
        obstacles.append(spawn_obstacle())
        spawn_timer = 0

    # Move obstacles
    for obs in obstacles:
        obs.x -= 6

    # Remove off-screen obstacles
    obstacles = [obs for obs in obstacles if obs.x > -50]

    # Collision
    for obs in obstacles:
        if player.colliderect(obs):
            reset_game()

    # Draw
    pygame.draw.rect(screen, BLUE, player)

    for obs in obstacles:
        pygame.draw.rect(screen, RED, obs)

    pygame.draw.line(screen, WHITE, (0, ground_y), (WIDTH, ground_y), 2)

    pygame.display.update()
    clock.tick(60)