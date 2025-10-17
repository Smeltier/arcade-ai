import math
import pygame

from states.align import Align
from outputs import SteeringOutput

class Face(Align):
    def __init__(self, character, target) -> None:
        super().__init__(character, target)

    def execute(self):
        steering = self.get_steering()
        self.character.apply_steering(steering, self.character.delta_time)
    
    def get_steering(self) -> SteeringOutput:
        direction = self.target.position - self.character.position

        if direction.length() == 0:
            return SteeringOutput()
        
        old_target = self.target
        temporary_target = type(self.target)()
        temporary_target.orientation = math.atan2(-direction.x, direction.y)

        self.target = temporary_target
        
        steering = super().get_steering()

        self.target = old_target
        return steering

    def enter(self):
        print(f"[DEBUG] {self.character.ID} -> Face")
        self.character.change_color("white")
    
    def exit(self): pass