import pygame
import random
import time

from movingentity import MovingEntity, SEEK, FLEE

def generate_random_position(WIDTH, HEIGHT):
    x = random.randrange(1, WIDTH - 1)
    y = random.randrange(1, HEIGHT - 1)
    return pygame.math.Vector2(x, y)

def main():
    pygame.init()

    WIDTH, HEIGHT = 800, 800
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    CLOCK = pygame.time.Clock()


    entity_one = MovingEntity(WIDTH // 2, HEIGHT // 2, 1, 150, 100, SEEK)
    entity_one.color = "blue"

    entity_two = MovingEntity(WIDTH // 3, HEIGHT // 3, 1, 150, 100, SEEK)
    entity_one.color = "red"

    entities = [entity_one, entity_two]

    random_position = generate_random_position(WIDTH, HEIGHT)
    change_time = time.time() + 1.5

    running = True
    while running:
        delta_time = CLOCK.tick(60) / 1000.0
        
        SCREEN.fill("black")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if(time.time() >= change_time):
            random_position = generate_random_position(WIDTH, HEIGHT)
            change_time = time.time() + 1.5

        entity_one.change_target(random_position)
        entity_two.change_target(entity_one.position)
        
        for entity in entities:
            entity.update(delta_time)
            entity.draw(SCREEN)
            entity.limit_the_entity(WIDTH, HEIGHT)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()