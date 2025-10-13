import pygame

from world import World
from atributes import Limits, WanderThresholds, BehaviorThresholds
from moving_entity import MovingEntity
from dynamic_states import Wander, Seek
from input_controller import InputController

def main():
    pygame.init()

    WIDTH, HEIGHT = 800, 800
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    CLOCK = pygame.time.Clock()

    world: World = World(SCREEN)

    # Definições da primeira entidade:
    entity_one_wander = WanderThresholds()
    entity_one_behavior = BehaviorThresholds()
    entity_one_limits = Limits(
        max_speed=300,
        max_acceleration=500,
        max_force=1000
    )
                               
    entity_one = MovingEntity(
        WIDTH // 2, 
        HEIGHT // 2, 
        world, 
        limits=entity_one_limits,
        wander_threshold=entity_one_wander,
        behavior_threshold=entity_one_behavior
    )
    
    # Definições da segunda entidade:
    entity_two_behavior = BehaviorThresholds()
    entity_two_limits = Limits(
        max_speed=300,
        max_acceleration=500,
        max_force=1000
    )
                               
    entity_two = MovingEntity(
        WIDTH // 4, 
        HEIGHT // 4, 
        world, 
        limits=entity_two_limits,
        behavior_threshold=entity_two_behavior
    )
    
    world.add_entity(entity_one)
    world.add_entity(entity_two)

    entity_one.state_machine.change_state(Wander(entity_one, entity_two))
    entity_two.state_machine.change_state(Seek(entity_two, entity_one))

    controller = InputController(entity_one, entity_two)

    running = True
    while running:
        pygame.display.flip()
        SCREEN.fill("black")

        delta_time = CLOCK.tick() / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            controller.handle_event(event)

        world.update(delta_time)

    pygame.quit()

if __name__ == "__main__": main()