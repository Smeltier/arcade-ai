import pygame
import random
import time

from moving_entity import MovingEntity
from states import Seek, Flee, KinematicWander

pygame.init()

game_title: str = "Steering Behaviors"
pygame.display.set_caption(game_title)

WIDTH, HEIGTH = 800, 800
SCREEN = pygame.display.set_mode((WIDTH, HEIGTH))
CLOCK = pygame.time.Clock()

# target = MovingEntity(500, 500, max_speed=100, max_force=100, mass=1, max_acceleration=200)
# timmer = time.time() + 3

player_one = MovingEntity(100, 100, max_speed=200, max_force=300, max_acceleration=200, mass=1)
player_one.change_world_resolution(WIDTH, HEIGTH)

player_two = MovingEntity(400, 300, max_speed=200, max_force=300, max_acceleration=200, mass=1)
player_two.change_world_resolution(WIDTH, HEIGTH)

# player_one.target = target
player_two.target = player_one

# target.state_machine.change_state(Flee(target, player_one))
player_one.state_machine.change_state(KinematicWander(player_one))
player_two.state_machine.change_state(Seek(player_two, player_one))

running = True
while running:
    delta_time = CLOCK.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # if time.time() >= timmer:
    #     target.position = pygame.Vector2(random.randint(1, WIDTH - 1), random.randint(1, HEIGTH - 1))
    #     timmer = time.time() + 3

    player_one.delta_time = delta_time
    player_two.delta_time = delta_time

    player_one.update()
    player_two.update()

    SCREEN.fill((30, 30, 30))

    pygame.draw.circle(SCREEN, player_one.color, player_one.position, 8)  
    pygame.draw.circle(SCREEN, player_two.color, player_two.position, 8)  
    # pygame.draw.circle(SCREEN, target.color, target.position, 2)  

    pygame.display.flip()

pygame.quit()