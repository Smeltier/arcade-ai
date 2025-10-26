import pygame

class Character ():
    def __init__(self, x, y, environment):
        self.position = pygame.Vector2((x, y))
        self.environment = environment
        self.orientation = 0 # 1 = up, 2 = down, 3 = left, 4 = right.
        self.sprites = self._load_sprites()
        self.animation_timer = 0.0
        self.animation_speed = 0.1
        self.animation_frame = 0
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
                self.orientation = ft

    def _orientated_moviment(self):
        if self.orientation == 1 and self.can_move(1):
            self.position.y -= self.speed
        elif self.orientation == 2 and self.can_move(2):
            self.position.y += self.speed
        elif self.orientation == 3 and self.can_move(3):
            self.position.x -= self.speed
        elif self.orientation == 4 and self.can_move(4):
            self.position.x += self.speed

    def _load_sprites(self):
        sprites = []
        for cnt in range(0, 3):
            sprite = pygame.transform.scale(pygame.image.load(f'pacman/images/pacman_eat_{cnt}.png'), (40, 40))
            sprites.append(sprite)
        return sprites
    
    def update(self, keys, delta_time):
        self._update_orientation(keys)
        self._orientated_moviment()

        self.animation_timer += delta_time / 2

        if self.animation_timer >= self.animation_speed:
            self.animation_timer -= self.animation_speed
            self.animation_frame = (self.animation_frame + 1) % len(self.sprites)

    def draw(self, screen):
        x, y = int(self.position.x), int(self.position.y)
        sprite = self.sprites[self.animation_frame]

        angle = 0
        if self.orientation == 1:
            angle = 90
        elif self.orientation == 2:
            angle = -90
        elif self.orientation == 3:
            angle = 180

        rotated_sprite = pygame.transform.rotate(sprite, angle)

        rect = rotated_sprite.get_rect(center=(x, y))
        screen.blit(rotated_sprite, rect)

    def can_move(self, direction):
        # new_position = self.position.copy()
        # speed = 1

        # if direction == 1:
        #     new_position.y -= speed
        # if direction == 2:
        #     new_position.y += speed
        # if direction == 3:
        #     new_position.x -= speed
        # if direction == 4:
        #     new_position.x += speed

        # row = int(new_position.y // self.environment.cell_height)
        # col = int(new_position.x // self.environment.cell_width)

        # if self.environment.matrix[row][col] == -1:
        #     return False

        return True            