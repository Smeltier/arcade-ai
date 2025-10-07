import math
import pygame 

from state_machine import StateMachine
from states import SteeringOutput, KinematicSteeringOutput

class MovingEntity:
    _next_ID = 0

    def __init__(self, x, y, max_speed=1, max_force=1, max_acceleration=1, mass=1, start_state=None):
        self.ID = MovingEntity._next_ID
        MovingEntity._next_ID += 1

        self.position = pygame.math.Vector2(x, y)
        self.velocity = pygame.math.Vector2(0, 0)
        self.acceleration = pygame.math.Vector2(0, 0)
        self.mass = mass

        self.target: MovingEntity = self
        self.orientation = 0.0

        self.rotation = 1
        self.time_to_target = 0.25
        self.distance = 0

        self.target_radius = 2.0
        self.slow_radius = 20
        self.detection_radius = 50

        self.max_speed = max_speed
        self.max_force = max_force
        self.max_acceleration = max_acceleration
        self.max_prediction = 1.0
        self.max_rotation = 50
        self.max_angular_acceleration = 50

        self.wander_offset = 2.0
        self.wander_radius = 1.0
        self.wander_rate = 0.4
        self.wander_orientation = 1 

        self.start_state = start_state
        self.state_machine = StateMachine(self, self.start_state)

        self.color = pygame.Color("white")

        self.world_width = 0
        self.world_heigth = 0
        self.delta_time = 0.1

    def _update_distance(self):
        if self.target:
            to_target = self.target.position - self.position
            self.distance = to_target.length()

    def _limit_entity(self):
        if self.position.x > self.world_width:
            self.position.x = 1
        elif self.position.x < 0:
            self.position.x = self.world_width - 1

        if self.position.y > self.world_heigth:
            self.position.y = 1
        elif self.position.y < 0:
            self.position.y = self.world_heigth - 1

    def _apply_force(self, steering: SteeringOutput):
        if steering.linear.length_squared() > self.max_force * self.max_force:
            steering.linear.scale_to_length(self.max_force)
            
        self.acceleration += steering.linear / self.mass

    def update(self):
        self._update_distance()
        
        if self.state_machine:
            self.state_machine.update()
        
        self._limit_entity()

    def apply_steering(self, steering: SteeringOutput, delta_time):
        self._apply_force(steering)

        self.position += self.velocity * delta_time
        self.orientation += self.rotation * delta_time

        self.orientation += steering.angular * delta_time

        self.velocity += steering.linear * delta_time
        if self.velocity.length() > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)

    def apply_kinematic_steering(self, steering: KinematicSteeringOutput, delta_time):
        self.orientation += steering.rotation * delta_time

        self.velocity = steering.velocity
        if self.velocity.length() > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)

        self.position += self.velocity * delta_time

    def change_color(self, color) -> None:
        self.color = pygame.Color(color)

    def change_world_resolution(self, width: float, heigth: float) -> None:
        self.world_width = width
        self.world_heigth = heigth

    # TODO - Verificar a implementação
    def new_orientation(self, velocity) -> float:
        if velocity.length() <= 0:
            return self.orientation

        return math.atan2(-velocity.x, velocity.y)