import pygame

from states.state import State
from outputs import SteeringOutput

class Seek (State):
    def __init__(self, character, target):
        super().__init__()

        self.character = character
        self.target = target
        self.max_acceleration = character.max_acceleration

    def execute(self):
        steering = self.get_steering()
        self.character.apply_steering(steering, self.character.delta_time)

    def get_steering(self):
        steering = SteeringOutput()

        if not self.target:
            return steering

        steering.linear = self.target.position - self.character.position
        steering.linear.normalize_ip()
        steering.linear *= self.max_acceleration

        steering.angular = 0
        return steering  

    def enter(self):
        print(f"[DEBUG] {self.character.ID} -> Seek")
        self.character.change_color("green")
    
    def exit(self): pass