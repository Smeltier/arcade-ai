import pygame

class Environment:
    def __init__(self, screen, cell_size, maze_file: str) -> None:
        self.domain = screen
        self.cell_size = cell_size
        
        self.maze = self.load_maze(maze_file)
        self.maze_size = len(self.maze[0])

    def load_maze(self, file):
        maze = []
        with open(file, 'r') as f:
            for line in f:
                row = [int(x) for x in line.split()]
                maze.append(row)
        return maze

    def draw(self):
        SIZE = self.maze_size
        CELL_SIZE = self.cell_size
        SCREEN = self.domain

        for row in range(SIZE):
            for col in range(SIZE):
                x, y = col * CELL_SIZE, row * CELL_SIZE
                
                if self.maze[row][col] == -1:
                    pygame.draw.rect(SCREEN, "blue", (x, y, CELL_SIZE, CELL_SIZE))
                if self.maze[row][col] ==  1:
                    pygame.draw.circle(SCREEN, "white", (x + CELL_SIZE / 2, y + CELL_SIZE / 2), 2)