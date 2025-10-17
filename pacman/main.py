import pygame

from environment import Environment

def main():
    pygame.init()

    game_title: str = "PACMAN"
    pygame.display.set_caption(game_title)

    WIDTH, HEIGHT = 840, 840
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    CLOCK = pygame.time.Clock()

    environment = Environment(SCREEN, 40)

    running = True
    while running:
        delta_time = CLOCK.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        environment.draw()

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()