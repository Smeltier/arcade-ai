import pygame
import random
import time

from moving_entity import MovingEntity
from states import SeekState, FleeState

pygame.init()

WIDTH, HEIGTH = 800, 800
SCREEN = pygame.display.set_mode((WIDTH, HEIGTH))
CLOCK = pygame.time.Clock()

player_one = MovingEntity(100, 100, max_speed=100, max_force=100, max_acceleration=100, mass=2, start_state=SeekState())
player_one.world_heigth = HEIGTH
player_one.world_width = WIDTH

player_two = MovingEntity(400, 300, max_speed=100, max_force=100, max_acceleration=100, mass=2, start_state=SeekState())
player_two.world_heigth = HEIGTH
player_two.world_width = WIDTH

target = MovingEntity(500, 500, max_speed=0, max_force=0)
timmer = time.time() + 2.5

player_one.target = target
player_two.target = player_one

running = True
while running:
    delta_time = CLOCK.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if time.time() >= timmer:
        target.position = pygame.Vector2(random.randint(1, WIDTH - 1), random.randint(1, HEIGTH - 1))
        timmer = time.time() + 2.5

    player_one.update()
    player_two.update()

    SCREEN.fill((30, 30, 30))

    pygame.draw.circle(SCREEN, player_one.color, player_one.position, 8)  
    pygame.draw.circle(SCREEN, player_two.color, player_two.position, 8)  
    pygame.draw.circle(SCREEN, target.color, target.position, 2)  

    pygame.display.flip()

pygame.quit()