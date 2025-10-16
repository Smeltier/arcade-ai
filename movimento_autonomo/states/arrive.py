import pygame

from states.state import State
from outputs import SteeringOutput

class Arrive (State):
    def __init__(self, character, target):
        super().__init__()

        self.character = character
        self.target = target
        self.max_speed = character.max_speed
        self.max_acceleration = character.max_acceleration
        self.slow_radius = character.slow_radius
        self.target_radius = character.target_radius
        self.time_to_target = character.time_to_target        

    def execute(self):
        steering = self.get_steering()
        self.character.apply_steering(steering, self.character.delta_time)

    def get_steering(self) -> SteeringOutput:
        steering = SteeringOutput()

        if not self.target:
            return steering
            
        self.direction = self.target.position - self.character.position
        self.distance = self.direction.length()

        if self.distance < self.target_radius:
            return SteeringOutput()
        
        if self.distance > self.slow_radius:
            target_speed = self.max_speed
        else:
            target_speed = self.max_speed * self.distance / self.slow_radius

        target_velocity = self.direction.normalize()
        target_velocity *= target_speed

        steering.linear = target_velocity - self.character.velocity
        steering.linear /= self.time_to_target

        if steering.linear.length() > self.max_acceleration:
            steering.linear.scale_to_length(self.max_acceleration)

        steering.angular = 0
        return steering
    
    def enter(self):
        print(f"[DEBUG] {self.character.ID} -> Arrive")
        self.character.change_color("blue")
    
    def exit(self): pass