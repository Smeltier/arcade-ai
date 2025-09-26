import pygame
import pacotes.bfs_menor_caminho as bfspath

def main():

    pygame.init()

    TITLE = "ANIMAÇÃO MENOR CAMINHO"
    WIDTH, HEIGHT = 800, 800
    MATRIZ_SIZE = 50
    MATRIZ_DENSITY = 35
    CELL_SIZE = WIDTH // MATRIZ_SIZE
    FPS = 10

    START = (1, 1)
    END = (MATRIZ_SIZE - 2, MATRIZ_SIZE - 2)

    while True:
        matriz = bfspath.criar_ambiente(MATRIZ_SIZE, MATRIZ_DENSITY)
        bfspath.anotar_matriz(matriz, MATRIZ_SIZE, START, END)
        path = []
        if bfspath.extrair_caminho(matriz, MATRIZ_SIZE, START, END, path):
            break

    path.reverse()

    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE)
    CLOCK = pygame.time.Clock()

    current_step = 0
    RUNNING = True
    while RUNNING:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNNING = False

        SCREEN.fill("white")

        for r in range(MATRIZ_SIZE):
            for c in range(MATRIZ_SIZE):
                x, y = c * CELL_SIZE, r * CELL_SIZE
                if matriz[r][c] == -1:
                    pygame.draw.rect(SCREEN, "gray", (x, y, CELL_SIZE, CELL_SIZE))

        for step in range(current_step):
            r, c = path[step]
            x, y = c * CELL_SIZE, r * CELL_SIZE
            pygame.draw.rect(SCREEN, "blue", (x, y, CELL_SIZE, CELL_SIZE))

        pygame.display.flip()

        if current_step < len(path):
            current_step += 1

        CLOCK.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()