import pygame

pygame.init()

WIDTH, HEIGHT = 800, 800
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()
FPS = 60

running = True
while running:
    SCREEN.fill('black')

    delta_time = CLOCK.tick(FPS) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.quit()

pygame.quit()