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
        self.maze_surface = pygame.Surface((self.width, self.height))
        self.entities = []
        self.maze = self._load_maze(maze_file)
        self.rows = len(self.maze)
        self.cols = len(self.maze[0])
        self.matrix = self._load_walls()

        self.maze_surface.fill('black')
        self._draw_maze(self.maze_surface)

    def _load_maze(self, maze_file: str):
        maze = []
        with open(maze_file, 'r') as f:
            for line in f:
                row = [int(x) for x in line.split()]
                maze.append(row)
        return maze
    
    def _load_walls(self):
        matrix = []
        for row in self.maze:
            new_row = [-1 if x > 2 else x for x in row]
            matrix.append(new_row)
        return matrix
    
    def _draw_maze(self, surface): # O(H * W)
        color = 'blue'

        for row in range(self.rows):
            for col in range(self.cols):
                x, y = col * self.cell_width, row * self.cell_height

                if self.maze[row][col] == 3:
                    x += self.cell_height // 2
                    pygame.draw.line(surface, color, (x, y), (x, y + self.cell_height))

                elif self.maze[row][col] == 4:
                    y += self.cell_width // 2
                    pygame.draw.line(surface, color, (x, y), (x + self.cell_height, y))

                elif self.maze[row][col] == 5:
                    x -= self.cell_height // 2
                    y += self.cell_width // 2
                    pygame.draw.arc(surface, color, (x, y, self.cell_height, self.cell_width), 0, math.pi / 2)

                elif self.maze[row][col] == 6:
                    x += self.cell_height // 2
                    y += self.cell_width // 2
                    pygame.draw.arc(surface, color, (x, y, self.cell_height, self.cell_width), math.pi / 2, math.pi)

                elif self.maze[row][col] == 7:
                    x += self.cell_height // 2
                    y -= self.cell_width // 2
                    pygame.draw.arc(surface, color, (x, y, self.cell_height, self.cell_width), math.pi, 3 * math.pi / 2)

                elif self.maze[row][col] == 8:
                    x -= self.cell_height // 2
                    y -= self.cell_width // 2
                    pygame.draw.arc(surface, color, (x, y, self.cell_height, self.cell_width), 3 * math.pi / 2, 2 * math.pi)

                elif self.maze[row][col] == 9:
                    y += self.cell_width // 2
                    pygame.draw.line(surface, "pink", (x, y), (x + self.cell_height, y))

    def _draw_food(self):
        color = 'white'

        for row in range(self.rows):
            for col in range(self.cols):
                x, y = col * self.cell_width, row * self.cell_height

                if self.maze[row][col] == 1:
                    x += self.cell_height // 2
                    y += self.cell_width // 2
                    pygame.draw.circle(self.screen, color, (x, y), 2)

                if self.maze[row][col] == 2:
                    x += self.cell_height // 2
                    y += self.cell_width // 2
                    pygame.draw.circle(self.screen, color, (x, y), 6)

    def _draw_entities(self):
        for entity in self.entities:
            entity.draw(self.screen)

    def draw(self):
        self.screen.blit(self.maze_surface, (0, 0))
        self._draw_food()
        self._draw_entities()

    def add_entity(self, entity):
        if entity is None:
            raise ValueError('Entidade inválida.')
        
        self.entities.append(entity)

    def remove_entity(self, entity):
        self.entities = [e for e in self.entities if e is not entity]

    def update(self, keys, delta_time):
        for entity in self.entities:
            entity.update(keys, delta_time)