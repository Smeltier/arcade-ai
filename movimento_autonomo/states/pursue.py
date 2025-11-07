import pygame

from .seek import Seek
from ..outputs import SteeringOutput

class Pursue (Seek):
    def __init__(self, character, target):
        super().__init__(character, target)

        self.max_prediction = self.character.max_prediction

    def execute(self):
        steering = self.get_steering()
        self.character.apply_steering(steering, self.character.delta_time)

    def get_steering(self):
        steering = SteeringOutput()

        if not self.target:
            return steering

        direction = self.target.position - self.character.position
        distance = direction.length()
        speed = self.character.velocity.length()

        if speed <= distance / self.max_prediction:
            prediction = self.max_prediction

        else:
            prediction = distance / speed

        predicted_position = self.target.position + self.target.velocity * prediction

        steering.linear = (predicted_position - self.character.position).normalize()
        steering.linear *= self.max_acceleration

        steering.angular = 0
        return steering

    def enter(self):
        print(f"[DEBUG] {self.character.ID} -> Pursue")
        self.character.change_color("orange")
    
    def exit(self): pass