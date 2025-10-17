import pygame

from maze import MAZE

class Environment:
    def __init__(self, screen, cell_size) -> None:
        self.domain = screen
        self.cell_size = cell_size

        self.maze = MAZE
        self.maze_size = len(MAZE[0])

    def draw(self):
        SIZE = self.maze_size
        CELL_SIZE = self.cell_size
        SCREEN = self.domain

        for i in range(SIZE):
            for j in range(SIZE):
                x, y = i * CELL_SIZE, j * CELL_SIZE
                    
                if self.maze[i][j] == -1:
                    pygame.draw.rect(SCREEN, "blue", (x, y, CELL_SIZE, CELL_SIZE))