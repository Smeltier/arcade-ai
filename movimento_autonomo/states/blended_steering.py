import pygame

from states.state import State
from outputs import SteeringOutput, BehaviorAndWeight

class BlendedSteering (State):
    def __init__(self, character, behaviors: list[BehaviorAndWeight]) -> None:
        self.behaviors: list = behaviors
        self.character = character
        self.max_acceleration = character.max_acceleration
        self.max_rotation = character.max_rotation

    def execute(self):
        steering = self.get_steering()
        self.character.apply_steering(steering, self.character.delta_time)
    
    def get_steering(self) -> SteeringOutput:
        steering = SteeringOutput()

        for behavior in self.behaviors:
            behavior_steering = behavior.behavior.get_steering()
            steering.linear += (behavior_steering.linear * behavior.weight)
            steering.angular += (behavior_steering.angular * behavior.weight)

        if steering.linear.length() > self.max_acceleration:
            steering.linear.scale_to_length(self.max_acceleration)

        steering.angular = max(min(steering.angular, self.max_rotation), -self.max_rotation)

        return steering
    
    def enter(self):
        print(f"[DEBUG] {self.character.ID} -> BlendedSteering")
        self.character.change_color("white")
    
    def exit(self): pass