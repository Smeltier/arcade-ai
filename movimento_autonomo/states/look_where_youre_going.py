import pygame

from .align import Align
from ..outputs import SteeringOutput

class LookWhereYoureGoing (Align):
    def __init__(self, character, target) -> None:
        super().__init__(character, target)

    def execute(self):
        return super().execute()
    
    def get_steering(self) -> SteeringOutput:
        if self.character.velocity.length() == 0:
            return SteeringOutput()
            
        return SteeringOutput()

    def enter(self):
        return super().enter()
    
    def exit(self): 
        return super().exit()