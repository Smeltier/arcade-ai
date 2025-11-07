import math
import pygame

from .state import State
from ..collision_detector import CollisionDetector
from ..outputs import SteeringOutput

class CollisionAvoidance (State):
    def __init__(self, character) -> None:
        super().__init__()

        self.character = character

    def execute(self):
        steering = self.get_steering()
        self.character.apply_steering(steering, self.character.delta_time)
    
    def get_steering(self) -> SteeringOutput:
        steering = SteeringOutput()

        first_target = None
        first_min_separation = None
        first_distance = None
        first_relative_position = None
        first_relative_velocity = None

        shortest_time = math.inf

        for target in self.character.world.entities_list:

            relative_position = target.position - self.character.position
            relative_velocity = target.velocity - self.character.velocity

            relative_speed = relative_velocity.length()
            distance = relative_position.length()

            if relative_speed == 0 or relative_position.length() == 0: continue

            time_to_collision = (relative_position.dot(relative_velocity)) / (relative_speed ** 2)

            min_separation: float = distance - relative_speed * shortest_time

            if min_separation > 2 * self.character.effect_radius: continue

            if 0 < time_to_collision < shortest_time:

                shortest_time = time_to_collision
                first_target = target
                first_min_separation = min_separation
                first_distance = distance
                first_relative_position = relative_position
                first_relative_velocity = relative_velocity

        if not first_target:
            return SteeringOutput()
        
        if first_min_separation <= 0 or first_distance < 2 * self.character.effect_radius:
            relative_position = first_target.position - self.character.position
        else:
            relative_position = first_relative_position + first_relative_velocity * shortest_time

        relative_position.normalize_ip()
        steering.linear = relative_position * self.character.max_acceleration

        steering.angular = 0
        return steering
    
    def enter(self):
        print(f"[DEBUG] {self.character.ID} -> CollisionAvoidance")
        self.character.change_color("gray")
    
    def exit(self): pass