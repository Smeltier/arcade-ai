import pygame
import random

def main():
    pygame.init()

    game_title: str = "Colisão de Retângulos"
    pygame.display.set_caption(game_title)

    width: float = 800
    height: float = 800
    clock: object = pygame.time.Clock()
    screen: object = pygame.display.set_mode((width, height))

    # Configurando o "jogador".
    player: object = pygame.Rect(0, 0, 50, 50)

    # Configurando os "inimigos".
    enemy_list: list = []
    for _ in range(20):
        new_enemy: object = pygame.Rect(random.randint(0, 800), random.randint(0, 800), 50, 50)
        enemy_list.append(new_enemy)

    # Desativar a setinha do mouse.
    pygame.mouse.set_visible(False)

    running: bool = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill("white")

        # Se tocar no "inimigo" o "jogador" muda de cor.
        color: str = "green"
        if player.collidelist(enemy_list) >= 0:
            print(player.collidelist(enemy_list))
            color = "red"

        # Desenhar o "jogador".
        position: tuple = pygame.mouse.get_pos()
        player.center = position
        pygame.draw.rect(screen, color, player)

        # Desenhar os "inimigos".
        for enemy in enemy_list:
            pygame.draw.rect(screen, "blue", enemy)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()