import pygame

from states.seek import Seek
from outputs import SteeringOutput, Collision

class ObstacleAvoidance (Seek):
    def __init__(self, character, target):
        super().__init__(character, target)

        self.collision_detector = CollisionDetector()

    def execute(self):
        steering = self.get_steering()
        self.character.apply_steering(steering, self.character.delta_time)
    
    def get_steering(self):
        ray_vector = self.character.velocity
        ray_vector.normalize_ip()
        ray_vector *= self.character.collision_ray

        collision = self.collision_detector.get_collision(self.character.position, ray_vector)

        if not collision: return SteeringOutput()

        self.target = collision.position + collision.normal * self.character.avoid_distance

        return super().get_steering()
    
    def enter(self):
        return super().enter()
    
    def exit(self):
        return super().exit()