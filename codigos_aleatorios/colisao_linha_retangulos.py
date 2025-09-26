import pygame
import random

def main():
    pygame.init()

    game_title: str = "Colisão entre mouse e retângulos"
    pygame.display.set_caption(game_title)

    width: float = 800
    height: float = 800
    clock: object = pygame.time.Clock()
    screen: object = pygame.display.set_mode((width, height))

    line_coords: tuple = (width / 2, height / 2)

    # Configurando os "inimigos".
    enemy_list: list = []
    for _ in range(20):
        new_enemy: object = pygame.Rect(random.randint(0, 800), random.randint(0, 800), 50, 50)
        enemy_list.append(new_enemy)

    running: bool = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill("white")

        position = pygame.mouse.get_pos()
        pygame.draw.line(screen, "black", line_coords, position, 5)

        for enemy in enemy_list:
            if enemy.clipline((line_coords, position)):
                pygame.draw.rect(screen, "red", enemy)
            else:
                pygame.draw.rect(screen, "green", enemy)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()