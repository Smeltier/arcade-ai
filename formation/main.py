import pygame
import math

from formation.formation_entity import FormationEntity
from formation.pattern.defensive_circle_pattern import DefensiveCirclePattern
from formation.static import Static

from movimento_autonomo.world import World
from movimento_autonomo.states.arrive import Arrive


pygame.init()
pygame.display.set_caption("Formation Pattern (Modelo Líder-Seguidor)")

WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

world = World(SCREEN)
pattern = DefensiveCirclePattern(character_radius=15)

entities = []
num_agents = 10
center_x, center_y = WIDTH // 2, HEIGHT // 2

leader = FormationEntity(
    center_x, 
    center_y, 
    world, 
    color="yellow",
    max_speed=100, 
    max_acceleration=80,
)
leader.become_leader(pattern) 
entities.append(leader)
world.add_entity(leader) 

leader_target = Static((center_x, center_y))
leader.state_machine.change_state(Arrive(leader, leader_target))

running = True
while running:
    delta_time = clock.tick(60) / 1000.0
    if delta_time == 0: continue 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_q:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                
                new_follower = FormationEntity(
                    mouse_x, 
                    mouse_y, 
                    world, 
                    color="red", 
                    max_speed=80, 
                    max_acceleration=100,
                    threshold=5
                )
                
                entities.append(new_follower)
                world.add_entity(new_follower)
                leader.add_follower(new_follower)

            elif event.key == pygame.K_w:
                if len(entities) > 1:
                    
                    entity_to_remove = entities.pop()
                    
                    if entity_to_remove is leader:
                        entities.append(leader) 
                    else:
                        world.remove_entity(entity_to_remove)
                        leader.formation_manager.remove_character(entity_to_remove) # type: ignore

    mouse_position = pygame.mouse.get_pos()
    leader_target.position.update(mouse_position)
    
    for entity in entities:
        entity.update(delta_time)

    SCREEN.fill("black")

    pygame.draw.circle(SCREEN, "blue", (int(leader_target.position.x), int(leader_target.position.y)), 6)

    for entity in entities:
        entity.draw(SCREEN)

    pygame.display.flip()

pygame.quit()