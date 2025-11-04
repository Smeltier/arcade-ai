import pygame

from .world import World
from .moving_entity import MovingEntity
from .states.seek import Seek
from .states.wander import Wander
from .states.blended_steering import BlendedSteering
from .input_controller import InputController
from .outputs import BehaviorAndWeight

def main():
    pygame.init()

    WIDTH, HEIGHT = 800, 800
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    CLOCK = pygame.time.Clock()

    world: World = World(SCREEN)

    entity_one = MovingEntity(
        WIDTH // 2, 
        HEIGHT // 2, 
        world, 
        max_speed=300,
        max_acceleration=500,
        max_force=1000,
        max_prediction=10
    )

    entity_two = MovingEntity(
        WIDTH // 4, 
        HEIGHT // 4, 
        world, 
        max_speed=300,
        max_acceleration=500,
        max_force=1000
    )

    behaviors_list = [
        BehaviorAndWeight(Seek(entity_two, entity_one), 1),
        # BehaviorAndWeight(Separation(entity_two), 1)
    ]

    entity_one.state_machine.change_state(Wander(entity_one, entity_two))
    entity_two.state_machine.change_state(BlendedSteering(entity_two, behaviors_list))
    
    world.add_entity(entity_one)
    world.add_entity(entity_two)

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