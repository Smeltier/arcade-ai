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
    def __init__(self, x, y, mass = 0, max_speed = 0, max_force = 0, start_state = None, target = None):
        super().__init__()

        # Relativo aos estados da Entidade.
        self.state_machine = StateMachine(self, start_state)
        self.fleeing       = False
        self.seeking       = False
        self.arriving      = False
        self.pursuing      = False

        # Relativo a movimentação da Entidade.
        self.position     = pygame.math.Vector2(x, y)
        self.velocity     = pygame.math.Vector2(0, 0)
        self.acceleration = pygame.math.Vector2(0, 0)
        self.heading      = pygame.math.Vector2(1, 0)
        self.max_speed    = max_speed
        self.max_force    = max_force
        self.mass         = mass

        # Relativo ao alvo da Entidade.
        self.target_entity: MovingEntity  = target
        self.target_position              = self.position.copy()
        self.target_speed                 = 0
        self.to_target                    = self.target_position - self.position
        self.distance                     = self.to_target.length()
        
        # Relativo a representação da entidade.
        self.color = pygame.Color("white")

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

        self.to_target = self.target_position - self.position
        self.distance  = self.to_target.length()


    def change_color(self, new_color: str):
        if new_color is not None:
            self.color = pygame.Color(new_color)
            self.image = pygame.Surface((20, 10), pygame.SRCALPHA)
            pygame.draw.polygon(self.image, self.color, [(20, 5), (0, 0), (0, 10)])

    def change_target(self, target: pygame.math.Vector2):
        self.target_position = target

    def change_target_speed(self, target: pygame.math.Vector2):
        self.target_speed = target.length()

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
        pygame.draw.circle(screen, self.color, self.position, 5)

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

    def enter(self, entity: MovingEntity):
        if not entity.fleeing:
            print(f"[DEBUG] {entity.ID}: ENTRANDO NO MODO DE FUGA.")
            entity.fleeing = True
            entity.change_color("blue")

    def exit(self, entity: MovingEntity):
        print(f"[DEBUG] {entity.ID}: SAINDO DO MODO DE FUGA.")
        entity.fleeing = False

class Seek (State):
    def execute(self, entity: MovingEntity):
        if entity.distance <= 50:
            entity.state_machine.change_state(ARRIVE)
        elif entity.target_entity is not None and entity.distance <= 200:
            entity.state_machine.change_state(PURSUIT)

        desired_velocity = (entity.target_position - entity.position).normalize() * entity.max_speed
        steering_force = desired_velocity - entity.velocity

        if steering_force.length() > entity.max_force:
            steering_force.normalize_ip()
            steering_force *= entity.max_force

        entity.apply_force(steering_force)

    def enter(self, entity: MovingEntity):
        if not entity.seeking:
            print(f"[DEBUG] {entity.ID}: ENTRANDO NO MODO DE BUSCA.")
            entity.seeking = True
            entity.change_color("red")

    def exit(self, entity: MovingEntity):
        print(f"[DEBUG] {entity.ID}: SAINDO DO MODO DE BUSCA.")
        entity.seeking = False

class Arrive (State):
    def __init__(self, deceleration = 2):
        self.deceleration = deceleration # 3 - slow | 2 - normal | 1 - fast
        self.deceleration_tweaker = 0.3

    def execute(self, entity: MovingEntity):

        if not 0 < entity.distance <= 50:
            entity.state_machine.change_state(SEEK)

        speed = entity.distance / (self.deceleration * self.deceleration_tweaker)
        speed = min(speed, entity.max_speed)

        desired_velocity = entity.to_target * speed / max(1, entity.distance)
        steering_force = desired_velocity - entity.velocity

        if steering_force.length() > entity.max_force:
            steering_force.normalize_ip()
            steering_force *= entity.max_force

        entity.apply_force(steering_force)

        if entity.distance < 5:
            entity.velocity *= 0
            entity.state_machine.change_state(SEEK)

    def enter(self, entity: MovingEntity):
        if not entity.arriving:
            print(f"[DEBUG] {entity.ID}: ENTRANDO NO MODO DE CHEGADA.")
            entity.arriving = True
            entity.change_color("green")
    
    def exit(self, entity: MovingEntity):
        print(f"[DEBUG] {entity.ID}: SAINDO DO MODO DE CHEGADA.")
        entity.arriving = False

class Pursuit (State):
    def execute(self, entity: MovingEntity):
        if not entity.target_entity: return 
        
        if entity.distance < 50: 
            entity.state_machine.change_state(ARRIVE)
            return
        elif entity.distance > 200:
            entity.state_machine.change_state(SEEK)
            return

        evader = entity.target_entity
        to_evader = evader.position - entity.position
        relative_heading = entity.heading.dot(evader.heading)

        if to_evader.dot(entity.heading) > 0 and relative_heading < -0.95:
            entity.state_machine.change_state(SEEK)
            return

        relative_speed = entity.velocity.length() + evader.velocity.length()
        if relative_speed < 0.01: look_ahead_time = 0
        else: look_ahead_time = to_evader.length() / relative_speed

        predicted_pos = evader.position + evader.velocity * look_ahead_time
        entity.change_target(predicted_pos)

        desired_velocity = (entity.target_position - entity.position).normalize() * entity.max_speed

        steering_force = desired_velocity - entity.velocity
        if steering_force.length() > entity.max_force:
            steering_force.normalize_ip()
            steering_force *= entity.max_force

        entity.apply_force(steering_force)
    
    def enter(self, entity: MovingEntity):
        if not entity.pursuing:
            print(f"[DEBUG] {entity.ID}: ENTRANDO NO MODO DE PERSEGUIÇÃO.")
            entity.pursuing = True
            entity.change_color("violet")
    
    def exit(self, entity: MovingEntity):
        print(f"[DEBUG] {entity.ID}: SAINDO DO MODO DE PERSEGUIÇÃO.")
        entity.pursuing = False

PURSUIT = Pursuit()
ARRIVE = Arrive(deceleration=1)
FLEE   = Flee()
SEEK   = Seek()