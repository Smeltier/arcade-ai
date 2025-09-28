import pygame
import random
import time

from movingentity import MovingEntity, SEEK, FLEE, ARRIVE, PURSUIT, EVADE

def generate_random_position(WIDTH, HEIGHT):
    x = random.randrange(1, WIDTH - 1)
    y = random.randrange(1, HEIGHT - 1)
    return pygame.math.Vector2(x, y)

def main():
    pygame.init()

    game_title: str = "Movimento Autônomo"
    pygame.display.set_caption(game_title)

    WIDTH, HEIGHT = 800, 800
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    CLOCK = pygame.time.Clock()

    entity_one = MovingEntity(WIDTH // 2, HEIGHT // 2, 1, 150, 100, SEEK)
    entity_two = MovingEntity(WIDTH // 3, HEIGHT // 3, 1, 150, 100, PURSUIT, entity_one)
    entities = [entity_one, entity_two]

    random_position = generate_random_position(WIDTH, HEIGHT)
    time_stamp = time.time() + 3

    running = True
    while running:
        delta_time = CLOCK.tick(60) / 1000.0
        
        SCREEN.fill("black")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if time.time() >= time_stamp:
            random_position = generate_random_position(WIDTH, HEIGHT)
            time_stamp = time.time() + 2

        entity_one.change_target(random_position)

        entity_two.change_target(entity_one.position)
        entity_two.change_target_speed(entity_one.velocity)
        
        for entity in entities:
            entity.update(delta_time)
            entity.draw(SCREEN)
            entity.limit_the_entity(WIDTH, HEIGHT)

        # Desenha a posição que a entidade um segue.
        pygame.draw.circle(SCREEN, "yellow", random_position, 2)

        pygame.draw.circle(SCREEN, "purple", entity_one.position, 300, 1)
        pygame.draw.circle(SCREEN, "green", entity_one.position, 50, 1)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()