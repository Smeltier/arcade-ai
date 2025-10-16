import pygame

from blended_steering import BlendedSteering
from outputs import SteeringOutput

class PrioritySteering (State):
   def __init__(self, character, groups: list[BlendedSteering]) -> None:
       super().__init__()

       self.character = character
       self.groups = groups
       self.epsilon = 0.1

   def execute(self):
       steering = self.get_steering()
       self.character.apply_steering(steering, self.character.delta_time)
  
   def get_steering(self) -> SteeringOutput:
       steering = SteeringOutput()

       for group in self.groups:
           steering = group.get_steering()

           if steering.linear.length() > self.epsilon or abs(steering.angular) > self.epsilon:
               return steering
      
       return steering
  
   def enter(self):
       print(f"[DEBUG] {self.character.ID} -> BlendedSteering")
       self.character.change_color("white")
  
   def exit(self): pass