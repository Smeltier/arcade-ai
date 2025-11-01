import pygame

from environment import Environment
from character import Character

pygame.init()
pygame.mixer.init()

FPS = 60
WIDTH, HEIGHT = 900, 950
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
clock = pygame.time.Clock()

environment = Environment(screen, 'pacman/maze.txt')

x = 2 * environment.cell_width + environment.cell_width // 2
y = 2 * environment.cell_height + environment.cell_height // 2
character = Character(x, y, environment)

environment.add_entity(character)

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