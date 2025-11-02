import pygame

class PacMan ():
    def __init__(self, x, y, environment):
        self.position = pygame.Vector2((x, y))
        self.environment = environment

        self._current_orientation = 0
        self._next_orientation = 0

        self._sprites = self._load_sprites()
        self._animation_timer = 0.0
        self._animation_speed = 0.15
        self._animation_frame = 0

        self.eat_sound = pygame.mixer.Sound('pacman/sounds/Waka Waka.mp3')
        self.eat_sound.set_volume(0.4)

        self.total_points = 0
        self._speed = 2

    def _update_orientation(self, keys) -> None:
        """ Atualiza a próxima orientação do personagem baseado na tecla pressionada. """

        key_map = { pygame.K_UP : 1, pygame.K_DOWN : 2, pygame.K_LEFT : 3, pygame.K_RIGHT : 4 }

        for k, ft in key_map.items():
            if keys[k]:
                self._next_orientation = ft

    def _is_on_grid(self) -> bool: 
        """ Verifica se o personagem está dentro da célula atual da matriz. """

        row = int(self.position.y // self.environment.cell_height)
        col = int(self.position.x // self.environment.cell_width)

        center_x = (col * self.environment.cell_width) + (self.environment.cell_width / 2)
        center_y = (row * self.environment.cell_height) + (self.environment.cell_height / 2)

        if abs(self.position.x - center_x) < self._speed and abs(self.position.y - center_y) < self._speed:
            self.position.x = center_x
            self.position.y = center_y

            return True
        
        return False
    
    def _make_point(self) -> None:
        """ Aumenta a pontuação baseado em qual tipo de pastilha o personagem comeu. """

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
            
            self.environment.set_vulnerable()

    def _handle_moviment(self) -> None:
        """ Movimenta o personagem baseado na tecla que foi pressionada. """

        if self._is_on_grid():
            self._play_eat_sound()
            self._make_point()

            if self._can_move(self._next_orientation):
                self.current_orientation = self._next_orientation
            elif not self._can_move(self.current_orientation):
                self.current_orientation = 0

        if self.position.x <= 15: 
            self.position.x = 880
        if self.position.x >= 885: 
            self.position.x = 20

        if self.current_orientation == 1:
            self.position.y -= self._speed
        elif self.current_orientation == 2:
            self.position.y += self._speed
        elif self.current_orientation == 3:
            self.position.x -= self._speed
        elif self.current_orientation == 4:
            self.position.x += self._speed

    def _load_sprites(self) -> list[pygame.Surface]:
        """ Carrega os sprites do personagem. """

        sprites = []
        for cnt in range(0, 3):
            sprite = pygame.transform.scale(pygame.image.load(f'pacman_game/images/pacman_eat_{cnt}.png'), (40, 40))
            sprites.append(sprite)

        return sprites
    
    def _can_move(self, direction) -> bool:
        """ Verifica se o personagem pode se mover. """

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
    
    def _update_sprite(self, delta_time):
        if self.current_orientation == 0:
            self.current_orientation = self.previous_orientation
            return

        self.animation_timer += delta_time / 2

        if self.animation_timer >= self._animation_speed:
            self.animation_timer -= self._animation_speed
            self.animation_frame = (self.animation_frame + 1) % len(self._sprites)

        self.previous_orientation = self.current_orientation

    def _play_eat_sound(self):
        row = int(self.position.y // self.environment.cell_height)
        col = int(self.position.x // self.environment.cell_width)

        point_type = 0
        if 0 <= row < len(self.environment.matrix) and 0 <= col < len(self.environment.matrix[0]):
            point_type = self.environment.matrix[row][col]

        if point_type in (1, 2) and self.current_orientation != 0:
            if self.eat_sound.get_num_channels() == 0:
                self.eat_sound.play(loops=-1)
        else:
            self.eat_sound.stop()

    def update(self, keys, delta_time):
        self._update_orientation(keys)
        self._handle_moviment()
        self._update_sprite(delta_time)

    def draw(self, screen) -> None:
        """ Desenha o personagem baseado na orientação atual. """

        x, y = int(self.position.x), int(self.position.y)
        sprite = self._sprites[self._animation_frame]

        angle = 0

        if self._current_orientation == 1:
            angle = 90
        elif self._current_orientation == 2:
            angle = -90
        elif self._current_orientation == 3:
            angle = 180

        rotated_sprite = pygame.transform.rotate(sprite, angle)

        rect = rotated_sprite.get_rect(center=(x, y))
        screen.blit(rotated_sprite, rect)