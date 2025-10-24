import math
import pygame

class Environment ():
    def __init__(self, screen, maze_file: str) -> None:
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.cell_width = self.width // 30
        self.cell_height = self.height // 32
        self.wall_color = 'blue'
        self.matrix = self._load_maze(maze_file)

    def _load_maze(self, maze_file: str):
        maze = []
        with open(maze_file, 'r') as f:
            for line in f:
                row = [int(x) for x in line.split()]
                maze.append(row)
        return maze
    
    def draw_maze(self):
        color = 'blue'
        matrix_width = len(self.matrix[0])
        matrix_height = len(self.matrix)

        for row in range(matrix_height):
            for col in range(matrix_width):
                x, y = col * self.cell_width, row * self.cell_height

                if self.matrix[row][col] == 1:
                    x += self.cell_height // 2
                    y += self.cell_width // 2
                    pygame.draw.circle(self.screen, "white", (x, y), 2)

                if self.matrix[row][col] == 2:
                    x += self.cell_height // 2
                    y += self.cell_width // 2
                    pygame.draw.circle(self.screen, "white", (x, y), 6)

                if self.matrix[row][col] == 3:
                    x += self.cell_height // 2
                    pygame.draw.line(self.screen, color, (x, y), (x, y + self.cell_height))

                if self.matrix[row][col] == 4:
                    y += self.cell_width // 2
                    pygame.draw.line(self.screen, color, (x, y), (x + self.cell_height, y))

                if self.matrix[row][col] == 5:
                    x -= self.cell_height // 2
                    y += self.cell_width // 2
                    pygame.draw.arc(self.screen, color, (x, y, self.cell_height, self.cell_width), 0, math.pi / 2)

                if self.matrix[row][col] == 6:
                    x += self.cell_height // 2
                    y += self.cell_width // 2
                    pygame.draw.arc(self.screen, color, (x, y, self.cell_height, self.cell_width), math.pi / 2, math.pi)

                if self.matrix[row][col] == 7:
                    x += self.cell_height // 2
                    y -= self.cell_width // 2
                    pygame.draw.arc(self.screen, color, (x, y, self.cell_height, self.cell_width), math.pi,  3 * math.pi / 2)

                if self.matrix[row][col] == 8:
                    x -= self.cell_height // 2
                    y -= self.cell_width // 2
                    pygame.draw.arc(self.screen, color, (x, y, self.cell_height, self.cell_width), 3 * math.pi / 2, 2 * math.pi)

                if self.matrix[row][col] == 9:
                    y += self.cell_width // 2
                    pygame.draw.line(self.screen, "white", (x, y), (x + self.cell_height, y))