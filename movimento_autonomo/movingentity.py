import sys
from abc import ABC, abstractmethod

import pygame

class BaseGameEntity (ABC):
    _next_id = 1000

    def __init__(self): 
        self.ID = BaseGameEntity._next_id
        BaseGameEntity._next_id += 1

    @abstractmethod
    def update(self): pass

class MovingEntity (BaseGameEntity):
    def __init__(self, x, y, mass, max_speed, max_force, start_state) -> None:

        # Relativo aos estados da Entidade.
        self.state_machine = StateMachine(self, start_state)
        self.pursue        = True
        self.seeking       = False

        # Relativo a movimentação da Entidade.
        self.position     = pygame.math.Vector2(x, y)
        self.velocity     = pygame.math.Vector2(0, 0)
        self.acceleration = pygame.math.Vector2(0, 0)
        self.heading      = pygame.math.Vector2(1, 0)
        self.max_speed    = max_speed
        self.max_force    = max_force
        self.mass         = mass

        # Relativo ao alvo da Entidade.
        self.target_position = None
        
        # Relativo a representação da entidade.
        self.image = pygame.Surface((20, 10), pygame.SRCALPHA)
        self.color = "white"
        pygame.draw.polygon(self.image, self.color, [(20, 5), (0, 0), (0, 10)])

    # Segunda Lei de Newton := F = m x a
    def apply_force(self, force) -> None:
        """ Utiliza a Segunda Lei de Newton para atualizar a aceleração da entidade. """
        self.acceleration += force / self.mass

    def _update_position(self, delta_time = 0):
        self.velocity += self.acceleration * delta_time

        if self.velocity.length() > self.max_speed:
            self.velocity.normalize_ip()
            self.velocity *= self.max_speed
        
        self.position += self.velocity * delta_time
        self.acceleration *= 0

        if self.velocity.length_squared() > 0:
            self.heading = self.velocity.normalize()

    def change_color(self, new_color: str):
        if new_color is not None:
            self.color = new_color
            self.image = pygame.Surface((20, 10), pygame.SRCALPHA)
            pygame.draw.polygon(self.image, self.color, [(20, 5), (0, 0), (0, 10)])

    def change_target(self, target: pygame.math.Vector2):
        self.target_position = target

    def limit_the_entity(self, WIDTH, HEIGHT):
        if self.position.x < 0:
            self.position.x = HEIGHT
        elif self.position.x > HEIGHT:
            self.position.x = 0
        elif self.position.y < 0:
            self.position.y = WIDTH
        elif self.position.y > WIDTH:
            self.position.y = 0

    def draw(self, screen) -> None:
        angle = self.heading.angle_to(pygame.math.Vector2(1, 0))
        rotated_img = pygame.transform.rotozoom(self.image, angle, 1)
        rect = rotated_img.get_rect(center = self.position)
        screen.blit(rotated_img, rect)

    def update(self, delta_time = 0) -> None:
        self.state_machine.update()
        self._update_position(delta_time)

class State (ABC):
    @abstractmethod
    def execute(entity: MovingEntity): pass

    @abstractmethod
    def enter(entity: MovingEntity): pass

    @abstractmethod
    def exit(entity: MovingEntity): pass

class StateMachine:
    def __init__(self, owner: MovingEntity, start_state):
        self.owner = owner
        self.current_state = start_state
    
    def update(self) -> None:
        self.current_state.execute(self.owner)

    def change_state(self, new_state: State) -> None:
        if new_state is None:
            return

        self.current_state.exit(self.owner)
        self.current_state = new_state
        self.current_state.enter(self.owner)

class Flee (State):
    def execute(self, entity: MovingEntity):
        desired_velocity = (entity.position - entity.target_position).normalize() * entity.max_speed

        steering_force = desired_velocity - entity.velocity
        if steering_force.length() > entity.max_force:
            steering_force.normalize_ip()
            steering_force *= entity.max_force

        entity.apply_force(steering_force)

        if entity.position == entity.target_position:
            entity.state_machine.change_state(SEEK)

    def enter(self, entity: MovingEntity):
        if not entity.pursue:
            print(f"[DEBUG] {entity.ID}: ENTRANDO NO MODO DE FUGA.")
            entity.pursue = True
            entity.change_color("green")

    def exit(self, entity: MovingEntity):
        print(f"[DEBUG] {entity.ID}: SAINDO DO MODO DE FUGA.")
        entity.pursue = False

class Seek (State):
    def execute(self, entity: MovingEntity):
        desired_velocity = (entity.target_position - entity.position).normalize() * entity.max_speed
        
        steering_force = desired_velocity - entity.velocity

        if steering_force.length() > entity.max_force:
            steering_force.normalize_ip()
            steering_force *= entity.max_force

        entity.apply_force(steering_force)

        if entity.position == entity.target_position:
            entity.state_machine.change_state(FLEE)

    def enter(self, entity: MovingEntity):
        if not entity.seeking:
            print(f"[DEBUG] {entity.ID}: ENTRANDO NO MODO DE FUGA.")
            entity.seeking = True
            entity.change_color("red")

    def exit(self, entity: MovingEntity):
        print(f"[DEBUG] {entity.ID}: SAINDO DO MODO DE FUGA.")
        entity.seeking = False

FLEE = Flee()
SEEK = Seek()