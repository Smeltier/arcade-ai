import pygame
import random 
import time

from moving_entity import MovingEntity
from dynamic_states import Seek, Separation, CollisionAvoidance, Wander

pygame.init()

game_title: str = "Steering Behaviors"
pygame.display.set_caption(game_title)

WIDTH, HEIGHT = 800, 800
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()

# target = MovingEntity(500, 500, max_speed=100, max_force=100, mass=1, max_acceleration=200)
# timmer = time.time() + 3

player_one = MovingEntity(100, 100, max_speed=50, max_force=50, max_acceleration=50, mass=1)
player_one.change_world_resolution(WIDTH, HEIGHT)

player_two = MovingEntity(700, 300, max_speed=200, max_force=300, max_acceleration=200, mass=1)
player_two.change_world_resolution(WIDTH, HEIGHT)

player_three = MovingEntity(400, 300, max_speed=200, max_force=300, max_acceleration=200, mass=1)
player_three.change_world_resolution(WIDTH, HEIGHT)

player_one.target = player_two
player_three.target = player_two

player_two.add_target(player_one)
player_two.add_target(player_three)

# target.state_machine.change_state(Flee(target, player_one))
player_one.state_machine.change_state(Wander(player_one, None))
player_two.state_machine.change_state(Separation(player_two))
player_three.state_machine.change_state(Seek(player_three, player_two))

running = True
while running:
    delta_time = CLOCK.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # if time.time() >= timmer:
    #     target.position = pygame.Vector2(random.randint(1, WIDTH - 1), random.randint(1, HEIGHT - 1))
    #     timmer = time.time() + 3

    # player_one.delta_time = delta_time
    player_two.delta_time = delta_time
    player_three.delta_time = delta_time

    player_one.update()
    player_two.update()
    player_three.update()

    player_three.position = pygame.math.Vector2(pygame.mouse.get_pos())

    SCREEN.fill((30, 30, 30))

    player_one.draw(SCREEN)
    player_two.draw(SCREEN)
    player_three.draw(SCREEN)
    # pygame.draw.circle(SCREEN, target.color, target.position, 2)  

    pygame.display.flip()

pygame.quit()