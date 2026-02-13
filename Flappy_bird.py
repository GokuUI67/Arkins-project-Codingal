import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 400, 600
FPS = 60
GRAVITY = 0.5
FLAP_STRENGTH = -10
PIPE_WIDTH = 70
PIPE_HEIGHT = random.randint(150, 400)

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Load images
bird_image = pygame.Surface((40, 30))
bird_image.fill(BLUE)
pipe_image = pygame.Surface((PIPE_WIDTH, HEIGHT))
pipe_image.fill(GREEN)

# Bird class
class Bird:
    def __init__(self):
        self.rect = bird_image.get_rect(center=(100, HEIGHT // 2))
        self.velocity = 0

    def flap(self):
        self.velocity = FLAP_STRENGTH

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += self.velocity

# Pipe class
class Pipe:
    def __init__(self):
        self.height = random.randint(150, 400)
        self.top = pygame.Rect(400, 0, PIPE_WIDTH, self.height)
        self.bottom = pygame.Rect(400, self.height + 150, PIPE_WIDTH, HEIGHT - self.height)

    def update(self):
        self.top.x -= 5
        self.bottom.x -= 5

    def off_screen(self):
        return self.top.x < -PIPE_WIDTH

# Game function
def game():
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    bird = Bird()
    pipes = [Pipe()]
    score = 0
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.flap()

        bird.update()

        if bird.rect.y > HEIGHT or bird.rect.y < 0:
            running = False

        for pipe in pipes:
            pipe.update()
            if pipe.off_screen():
                pipes.remove(pipe)
                pipes.append(Pipe())
                score += 1

            if bird.rect.colliderect(pipe.top) or bird.rect.colliderect(pipe.bottom):
                running = False

        screen.fill(WHITE)
        screen.blit(bird_image, bird.rect)
        for pipe in pipes:
            screen.blit(pipe_image, pipe.top)
            screen.blit(pipe_image, pipe.bottom)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

# Run the game
game()