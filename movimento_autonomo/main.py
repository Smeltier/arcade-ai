import pygame

from world import World
from atributes import Limits
from moving_entity import MovingEntity


def main():
    WIDTH, HEIGHT = 800, 800
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    CLOCK = pygame.time.Clock()

    world: World = World(SCREEN)

    # Definições da primeira entidade:
    entity_one_limits = Limits(max_speed=200,
                               max_acceleration=200,
                               max_force=100)
                               
    entity_one = MovingEntity(WIDTH // 2, 
                              HEIGHT // 2, 
                              world, 
                              limits=entity_one_limits)
    
    # Definições da segunda entidade:
    entity_two_limits = Limits(max_speed=200,
                               max_acceleration=200,
                               max_force=100)
                               
    entity_two = MovingEntity(WIDTH // 4, 
                              HEIGHT // 4, 
                              world, 
                              limits=entity_one_limits)
    
    world.add_entity(entity_one)
    world.add_entity(entity_two)

    pygame.init()

    running = True
    while running:
        pygame.display.flip()
        SCREEN.fill("black")

        delta_time = CLOCK.tick() / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        world.update(delta_time)

    pygame.quit()

if __name__ == "__main__": main()