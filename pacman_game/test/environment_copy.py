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

        wall_10 = pygame.image.load('pacman/sprites/sprite_00.png').convert_alpha()
        wall_11 = pygame.image.load('pacman/sprites/sprite_01.png').convert_alpha()
        wall_12 = pygame.image.load('pacman/sprites/sprite_02.png').convert_alpha()
        wall_13 = pygame.image.load('pacman/sprites/sprite_03.png').convert_alpha()
        wall_14 = pygame.image.load('pacman/sprites/sprite_04.png').convert_alpha()
        wall_15 = pygame.image.load('pacman/sprites/sprite_05.png').convert_alpha()
        wall_16 = pygame.image.load('pacman/sprites/sprite_06.png').convert_alpha()
        wall_17 = pygame.image.load('pacman/sprites/sprite_07.png').convert_alpha()
        wall_18 = pygame.image.load('pacman/sprites/sprite_08.png').convert_alpha()
        wall_19 = pygame.image.load('pacman/sprites/sprite_09.png').convert_alpha()
        wall_20 = pygame.image.load('pacman/sprites/sprite_10.png').convert_alpha()
        wall_21 = pygame.image.load('pacman/sprites/sprite_11.png').convert_alpha()
        wall_22 = pygame.image.load('pacman/sprites/sprite_12.png').convert_alpha()
        wall_23 = pygame.image.load('pacman/sprites/sprite_13.png').convert_alpha()
        wall_24 = pygame.image.load('pacman/sprites/sprite_14.png').convert_alpha()
        wall_25 = pygame.image.load('pacman/sprites/sprite_15.png').convert_alpha()
        wall_26 = pygame.image.load('pacman/sprites/sprite_16.png').convert_alpha()
        wall_27 = pygame.image.load('pacman/sprites/sprite_17.png').convert_alpha()

        wall_10 = pygame.transform.scale(wall_10, (CELL_SIZE, CELL_SIZE))
        wall_11 = pygame.transform.scale(wall_11, (CELL_SIZE, CELL_SIZE))
        wall_12 = pygame.transform.scale(wall_12, (CELL_SIZE, CELL_SIZE))
        wall_13 = pygame.transform.scale(wall_13, (CELL_SIZE, CELL_SIZE))
        wall_14 = pygame.transform.scale(wall_14, (CELL_SIZE, CELL_SIZE))
        wall_15 = pygame.transform.scale(wall_15, (CELL_SIZE, CELL_SIZE))
        wall_16 = pygame.transform.scale(wall_16, (CELL_SIZE, CELL_SIZE))
        wall_17 = pygame.transform.scale(wall_17, (CELL_SIZE, CELL_SIZE))
        wall_18 = pygame.transform.scale(wall_18, (CELL_SIZE, CELL_SIZE))
        wall_19 = pygame.transform.scale(wall_19, (CELL_SIZE, CELL_SIZE))
        wall_20 = pygame.transform.scale(wall_20, (CELL_SIZE, CELL_SIZE))
        wall_21 = pygame.transform.scale(wall_21, (CELL_SIZE, CELL_SIZE))
        wall_22 = pygame.transform.scale(wall_22, (CELL_SIZE, CELL_SIZE))
        wall_23 = pygame.transform.scale(wall_23, (CELL_SIZE, CELL_SIZE))
        wall_24 = pygame.transform.scale(wall_24, (CELL_SIZE, CELL_SIZE))
        wall_25 = pygame.transform.scale(wall_25, (CELL_SIZE, CELL_SIZE))
        wall_26 = pygame.transform.scale(wall_26, (CELL_SIZE, CELL_SIZE))
        wall_27 = pygame.transform.scale(wall_27, (CELL_SIZE, CELL_SIZE))

        for row in range(ROWS):
            for col in range(COLS):
                
                x_pos = col * CELL_SIZE
                y_pos = row * CELL_SIZE

                center_x = x_pos + RADIUS
                center_y = y_pos + RADIUS

                if self.maze[row][col] == 1:
                    pygame.draw.circle(SCREEN, "white", (center_x, center_y), CELL_SIZE // 10)
                    continue

                # pygame.draw.rect(SCREEN, "blue", (x_pos, y_pos, CELL_SIZE, CELL_SIZE))

                if self.maze[row][col] == 10:
                    SCREEN.blit(wall_10, (x_pos, y_pos))
                if self.maze[row][col] == 11:
                    SCREEN.blit(wall_11, (x_pos, y_pos))
                if self.maze[row][col] == 12:
                    SCREEN.blit(wall_12, (x_pos, y_pos))
                if self.maze[row][col] == 13:
                    SCREEN.blit(wall_13, (x_pos, y_pos))
                if self.maze[row][col] == 14:
                    SCREEN.blit(wall_14, (x_pos, y_pos))
                if self.maze[row][col] == 15:
                    SCREEN.blit(wall_15, (x_pos, y_pos))
                if self.maze[row][col] == 16:
                    SCREEN.blit(wall_16, (x_pos, y_pos))
                if self.maze[row][col] == 17:
                    SCREEN.blit(wall_17, (x_pos, y_pos))
                if self.maze[row][col] == 18:
                    SCREEN.blit(wall_18, (x_pos, y_pos))
                if self.maze[row][col] == 19:
                    SCREEN.blit(wall_19, (x_pos, y_pos))
                if self.maze[row][col] == 20:
                    SCREEN.blit(wall_20, (x_pos, y_pos))
                if self.maze[row][col] == 21:
                    SCREEN.blit(wall_21, (x_pos, y_pos))
                if self.maze[row][col] == 22:
                    SCREEN.blit(wall_22, (x_pos, y_pos))
                if self.maze[row][col] == 23:
                    SCREEN.blit(wall_23, (x_pos, y_pos))
                if self.maze[row][col] == 24:
                    SCREEN.blit(wall_24, (x_pos, y_pos))
                if self.maze[row][col] == 25:
                    SCREEN.blit(wall_25, (x_pos, y_pos))
                if self.maze[row][col] == 26:
                    SCREEN.blit(wall_26, (x_pos, y_pos))
                if self.maze[row][col] == 27:
                    SCREEN.blit(wall_27, (x_pos, y_pos))