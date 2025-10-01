import pygame

def main():
    pygame.init()

    ambient = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1, 1, 1, 0, 0, 0],
        [1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 1, 0, 1],
        [1, 1, 1, 0, 1, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 1, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
        [1, 1, 0, 1, 0, 1, 1, 1, 0, 1],
        [0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ]

    ROWS = len(ambient)
    COLS = len(ambient[0])
    CELL_SIZE: int = 40
    FPS: int = 10

    WIDTH: int = 400
    HEIGHT: int = 400
    SCREEN: object = pygame.display.set_mode((WIDTH, HEIGHT))
    CLOCK:  object = pygame.time.Clock()

    RUNNING: bool = True
    while RUNNING:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNNING = False

        SCREEN.fill("black")

        for r in range(ROWS):
            for c in range(COLS):
                x = c * CELL_SIZE
                y = r * CELL_SIZE

                if ambient[r][c] == 1:
                    pygame.draw.rect(SCREEN, "white", (x, y, CELL_SIZE, CELL_SIZE))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()