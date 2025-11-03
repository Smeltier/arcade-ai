import pygame

from environment import Environment
from pacman import PacMan

pygame.init()
pygame.mixer.init()

game_title: str = "Pac-Man"
pygame.display.set_caption(game_title)

FPS = 60
WIDTH, HEIGHT = 900, 950
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

environment = Environment(
    screen, 
    'pacman_game/maze.txt'
)

pacman = PacMan (
    15 * environment.cell_width + environment.cell_width // 2, 
    18 * environment.cell_height + environment.cell_height // 2, 
    environment
)

environment.add_entity(pacman)

running = True

while running:
    delta_time = clock.tick(FPS) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    environment.update(pygame.key.get_pressed(), delta_time)
    environment.draw()

    pygame.display.flip()

pygame.quit()