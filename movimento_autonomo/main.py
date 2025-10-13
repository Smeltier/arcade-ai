import pygame

from world import World
from atributes import Limits, WanderThresholds, BehaviorThresholds
from moving_entity import MovingEntity
from dynamic_states import Wander, Seek, BlendedSteering, Separation
from input_controller import InputController
from outputs import BehaviorAndWeight

def main():
    pygame.init()

    WIDTH, HEIGHT = 800, 800
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    CLOCK = pygame.time.Clock()

    world: World = World(SCREEN)

    # Definições da primeira entidade:
    entity_one = MovingEntity(
        WIDTH // 2, 
        HEIGHT // 2, 
        world, 
        limits = Limits(
            max_speed=300,
            max_acceleration=500,
            max_force=1000,
            max_prediction=10
        ),
        wander_threshold = WanderThresholds(),
        behavior_threshold = BehaviorThresholds()
    )

    # Definições da segunda entidade:
    entity_two = MovingEntity(
        WIDTH // 4, 
        HEIGHT // 4, 
        world, 
        limits = Limits(
            max_speed=300,
            max_acceleration=500,
            max_force=1000
        ),
        behavior_threshold = BehaviorThresholds()
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