import pygame
import math
import random

from state import State
from outputs import SteeringOutput, Collision
from collision_detector import CollisionDetector

def map_to_range(rotation):
    return (rotation + math.pi) % (2 * math.pi) - math.pi

class DummyEntity:
    def __init__(self) -> None:
        self.position = pygame.math.Vector2(0, 0)

class Arrive(State):
    def __init__(self, character, target):
        super().__init__()

        self.character = character
        self.target = target
        self.max_speed = character.limits.max_speed
        self.max_acceleration = character.limits.max_acceleration
        self.slow_radius = character.behavior_threshold.slow_radius
        self.target_radius = character.behavior_threshold.target_radius
        self.time_to_target = character.behavior_threshold.time_to_target        

    def execute(self):
        steering = self.get_steering()
        self.character.apply_steering(steering, self.character.delta_time)

    def get_steering(self) -> SteeringOutput:
        steering = SteeringOutput()

        if not self.target:
            return steering
            
        self.direction = self.target.position - self.character.position
        self.distance = self.direction.length()

        if self.distance < self.target_radius:
            return SteeringOutput()
        
        if self.distance > self.slow_radius:
            target_speed = self.max_speed
        else:
            target_speed = self.max_speed * self.distance / self.slow_radius

        target_velocity = self.direction.normalize()
        target_velocity *= target_speed

        steering.linear = target_velocity - self.character.velocity
        steering.linear /= self.time_to_target

        if steering.linear.length() > self.max_acceleration:
            steering.linear.scale_to_length(self.max_acceleration)

        steering.angular = 0
        return steering
    
    def enter(self):
        print(f"[DEBUG] {self.character.ID} -> Arrive")
        self.character.change_color("blue")
    
    def exit(self): pass


class Seek(State):
    def __init__(self, character, target):
        super().__init__()

        self.character = character
        self.target = target
        self.max_acceleration = character.limits.max_acceleration

    def execute(self):
        steering = self.get_steering()
        self.character.apply_steering(steering, self.character.delta_time)

    def get_steering(self):
        steering = SteeringOutput()

        if not self.target:
            return steering

        steering.linear = (self.target.position - self.character.position).normalize()
        steering.linear *= self.max_acceleration

        steering.angular = 0
        return steering  

    def enter(self):
        print(f"[DEBUG] {self.character.ID} -> Seek")
        self.character.change_color("green")
    
    def exit(self): pass


class Flee(State):
    def __init__(self, character, target):
        super().__init__()

        self.character = character
        self.target = target
        self.max_acceleration = character.limits.max_acceleration

    def execute(self):
        steering = self.get_steering()
        self.character.apply_steering(steering, self.character.delta_time)

    def get_steering(self):
        steering = SteeringOutput()

        if not self.target:
            return steering

        steering.linear = (self.character.position - self.target.position).normalize()
        steering.linear *= self.max_acceleration

        steering.angular = 0
        return steering 

    def enter(self):
        print(f"[DEBUG] {self.character.ID} -> Flee")
        self.character.change_color("yellow")
    
    def exit(self): pass


class Pursue(Seek):
    def __init__(self, character, target):
        super().__init__(character, target)

        self.max_prediction = self.character.limits.max_prediction

    def execute(self):
        steering = self.get_steering()
        self.character.apply_steering(steering, self.character.delta_time)

    def get_steering(self):
        steering = SteeringOutput()

        if not self.target:
            return steering

        direction = self.target.position - self.character.position
        distance = direction.length()
        speed = self.character.velocity.length()

        if speed <= distance / self.max_prediction:
            prediction = self.max_prediction

        else:
            prediction = distance / speed

        predicted_position = self.target.position + self.target.velocity * prediction

        steering.linear = (predicted_position - self.character.position).normalize()
        steering.linear *= self.max_acceleration

        steering.angular = 0
        return steering

    def enter(self):
        print(f"[DEBUG] {self.character.ID} -> Pursue")
        self.character.change_color("orange")
    
    def exit(self): pass


class Evade(Flee):
    def __init__(self, character, target):
        super().__init__(character, target)

        self.max_prediction = self.character.limits.max_prediction

    def execute(self):
        steering = self.get_steering()
        self.character.apply_steering(steering, self.character.delta_time)

    def get_steering(self):
        steering = SteeringOutput()
        if not self.target:
            return steering

        direction = self.target.position - self.character.position
        self.distance = direction.length()
        speed = self.character.velocity.length()

        if speed <= self.distance / self.max_prediction:
            prediction = self.max_prediction

        else:
            prediction = self.distance / speed

        predicted_position = self.target.position + self.target.velocity * prediction

        steering.linear = (self.character.position - predicted_position).normalize()
        steering.linear *= self.max_acceleration

        steering.angular = 0
        return steering

    def enter(self):
        print(f"[DEBUG] {self.character.ID} -> Evade")
        self.character.change_color("purple")
    
    def exit(self): pass


class Align(State):
    def __init__(self, character, target) -> None:
        super().__init__()

        self.character = character
        self.target = target
        self.max_rotation = character.limits.max_rotation
        self.target_radius = character.behavior_threshold.target_radius
        self.rotation = character.rotation
        self.slow_radius = character.behavior_threshold.slow_radius
        self.time_to_target = character.behavior_threshold.time_to_target
        self.max_angular_acceleration = character.limits.max_angular_acceleration

    def execute(self):
        return super().execute()
    
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


class Wander(Face):
    def __init__(self, character, target) -> None:
        super().__init__(character, target)

        self.max_acceleration = character.limits.max_acceleration
        self.wander_offset = character.wander_threshold.wander_offset
        self.wander_radius = character.wander_threshold.wander_radius
        self.wander_orientation = character.wander_threshold.wander_orientation
        self.wander_rate = character.wander_threshold.wander_rate

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
    
    def exit(self):
        return super().exit()


# TODO
class LookWhereYoureGoing(Align):
    def __init__(self, character, target) -> None:
        super().__init__(character, target)

    def execute(self):
        return super().execute()
    
    def get_steering(self) -> SteeringOutput:
        return super().get_steering()

    def enter(self):
        return super().enter()
    
    def exit(self): 
        return super().exit()


class VelocityMatch(State):
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
    
    def exit(self):
        return super().exit()
    

class Separation(State):
    def __init__(self, character) -> None:
        super().__init__()

        self.character = character
        self.target_list = character.world.entities_list
        self.threshold = character.behavior_threshold.threshold
        self.decay_coefficient = character.behavior_threshold.decay_coefficient
        self.max_acceleration = character.limits.max_acceleration

    def execute(self):
        steering = self.get_steering()
        self.character.apply_steering(steering, self.character.delta_time)
    
    def get_steering(self) -> SteeringOutput:
        steering = SteeringOutput()

        for target in self.target_list:

            if target == self.character:
                continue
            
            direction = self.character.position - target.position
            distance = direction.length() - 16

            if distance == 0 or distance >= self.threshold:
                continue

            strength = min(self.decay_coefficient * (distance * distance), self.max_acceleration)

            entity_size = pygame.math.Vector2(0, 8)

            direction.normalize_ip()
            
            steering.linear += strength * direction + entity_size

        if steering.linear.length() > self.max_acceleration:
            steering.linear.scale_to_length(self.max_acceleration)

        if steering.linear.length_squared() == 0:
            self.character.velocity = pygame.math.Vector2(0, 0)

        return steering
    
    def enter(self):
        print(f"[DEBUG] {self.character.ID} -> Separation")
        self.character.change_color("brown")
    
    def exit(self): pass


class Attraction(State):
    def __init__(self, character) -> None:
        super().__init__()

        self.character = character
        self.target_list = character.world.entities_list
        self.threshold = character.behavior_threshold.threshold
        self.decay_coefficient = character.behavior_threshold.decay_coefficient
        self.max_acceleration = character.limits.max_acceleration

    def execute(self):
        steering = self.get_steering()
        self.character.apply_steering(steering, self.character.delta_time)
    
    def get_steering(self) -> SteeringOutput:
        steering = SteeringOutput()

        for target in self.target_list:

            if target == self.character:
                continue
            
            direction = target.position - self.character.position
            distance = direction.length() - 16

            if distance == 0 or distance >= self.threshold:
                continue

            strength = min(self.decay_coefficient * (distance * distance), self.max_acceleration)

            entity_size = pygame.math.Vector2(0, 8)

            direction.normalize_ip()
            
            steering.linear += strength * direction + entity_size

        if steering.linear.length() > self.max_acceleration:
            steering.linear.scale_to_length(self.max_acceleration)

        if steering.linear.length_squared() == 0:
            self.character.velocity = pygame.math.Vector2(0, 0)

        return steering
    
    def enter(self):
        print(f"[DEBUG] {self.character.ID} -> Attraction")
        self.character.change_color("brown")
    
    def exit(self): pass

class CollisionAvoidance(State):
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

        for target in self.character.target_list:

            relative_position = target.position - self.character.position
            relative_velocity = target.velocity - self.character.velocity

            relative_speed = relative_velocity.length()
            distance = relative_position.length()

            if relative_speed == 0 or relative_position.length() == 0: continue

            time_to_collision = (relative_position.dot(relative_velocity)) / (relative_speed ** 2)

            min_separation: float = distance - relative_speed * shortest_time

            if min_separation > 2 * self.character.radius: continue

            if 0 < time_to_collision < shortest_time:

                shortest_time = time_to_collision
                first_target = target
                first_min_separation = min_separation
                first_distance = distance
                first_relative_position = relative_position
                first_relative_velocity = relative_velocity

        if not first_target:
            return SteeringOutput()
        
        if first_min_separation <= 0 or first_distance < 2 * self.character.radius:
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
    
    def exit(self):
        return super().exit()
    
class ObstacleAvoidance(Seek):
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