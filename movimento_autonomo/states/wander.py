import pygame
import random
import math

from .face import Face
from .dummy_entity import DummyEntity
from ..outputs import SteeringOutput

class Wander (Face):
    def __init__(self, character, target) -> None:
        super().__init__(character, target)

        self.max_acceleration = character.max_acceleration
        self.wander_offset = character.wander_offset
        self.wander_radius = character.wander_radius
        self.wander_orientation = character.wander_orientation
        self.wander_rate = character.wander_rate

    def execute(self):
        steering = self.get_steering()
        self.character.apply_steering(steering, self.character.delta_time)
    
    def get_steering(self) -> SteeringOutput:
        self.wander_orientation += random.uniform(-1.0, 1.0) * self.wander_rate

        target_orientation = self.wander_orientation + self.character.orientation

        orientation_vector = pygame.math.Vector2(math.cos(self.character.orientation), math.sin(self.character.orientation))
        target_orientation_vector = pygame.math.Vector2(math.cos(target_orientation), math.sin(target_orientation))
        
        circle_center = self.character.position + self.wander_offset * orientation_vector

        target_position = circle_center + self.wander_radius * target_orientation_vector

        old_target = self.target

        wander_target = DummyEntity()
        wander_target.position = target_position

        self.target = wander_target
        steering = super().get_steering()
        self.target = old_target

        wander_force = orientation_vector * self.max_acceleration
        steering.linear += wander_force

        return steering
    
    def enter(self):
        print(f"[DEBUG] {self.character.ID} -> Wander")
        self.character.change_color("pink")
    
    def exit(self): pass