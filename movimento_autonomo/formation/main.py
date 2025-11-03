import pygame
import math

from movimento_autonomo.formation.formation_manager import FormationManager
from movimento_autonomo.formation.defensive_circle_pattern import DefensiveCirclePattern
from movimento_autonomo.formation.static import Static
from movimento_autonomo.moving_entity import MovingEntity
from movimento_autonomo.world import World
from movimento_autonomo.states.arrive import Arrive

pygame.init()

WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Formation Pattern Demo")
clock = pygame.time.Clock()

world = World(SCREEN)
pattern = DefensiveCirclePattern(character_radius = 60)
formation_manager = FormationManager(pattern)

entities = []
num_agents = 6
center_x, center_y = WIDTH // 2, HEIGHT // 2

for i in range(num_agents):
    x = center_x + math.cos(i * 2 * math.pi / num_agents) * 100
    y = center_y + math.sin(i * 2 * math.pi / num_agents) * 100

    entity = MovingEntity(x, y, world, color="red", max_speed=80, max_acceleration=60)
    entities.append(entity)
    formation_manager.add_character(entity)

anchor_target = Static((WIDTH // 2, HEIGHT // 2))

formation_manager.world_anchor = anchor_target

running = True
while running:
    delta_time = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    mouse_pos = pygame.mouse.get_pos()
    anchor_target.position.update(mouse_pos)
    
    formation_manager.update_slots()

    for e in entities:
        e.update(delta_time)

    SCREEN.fill("black")
    pygame.draw.circle(SCREEN, "yellow", (int(anchor_target.position.x), int(anchor_target.position.y)), 6)
    for e in entities:
        e.draw(SCREEN)

    pygame.display.flip()

pygame.quit()