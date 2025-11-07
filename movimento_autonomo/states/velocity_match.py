import pygame

from .state import State
from ..outputs import SteeringOutput

class VelocityMatch (State):
    def __init__(self, character, target) -> None:
        super().__init__()

        self.character = character
        self.target = target

    def execute(self):
        return super().execute()
    
    def get_steering(self) -> SteeringOutput:
        steering = SteeringOutput()

        steering.linear = self.target.velocity - self.character.velocity
        steering.linear /= self.character.time_to_target

        if steering.linear.length() > self.character.max_acceleration:
            steering.linear.scale_to_length(self.character.max_acceleration)

        steering.angular = 0.0
        return steering
    
    def enter(self):
        print(f"[DEBUG] {self.character.ID} -> VelocityMatch")
        self.character.change_color("white")
    
    def exit(self): pass