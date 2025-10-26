import pygame

from environment import Environment
from character import Character

pygame.init()

WIDTH, HEIGHT = 900, 950
FPS = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
clock = pygame.time.Clock()

environment = Environment(screen, 'pacman/maze.txt')

cell_w = environment.cell_width 
cell_h = environment.cell_height
start_row = 2
start_col = 2
x = start_col * cell_w + cell_w / 2
y = start_row * cell_h + cell_h / 2
character = Character(x, y, environment)

environment.add_entity(character)

running = True
while running:
    delta_time = clock.tick(FPS) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    key = pygame.key.get_pressed()
    environment.update(key, delta_time)
    environment.draw()

    pygame.display.flip()  

pygame.quit()