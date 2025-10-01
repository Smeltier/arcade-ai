import pygame

import bfs_menor_caminho as sp

class DiscreteMovingEntity:
    
    def __init__(self, x, y, mass, max_force, max_speed, CELL_SIZE):
        self.position     = pygame.math.Vector2((x, y))
        self.velocity     = pygame.math.Vector2((0, 0))
        self.acceleration = pygame.math.Vector2((0, 0))

        self.max_speed = max_speed
        self.max_force = max_force
        self.mass = mass
        self.CELL_SIZE = CELL_SIZE

        self.path = []
        self.path_size = 0
        self.current_index = 0

    def pixel_to_grid(self, position_pixel):
        """Converte uma coordenada de pixel para uma coordenada de grid."""
        grid_x = int(position_pixel.x // self.CELL_SIZE)
        grid_y = int(position_pixel.y // self.CELL_SIZE)
        return (grid_x, grid_y)
    
    def grid_to_pixel(self, position_grid):
        """Converte uma coordenada de grid para o centro da célula em pixels."""
        pixel_x = (position_grid[0] * self.CELL_SIZE) + self.CELL_SIZE / 2
        pixel_y = (position_grid[1] * self.CELL_SIZE) + self.CELL_SIZE / 2
        return pygame.math.Vector2(pixel_x, pixel_y)

    def set_path(self, grid_path: list):
        self.path = []
        if not grid_path:
            return
        
        for grid_position in grid_path:
            self.path.append(self.grid_to_pixel(grid_position))
        
        self.path_size = len(self.path)
        self.current_index = 0
    
    def update(self, delta_time = 0):
        if self.path and self.current_index < self.path_size:
            target = self.path[self.current_index]

            distance = self.position.distance_to(target)
            if distance < self.CELL_SIZE / 1.5:
                self.current_index += 1

            if self.current_index < self.path_size:
                self.seek(self.path[self.current_index])
            else:
                self.path = []

        self.velocity += self.acceleration * delta_time
        if self.velocity.length() > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)

        self.position += self.velocity * delta_time
        self.acceleration *= 0

    def _apply_force(self, force):
        self.acceleration += force / self.mass

    def seek(self, target):
        desired_velocity = (target - self.position)
        
        if desired_velocity.length() > 0:
            desired_velocity.scale_to_length(self.max_speed)
        
        steering_force = desired_velocity - self.velocity
        if steering_force.length() > self.max_force:
            steering_force.scale_to_length(self.max_force)

        self._apply_force(steering_force)
    

    def draw(self, screen):
        pygame.draw.circle(screen, "red", self.position, self.CELL_SIZE / 2.5)

def draw_grid(screen, ambient, grid_size, cell_size):
    for row in range(grid_size):
        for col in range(grid_size):
            if ambient[row][col] == - 1:
                rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                pygame.draw.rect(screen, "white", rect)

def main():
    pygame.init()

    WIDTH, HEIGHT = 800, 800
    GRID_SIZE = 40 
    CELL_SIZE = WIDTH // GRID_SIZE

    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    CLOCK = pygame.time.Clock()
    
    ambient = sp.criar_ambiente(GRID_SIZE, densidade=25)
    entity = DiscreteMovingEntity(WIDTH // 2, HEIGHT // 2, mass=1, max_speed=250, max_force=300, CELL_SIZE=CELL_SIZE)

    running = True
    while running:
        DELTA_TIME = CLOCK.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    start_pos_grid = entity.pixel_to_grid(entity.position)
                    target_pos_grid = entity.pixel_to_grid(pygame.math.Vector2(event.pos))

                    if 0 <= target_pos_grid[0] < GRID_SIZE and 0 <= target_pos_grid[1] < GRID_SIZE and ambient[target_pos_grid[1]][target_pos_grid[0]] != -1:
                        mark_ambient = [line[:] for line in ambient]
                        sp.anotar_matriz(mark_ambient, GRID_SIZE, start_pos_grid, target_pos_grid)

                        grid_path = []
                        if sp.extrair_caminho(mark_ambient, GRID_SIZE, start_pos_grid, target_pos_grid, grid_path):
                            grid_path.reverse()
                            entity.set_path(grid_path)

        entity.update(DELTA_TIME)

        SCREEN.fill("black")
        draw_grid(SCREEN, ambient, GRID_SIZE, CELL_SIZE)
        entity.draw(SCREEN)
        pygame.draw.circle(SCREEN, "green", pygame.mouse.get_pos(), 8)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()