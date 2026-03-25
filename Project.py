import pygame
import random
pygame.init()
width, height = 640, 480
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("My first game screen")
white = (255, 255, 255)
rect_color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
rect_width, rect_height = 150, 100
rect_x = (width - rect_width) // 2
rect_y = (height - rect_height) // 2
font = pygame.font.SysFont(None, 48)
text = font.render("Yoooooo Sup", True, (0, 0, 0))
text_rect = text.get_rect(center=(width // 2, height // 4))
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill(white)
    pygame.draw.rect(screen, rect_color, (rect_x, rect_y, rect_width, rect_height))
    screen.blit(text, text_rect)
    pygame.display.flip()

pygame.quit()