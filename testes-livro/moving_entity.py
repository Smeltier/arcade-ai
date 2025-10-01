import pygame
from steering_output import SteeringOutput
from state_machine import StateMachine
from states import SeekState

class MovingEntity:
    _next_ID = 0

    def __init__(self, x, y, max_speed=1, max_force=1, max_acceleration=1, mass=1, start_state=None):
        self.ID = MovingEntity._next_ID
        MovingEntity._next_ID += 1

        self.position = pygame.math.Vector2(x, y)
        self.velocity = pygame.math.Vector2(0, 0)
        self.acceleration = pygame.math.Vector2(0, 0)
        self.mass = mass
        self.max_speed = max_speed
        self.max_force = max_force
        self.max_acceleration = max_acceleration
        self.delta_time = 0.1
        
        self.target: MovingEntity = None
        self.distance = 0

        self.arrive_behavior = None
        self.flee_behavior = None
        self.seek_behavior = None
        self.pursue_behavior = None
        self.evade_behavior = None
        
        self.world_width = 0
        self.world_heigth = 0
        self.color = pygame.Color("white")

        self.state_machine = StateMachine(self, start_state)

    def update(self):
        if self.state_machine:
            self.state_machine.update()
        
        self._update_distance()
        self._limit_entity()

    def _update_distance(self):
        if self.target:
            to_target = self.target.position - self.position
            self.distance = to_target.length()

    def _limit_entity(self):
        if self.position.x > self.world_width:
            self.position.x = self.world_width
        elif self.position.x < 0:
            self.position.x = 0

        if self.position.y > self.world_heigth:
            self.position.y = self.world_heigth
        elif self.position.y < 0:
            self.position.y = 0

    def _apply_force(self, steering: SteeringOutput):
        if steering.linear.length_squared() > self.max_force * self.max_force:
            steering.linear.scale_to_length(self.max_force)
            
        self.acceleration += steering.linear / self.mass

    def apply_steering(self, steering: SteeringOutput, delta_time):
        self._apply_force(steering)

        self.velocity += self.acceleration * delta_time

        if self.velocity.length() > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)

        self.position += self.velocity * delta_time
        self.acceleration *= 0

    def change_color(self, color):
        self.color = pygame.Color(color)