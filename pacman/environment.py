import pygame

class Environment:
    def __init__(self, screen, cell_size, maze_file: str) -> None:
        self.domain = screen
        self.cell_size = cell_size
        
        self.maze = self.load_maze(maze_file)
        self.maze_rows = len(self.maze)
        self.maze_cols = len(self.maze[0]) 

    def load_maze(self, file):
        maze = []
        with open(file, 'r') as f:
            for line in f:
                row = [int(x) for x in line.split()]
                maze.append(row)
        return maze

    def draw(self):
        ROWS = self.maze_rows
        COLS = self.maze_cols
        CELL_SIZE = self.cell_size
        SCREEN = self.domain
        RADIUS = CELL_SIZE // 2

        for row in range(ROWS):
            for col in range(COLS):
                
                x_pos = col * CELL_SIZE
                y_pos = row * CELL_SIZE

                center_x = x_pos + RADIUS
                center_y = y_pos + RADIUS

                if self.maze[row][col] == 1:
                    pygame.draw.circle(SCREEN, "white", (center_x, center_y), CELL_SIZE // 10)
                    continue

                pygame.draw.circle(SCREEN, "blue", (center_x, center_y), RADIUS)

                if col + 1 < COLS and self.maze[row][col + 1] == -1:
                    rect = pygame.Rect(center_x, y_pos, CELL_SIZE, CELL_SIZE)
                    pygame.draw.rect(SCREEN, "blue", rect, width=4)
                
                if row + 1 < ROWS and self.maze[row + 1][col] == -1:
                    rect = pygame.Rect(x_pos, center_y, CELL_SIZE, CELL_SIZE)
                    pygame.draw.rect(SCREEN, "blue", rect, width=4)