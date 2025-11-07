import pygame
import math

from .formation_manager import FormationManager
from .defensive_circle_pattern import DefensiveCirclePattern
from .static import Static

from movimento_autonomo.world import World
from movimento_autonomo.moving_entity import MovingEntity

from movimento_autonomo.states.arrive import Arrive
from movimento_autonomo.states.seek import Seek

pygame.init()

pygame.display.set_caption("Formation Pattern")

WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

world = World(SCREEN)
pattern = DefensiveCirclePattern(character_radius = 20)
formation_manager = FormationManager(pattern)

entities = []
num_agents = 15
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
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_q:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                
                entity = MovingEntity(
                    mouse_x, 
                    mouse_y, 
                    world, 
                    color="red", 
                    max_speed=80, 
                    max_acceleration=60
                )
                
                entities.append(entity)
                formation_manager.add_character(entity)

            elif event.key == pygame.K_w:
                if entities: 
                    entity_to_remove = entities.pop() 
                    
                    if hasattr(formation_manager, 'remove_character'):
                        formation_manager.remove_character(entity_to_remove)

    mouse_position = pygame.mouse.get_pos()
    anchor_target.position.update(mouse_position)
    
    formation_manager.update_slots()

    keys = pygame.key.get_pressed()


    for entity in entities:
        entity.update(delta_time)

    SCREEN.fill("black")

    pygame.draw.circle(SCREEN, "yellow", (int(anchor_target.position.x), int(anchor_target.position.y)), 6)

    for entity in entities:
        entity.draw(SCREEN)

    pygame.display.flip()

pygame.quit()