import pygame

class Character ():
    def __init__(self, x, y, environment):
        self.position = pygame.Vector2((x, y))
        self.environment = environment
        self.current_orientation = 0 # 1 = up, 2 = down, 3 = left, 4 = right.
        self.next_orientation = 0 
        self.sprites = self._load_sprites()
        self.animation_timer = 0.0
        self.animation_speed = 0.15
        self.animation_frame = 0
        self.total_points = 0
        self.speed = 2

    def _update_orientation(self, keys):
        key_map = {
            pygame.K_UP : 1,
            pygame.K_DOWN : 2,
            pygame.K_LEFT : 3,
            pygame.K_RIGHT : 4
        }

        for k, ft in key_map.items():
            if keys[k]:
                self.next_orientation = ft

    def _is_on_grid(self): 
        row = int(self.position.y // self.environment.cell_height)
        col = int(self.position.x // self.environment.cell_width)

        center_x = (col * self.environment.cell_width) + (self.environment.cell_width / 2)
        center_y = (row * self.environment.cell_height) + (self.environment.cell_height / 2)

        if abs(self.position.x - center_x) < self.speed and abs(self.position.y - center_y) < self.speed:
            self.position.x = center_x
            self.position.y = center_y

            return True
        
        return False
    
    def _make_point(self):
        row = int(self.position.y // self.environment.cell_height)
        col = int(self.position.x // self.environment.cell_width)

        if not (0 <= row < len(self.environment.matrix) and 0 <= col < len(self.environment.matrix[0])):
            return

        point_type = self.environment.matrix[row][col]

        if point_type == 1:
            self.environment.matrix[row][col] = 0
            self.total_points += 10
            self.environment.total_tablets -= 1

        elif point_type == 2:
            self.environment.matrix[row][col] = 0
            self.total_points += 20
            self.environment.total_tablets -= 1

    def _handle_moviment(self):
        if self._is_on_grid():
            if self._can_move(self.next_orientation):
                self.current_orientation = self.next_orientation
            elif not self._can_move(self.current_orientation):
                self.current_orientation = 0

        if self.current_orientation == 1:
            self.position.y -= self.speed
        elif self.current_orientation == 2:
            self.position.y += self.speed
        elif self.current_orientation == 3:
            self.position.x -= self.speed
        elif self.current_orientation == 4:
            self.position.x += self.speed

    def _load_sprites(self):
        sprites = []
        for cnt in range(0, 3):
            sprite = pygame.transform.scale(pygame.image.load(f'pacman/images/pacman_eat_{cnt}.png'), (40, 40))
            sprites.append(sprite)
        return sprites
    
    def update(self, keys, delta_time):
        self._update_orientation(keys)
        self._handle_moviment()
        self._make_point()

        if self.current_orientation != 0:
            self.animation_timer += delta_time / 2

            if self.animation_timer >= self.animation_speed:
                self.animation_timer -= self.animation_speed
                self.animation_frame = (self.animation_frame + 1) % len(self.sprites)
        else:
            self.animation_frame = 0

    def draw(self, screen):
        x, y = int(self.position.x), int(self.position.y)
        sprite = self.sprites[self.animation_frame]

        angle = 0

        if self.current_orientation == 1:
            angle = 90
        elif self.current_orientation == 2:
            angle = -90
        elif self.current_orientation == 3:
            angle = 180

        rotated_sprite = pygame.transform.rotate(sprite, angle)

        rect = rotated_sprite.get_rect(center=(x, y))
        screen.blit(rotated_sprite, rect)

    def _can_move(self, direction):
        col = int(self.position.x // self.environment.cell_width)
        row = int(self.position.y // self.environment.cell_height)

        if direction == 1:   row -= 1
        elif direction == 2: row += 1
        elif direction == 3: col -= 1
        elif direction == 4: col += 1
        elif direction == 0: return True
        
        if (0 <= row < len(self.environment.matrix) and 0 <= col < len(self.environment.matrix[0])):
            
            if self.environment.matrix[row][col] != -1:
                return True

        return False