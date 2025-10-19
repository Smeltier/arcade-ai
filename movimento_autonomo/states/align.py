import math
import pygame

from states.state import State
from outputs import SteeringOutput

class Align(State):
    def __init__(self, character, target) -> None:
        super().__init__()

        self.character = character
        self.target = target
        self.max_rotation = character.max_rotation
        self.target_radius = character.target_radius
        self.rotation = character.rotation
        self.slow_radius = character.slow_radius
        self.time_to_target = character.time_to_target
        self.max_angular_acceleration = character.max_angular_acceleration

    def execute(self): pass
    
    def get_steering(self) -> SteeringOutput:
        steering = SteeringOutput()

        rotation = self.target.orientation - self.character.orientation
        rotation = map_to_range(rotation)
        rotation_size = abs(rotation)

        if rotation_size < self.target_radius:
            return SteeringOutput()
        
        if rotation_size > self.slow_radius:
            target_rotation = self.max_rotation

        else:
            target_rotation = self.max_rotation * rotation_size / self.slow_radius

        target_rotation *= rotation / rotation_size

        steering.angular = target_rotation - self.rotation
        steering.angular /= self.time_to_target

        angular_acceleration = abs(steering.angular)

        if angular_acceleration > self.max_angular_acceleration:
            steering.angular /= angular_acceleration
            steering.angular *= self.max_angular_acceleration

        steering.linear = pygame.math.Vector2(0,0)
        return steering
    
    def enter(self):
        print(f"[DEBUG] {self.character.ID} -> Align")
        self.character.change_color("white")
    
    def exit(self):
        return super().exit()

def map_to_range(rotation):
    return (rotation + math.pi) % (2 * math.pi) - math.pi