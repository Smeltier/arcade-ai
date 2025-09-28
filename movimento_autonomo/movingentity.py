import sys
import pygame

from abc import ABC, abstractmethod


class BaseGameEntity (ABC):
    _next_id = 1000

    def __init__(self): 
        self.ID = BaseGameEntity._next_id
        BaseGameEntity._next_id += 1

    @abstractmethod
    def update(self): pass

class State (ABC):
    @abstractmethod
    def execute(entity: BaseGameEntity): pass

    @abstractmethod
    def enter(entity: BaseGameEntity): pass

    @abstractmethod
    def exit(entity: BaseGameEntity): pass


class StateMachine:
    def __init__(self, owner: BaseGameEntity, start_state):
        self.owner = owner
        self.current_state = start_state
        self.previous_state = None
    
    def update(self) -> None:
        self.current_state.execute(self.owner)

    def change_state(self, new_state: State) -> None:
        if new_state is None:
            return
        
        new_state_name = new_state.__class__.__name__
        if not self.owner.state_permissions.get(new_state_name, True):
            print(f"[DEBUG] {self.owner.ID}: NÃO PODE ENTRAR NO ESTADO {new_state_name}.")
            return

        self.current_state.exit(self.owner)
        self.current_state = new_state
        self.current_state.enter(self.owner)


class MovingEntity (BaseGameEntity):
    def __init__(self, x, y, mass = 1, max_speed = 1, max_force = 1, start_state = None, target = None):
        super().__init__()

        # Relativo aos estados da Entidade.
        self.state_machine = StateMachine(self, start_state)
        self.state_permissions = {
            "Seek"    : True,
            "Arrive"  : True,
            "Flee"    : True,
            "Pursuit" : True,
            "Evade"   : True,
        }

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
            self.position.x = WIDTH
        elif self.position.x > WIDTH:
            self.position.x = 0
        if self.position.y < 0:
            self.position.y = HEIGHT
        elif self.position.y > HEIGHT:
            self.position.y = 0

    def draw(self, screen) -> None:
        pygame.draw.circle(screen, self.color, self.position, 5)
        # pygame.draw.circle(screen, "purple", self.position, 300, 1)
        # pygame.draw.circle(screen, "green", self.position, 50, 1)

    def update(self, delta_time = 0) -> None:
        self.state_machine.update()
        self._update_position(delta_time)


class Flee (State):
    def execute(self, entity: MovingEntity):
        desired_velocity = (entity.position - entity.target_position).normalize() * entity.max_speed

        steering_force = desired_velocity - entity.velocity
        if steering_force.length() > entity.max_force:
            steering_force.normalize_ip()
            steering_force *= entity.max_force

        entity.apply_force(steering_force)

    def enter(self, entity: MovingEntity):
        print(f"[DEBUG] {entity.ID}: ENTRANDO NO MODO DE FUGA.")
        entity.change_color("blue")

    def exit(self, entity: MovingEntity):
        print(f"[DEBUG] {entity.ID}: SAINDO DO MODO DE FUGA.")


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
        print(f"[DEBUG] {entity.ID}: ENTRANDO NO MODO DE BUSCA.")
        entity.change_color("red")

    def exit(self, entity: MovingEntity):
        print(f"[DEBUG] {entity.ID}: SAINDO DO MODO DE BUSCA.")


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

        if steering_force.length() > entity.max_force + 100:
            steering_force.normalize_ip()
            steering_force *= entity.max_force

        entity.apply_force(steering_force)

        if entity.distance < 5:
            entity.velocity *= 0
            entity.state_machine.change_state(SEEK)

    def enter(self, entity: MovingEntity):
        print(f"[DEBUG] {entity.ID}: ENTRANDO NO MODO DE CHEGADA.")
        entity.change_color("green")
    
    def exit(self, entity: MovingEntity):
        print(f"[DEBUG] {entity.ID}: SAINDO DO MODO DE CHEGADA.")


class Pursuit(State):
    def execute(self, entity: MovingEntity):
        if not entity.target_entity:
            return

        evader = entity.target_entity
        to_evader = evader.position - entity.position
        distance = to_evader.length()

        if distance < 50:
            entity.state_machine.change_state(ARRIVE)
            return
        elif distance > 300: 
            entity.state_machine.change_state(SEEK)
            return

        relative_speed = entity.velocity.length() + evader.velocity.length()
        look_ahead_time = 0 if relative_speed < 1e-5 else distance / relative_speed

        predicted_pos = evader.position + evader.velocity * look_ahead_time
        entity.change_target(predicted_pos)

        desired_velocity = (predicted_pos - entity.position).normalize() * entity.max_speed
        steering_force = desired_velocity - entity.velocity

        if steering_force.length() > entity.max_force:
            steering_force.scale_to_length(entity.max_force)

        entity.apply_force(steering_force)

    def enter(self, entity: MovingEntity):
        print(f"[DEBUG] {entity.ID}: ENTRANDO NO MODO DE PERSEGUIÇÃO.")
        entity.change_color("purple")

    def exit(self, entity: MovingEntity):
        print(f"[DEBUG] {entity.ID}: SAINDO DO MODO DE PERSEGUIÇÃO.")


class Evade (State):
    def execute(self, entity: MovingEntity):
        if not entity.target_entity: return 
        
        elif entity.distance > 200:
            entity.state_machine.change_state(FLEE)
            return

        pursuer = entity.target_entity
        to_pursuer = pursuer.position - entity.position

        relative_speed = entity.velocity.length() + pursuer.velocity.length()
        if relative_speed < 0.01: look_ahead_time = 0
        else: look_ahead_time = to_pursuer.length() / relative_speed

        predicted_pos = pursuer.position + pursuer.velocity * look_ahead_time
        entity.change_target(predicted_pos)

        desired_velocity = (entity.position - entity.target_position).normalize() * entity.max_speed

        steering_force = desired_velocity - entity.velocity
        if steering_force.length() > entity.max_force:
            steering_force.normalize_ip()
            steering_force *= entity.max_force

        entity.apply_force(steering_force)

    def enter(self, entity: MovingEntity):
        print(f"[DEBUG] {entity.ID}: ENTRANDO NO MODO DE ESCAPE.")
        entity.change_color("violet")
    
    def exit(self, entity: MovingEntity):
        print(f"[DEBUG] {entity.ID}: SAINDO DO MODO DE ESCAPE.")


PURSUIT = Pursuit()
ARRIVE = Arrive(deceleration=1)
EVADE = Evade()
FLEE   = Flee()
SEEK   = Seek()