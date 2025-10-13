import math
import pygame 

from base_game_entity import BaseGameEntity
from world            import World
from atributes        import Limits, WanderThresholds, BehaviorThresholds
from state_machine    import StateMachine
from outputs          import SteeringOutput, KinematicSteeringOutput

class MovingEntity (BaseGameEntity):
    def __init__(
            self, 
            x, y, 
            world: World, 
            limits: Limits, 
            wander_threshold: WanderThresholds | None = None, 
            behavior_threshold: BehaviorThresholds | None = None, 
            mass=1, 
            start_state=None, 
            color="white"
        ):

        super().__init__()

        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.acceleration = pygame.Vector2(0, 0)
        self.mass = mass
        self.orientation = 0.0
        self.rotation = 1

        self.world: World = world
        self.limits: Limits = limits
        self.wander_threshold: WanderThresholds | None = wander_threshold
        self.behavior_threshold: BehaviorThresholds | None = behavior_threshold
        self.delta_time = 0.1

        self.start_state = start_state
        self.state_machine = StateMachine(self, start_state)

        self.color = color

    def update(self, delta_time) -> None:
        self.delta_time = delta_time
        
        if self.state_machine:
            self.state_machine.update()
        
        self._limit_entity()

    def apply_steering(self, steering: SteeringOutput, delta_time) -> None:
        max_speed = self.limits.max_speed

        self._apply_force(steering)

        self.velocity += steering.linear * delta_time

        if self.velocity.length() > max_speed:
            self.velocity.scale_to_length(max_speed)

        self.position += self.velocity * delta_time

        self.orientation += self.rotation * delta_time
        self.orientation += steering.angular * delta_time

        self.acceleration *= 0

    def apply_kinematic_steering(self, steering: KinematicSteeringOutput, delta_time) -> None:
        max_speed = self.limits.max_speed

        self.orientation += steering.rotation * delta_time

        self.velocity = steering.velocity

        if self.velocity.length() > max_speed:
            self.velocity.scale_to_length(max_speed)

        self.position += self.velocity * delta_time

    def _limit_entity(self) -> None:
        width, height = self.world.width, self.world.height

        if self.position.x > width:
            self.position.x = 1
        if self.position.x < 0:
            self.position.x = width - 1
        if self.position.y > height:
            self.position.y = 1
        if self.position.y < 0:
            self.position.y = height - 1

    def _apply_force(self, steering: SteeringOutput) -> None:
        max_force = self.limits.max_force

        if steering.linear.length_squared() > max_force * max_force:
            steering.linear.scale_to_length(max_force)
            
        # Force = mass * acceleration
        self.acceleration += steering.linear / self.mass

    def change_color(self, color) -> None:
        self.color = pygame.Color(color)

    def draw(self, SCREEN) -> None:
        if self.velocity.length() > 0:
            direction = self.velocity.normalize()        
            line_length = 10  
            line_end = self.position + direction * line_length

            pygame.draw.line(SCREEN, "white",  
                            (int(self.position.x), int(self.position.y)),
                            (int(line_end.x), int(line_end.y)), 2) 

        pygame.draw.circle(SCREEN, self.color, 
                           (int(self.position.x), int(self.position.y)), 8)

    # TODO -> Verificar implementação
    def new_orientation(self, velocity) -> float:
        if velocity.length() <= 0:
            return self.orientation

        return math.atan2(-velocity.x, velocity.y)


# def __init__(self, x, y, max_speed=1, max_force=1, max_acceleration=1, mass=1, start_state=None):
#     super().__init__()

#     self.position = pygame.math.Vector2()
#     self.velocity = pygame.math.Vector2(0, 0)
#     self.acceleration = pygame.math.Vector2(0, 0)
#     self.mass = mass
#     self.target: MovingEntity = self
#     self.orientation = 0.0
#     self.target_list = []
#     self.target_list.append(self.target)
#     self.distance = 0
#     self.max_speed = max_speed
#     self.max_force = max_force
#     self.max_acceleration = max_acceleration
#     self.max_prediction = 1.0
#     self.max_rotation = 50
#     self.max_angular_acceleration = 50
#     self.start_state = start_state
#     self.state_machine = StateMachine(self, self.start_state)
#     self.color = pygame.Color("white")
#     self.delta_time = 0.1
#     self.wander_offset = 2.0
#     self.wander_radius = 1.0
#     self.wander_rate = 0.4
#     self.wander_orientation = 1 
#     self.threshold = 100
#     self.decay_coefficient = 100000
#     self.time_to_target = 0.25
#     self.target_radius = 2.0
#     self.slow_radius = 20
#     self.detection_radius = 50
#     self.effect_radius = 20
#     self.avoid_distance = 25
#     self.collision_ray = 50
#     self.rotation = 1