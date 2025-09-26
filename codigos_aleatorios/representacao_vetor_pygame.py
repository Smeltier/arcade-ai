import pygame

def main():
    pygame.init()

    game_title: str = "Representação de um Vetor2D"
    pygame.display.set_caption(game_title)

    width: float = 800
    height: float = 800
    screen: object = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()

    # Definição das coordenadas dos pontos:
    x_first_point: float = width * 1 / 4
    y_first_point: float = height - height * 1 / 4
    x_second_point: float = width - width * 1 / 4
    y_second_point: float = height * 1 / 4

    # Definições das coordenadas do vetor:
    x_vector: float = x_first_point
    y_vector: float = y_first_point

    running: bool = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill("white")

        # Desenho dos pontos:
        pygame.draw.circle(screen, "black", (x_first_point + 1.5, y_first_point + 1.5), 3)
        pygame.draw.circle(screen, "black", (x_second_point + 1.5, y_second_point + 1.5), 3)

        # Desenho do vetor e da sua "ponta":
        pygame.draw.line(screen, "blue", (x_first_point, y_first_point), (x_vector, y_vector), 4)
        pygame.draw.line(screen, "blue", (x_vector, y_vector), (x_vector, y_vector + 6), 4)
        pygame.draw.line(screen, "blue", (x_vector, y_vector), (x_vector - 6, y_vector), 4)

        # Definir a animação do vetor:
        if x_vector != x_second_point and y_vector != y_second_point:
            x_vector += 10
            y_vector -= 10

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()