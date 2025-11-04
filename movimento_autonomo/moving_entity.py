import math
import pygame 

from .base_game_entity import BaseGameEntity
from .world            import World
from .state_machine    import StateMachine
from .outputs          import SteeringOutput, KinematicSteeringOutput

class MovingEntity (BaseGameEntity):
    def __init__(
            self, 
            x, 
            y, 
            world: World, 
            mass                     = 1, 
            max_speed                = 1, 
            max_acceleration         = 1, 
            max_force                = 1, 
            max_prediction           = 1.0, 
            max_rotation             = 50, 
            max_angular_acceleration = 1000,
            offset                   = 2.0, 
            radius                   = 1.0, 
            rate                     = 0.4, 
            orientation              = 1,
            threshold                = 100, 
            decay_coefficient        = 100000, 
            time_to_target           = 0.001, 
            target_radius            = 2.0, 
            slow_radius              = 50, 
            detection_radius         = 50, 
            effect_radius            = 20, 
            avoid_distance           = 25, 
            collision_ray            = 50,
            start_state              = None, 
            color: str               = "white"
        ):

        super().__init__()

        
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.acceleration = pygame.Vector2(0, 0)
        self.mass = mass
        self.orientation = 0.0
        self.rotation = 1

        self.max_speed = max_speed
        self.max_force = max_force
        self.max_acceleration = max_acceleration
        self.max_prediction = max_prediction
        self.max_rotation = max_rotation
        self.max_angular_acceleration = max_angular_acceleration

        self.wander_offset = offset
        self.wander_radius = radius
        self.wander_rate = rate
        self.wander_orientation = orientation 
        
        self.threshold = threshold
        self.decay_coefficient = decay_coefficient
        self.time_to_target = time_to_target
        self.target_radius = target_radius
        self.slow_radius = slow_radius
        self.detection_radius = detection_radius
        self.effect_radius = effect_radius
        self.avoid_distance = avoid_distance
        self.collision_ray = collision_ray

        self.start_state = start_state
        self.state_machine = StateMachine(self, start_state)

        self.world: World = world
        self.delta_time = 0.1

        self.color = color

    def update(self, delta_time) -> None:
        self.delta_time = delta_time
        
        if self.state_machine:
            self.state_machine.update()
        
        self._limit_entity()

    def apply_steering(self, steering: SteeringOutput, delta_time) -> None:
        self.velocity += steering.linear * delta_time

        if self.velocity.length() > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)

        self.position += self.velocity * delta_time
        self.orientation += steering.angular * delta_time

        self.acceleration = pygame.Vector2(0,0)

    def apply_kinematic_steering(self, steering: KinematicSteeringOutput, delta_time) -> None:
        max_speed = self.max_speed

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
        max_force = self.max_force

        if steering.linear.length_squared() > max_force * max_force:
            steering.linear.scale_to_length(max_force)
            
        # Force = mass * acceleration
        self.acceleration += steering.linear / self.mass

    def change_color(self, color) -> None:
        self.color = pygame.Color(color)

    def draw(self, SCREEN) -> None:
        if self.velocity.length() > 0:
            direction = self.velocity.normalize()        
            line_length = 15  
            line_end = self.position + direction * line_length

            pygame.draw.line(SCREEN, "white",  
                            (int(self.position.x), int(self.position.y)),
                            (int(line_end.x), int(line_end.y)), 2) 

            direction = pygame.math.Vector2(math.cos(self.orientation), math.sin(self.orientation))
            line_length = 10
            line_end = self.position + direction * line_length

            pygame.draw.line(SCREEN, "grey",  
                            (int(self.position.x), int(self.position.y)),
                            (int(line_end.x), int(line_end.y)), 2)


        pygame.draw.circle(SCREEN, self.color, 
                           (int(self.position.x), int(self.position.y)), 8)

    def new_orientation(self, velocity) -> float:
        if velocity.length() <= 0:
            return self.orientation

        return math.atan2(-velocity.x, velocity.y)