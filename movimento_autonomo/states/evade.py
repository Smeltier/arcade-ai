import pygame

from .flee import Flee
from ..outputs import SteeringOutput

class Evade(Flee):
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
        self.distance = direction.length()
        speed = self.character.velocity.length()

        if speed <= self.distance / self.max_prediction:
            prediction = self.max_prediction

        else:
            prediction = self.distance / speed

        predicted_position = self.target.position + self.target.velocity * prediction

        steering.linear = (self.character.position - predicted_position).normalize()
        steering.linear *= self.max_acceleration

        steering.angular = 0
        return steering

    def enter(self):
        print(f"[DEBUG] {self.character.ID} -> Evade")
        self.character.change_color("purple")
    
    def exit(self): pass