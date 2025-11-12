import pygame
import math
from ..outputs import SteeringOutput
from .state import State

class MaintainRadius(State):

    def __init__(self, character, leader, pattern, tolerance=5.0):
        self.character = character
        self.leader = leader
        self.pattern = pattern
        self.tolerance = tolerance
        self.max_acceleration = character.max_acceleration

    def execute(self):
        steering = self.get_steering()
        self.character.apply_steering(steering, self.character.delta_time)

    def get_steering(self) -> SteeringOutput:
        steering = SteeringOutput()

        manager = self.leader.formation_manager
        if not manager or not self.pattern:
            return steering

        total_slots = len(manager.slot_assignments)
        if total_slots == 0:
            return steering
            
        ideal_radius = self.pattern.calculate_ideal_radius(total_slots)

        vector_leader = self.leader.position - self.character.position
        distance_leader = vector_leader.length()

        if distance_leader == 0:
            return steering

        radial_direction = vector_leader.normalize()
        error = distance_leader - ideal_radius

        tangential_dir = pygame.Vector2(-radial_direction.y, radial_direction.x)
        
        steering.linear = tangential_dir * self.max_acceleration

        if abs(error) > self.tolerance:
            direction_sign = (error / abs(error))
            radial_force = radial_direction * (self.max_acceleration * direction_sign)
            steering.linear += radial_force
            steering.linear.scale_to_length(self.max_acceleration)

        steering.angular = 0
        return steering