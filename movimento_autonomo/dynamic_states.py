import pygame
import math
import random

from state import State
from steering_output import SteeringOutput

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

    def execute(self):
        steering = self.get_steering()
        self.character.apply_steering(steering, self.character.delta_time)

        if self.character.distance > 50:
            self.character.state_machine.change_state(Pursue(self.character, self.target))

    def get_steering(self) -> SteeringOutput:
        steering = SteeringOutput()

        if not self.target:
            return steering
            
        direction = self.target.position - self.character.position
        distance = direction.length()

        if distance < self.character.target_radius:
            return SteeringOutput()
        
        if distance > self.character.slow_radius:
            target_speed = self.character.max_speed

        else:
            target_speed = self.character.max_speed * distance / self.character.slow_radius

        target_velocity = direction
        target_velocity.normalize_ip()
        target_velocity *= target_speed

        steering.linear = target_velocity - self.character.velocity
        steering.linear /= self.character.time_to_target

        if steering.linear.length() > self.character.max_acceleration:
            steering.linear.scale_to_length(self.character.max_acceleration)

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

    def execute(self):
        steering = self.get_steering()
        self.character.apply_steering(steering, self.character.delta_time)

        if self.character.distance <= 200:
            self.character.state_machine.change_state(Pursue(self.character, self.target))

    def get_steering(self):
        steering = SteeringOutput()

        if not self.target:
            return steering

        steering.linear = self.target.position - self.character.position
        steering.linear.normalize_ip()
        steering.linear *= self.character.max_acceleration

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

    def execute(self):
        steering = self.get_steering()
        self.character.apply_steering(steering, self.character.delta_time)

        if self.character.distance <= 200:
            self.character.state_machine.change_state(Evade(self.character, self.target)) 

    def get_steering(self):
        steering = SteeringOutput()

        if not self.target:
            return steering

        steering.linear = self.character.position - self.target.position
        steering.linear.normalize_ip()
        steering.linear *= self.character.max_acceleration

        steering.angular = 0
        return steering 

    def enter(self):
        print(f"[DEBUG] {self.character.ID} -> Flee")
        self.character.change_color("yellow")
    
    def exit(self): pass


class Pursue(Seek):
    def __init__(self, character, target):
        super().__init__(character, target)

    def execute(self):
        steering = self.get_steering()
        self.character.apply_steering(steering, self.character.delta_time)

        if self.character.distance > 200:
            self.character.state_machine.change_state(Seek(self.character, self.target))

        elif self.character.distance <= 50:
            self.character.state_machine.change_state(Arrive(self.character, self.target))

    # G: Repetição de código, talvez tenha uma forma melhor de fazer isso.
    def get_steering(self):
        steering = SteeringOutput()
        if not self.target:
            return steering

        direction = self.target.position - self.character.position
        distance = direction.length()
        speed = self.character.velocity.length()

        if speed <= distance / self.character.max_prediction:
            prediction = self.character.max_prediction

        else:
            prediction = distance / speed

        predicted_position = self.target.position + self.target.velocity * prediction

        steering.linear = predicted_position - self.character.position
        steering.linear.normalize_ip()
        steering.linear *= self.character.max_acceleration

        steering.angular = 0
        return steering

    def enter(self):
        print(f"[DEBUG] {self.character.ID} -> Pursue")
        self.character.change_color("orange")
    
    def exit(self): pass


class Evade(Flee):
    def __init__(self, character, target):
        super().__init__(character, target)

    def execute(self):
        steering = self.get_steering()
        self.character.apply_steering(steering, self.character.delta_time)

        if self.character.distance > 200:
            self.character.state_machine.change_state(Flee(self.character, self.target)) 

    def get_steering(self):
        steering = SteeringOutput()
        if not self.target:
            return steering

        direction = self.target.position - self.character.position
        distance = direction.length()
        speed = self.character.velocity.length()

        if speed <= distance / self.character.max_prediction:
            prediction = self.character.max_prediction

        else:
            prediction = distance / speed

        predicted_position = self.target.position + self.target.velocity * prediction

        steering.linear = predicted_position - self.character.position
        steering.linear.normalize_ip()
        steering.linear *= self.character.max_acceleration

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

    def execute(self):
        return super().execute()
    
    def get_steering(self) -> SteeringOutput:
        steering = SteeringOutput()

        rotation = self.target.orientation - self.character.orientation
        rotation = map_to_range(rotation)
        rotation_size = abs(rotation)

        if rotation_size < self.character.target_radius:
            return SteeringOutput()
        
        if rotation_size > self.character.slow_radius:
            target_rotation = self.character.max_rotation

        else:
            target_rotation = self.character.max_rotation * rotation_size / self.character.slow_radius

        target_rotation *= rotation / rotation_size

        steering.angular = target_rotation - self.character.rotation
        steering.angular /= self.character.time_to_target

        angular_acceleration = abs(steering.angular)

        if angular_acceleration > self.character.max_angular_acceleration:
            steering.angular /= angular_acceleration
            steering.angular *= self.character.max_angular_acceleration

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

        self.character = character
        self.target = target

    def execute(self):
        steering = self.get_steering()
        self.character.apply_steering(steering, self.character.delta_time)
    
    def get_steering(self) -> SteeringOutput:
        self.character.wander_orientation += random.uniform(-1.0, 1.0) * self.character.wander_rate

        target_orientation = self.character.wander_orientation + self.character.orientation

        orientation_vector = pygame.math.Vector2(math.cos(self.character.orientation), math.sin(self.character.orientation))
        target_orientation_vector = pygame.math.Vector2(math.cos(target_orientation), math.sin(target_orientation))
        
        circle_center = self.character.position + self.character.wander_offset * orientation_vector

        target_position = circle_center + self.character.wander_radius * target_orientation_vector

        old_target = self.target

        wander_target = DummyEntity()
        wander_target.position = target_position

        self.target = wander_target
        steering = super().get_steering()
        self.target = old_target

        steering.linear = self.character.max_acceleration * orientation_vector

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

    def execute(self):
        steering = self.get_steering()
        self.character.apply_steering(steering, self.character.delta_time)
    
    def get_steering(self) -> SteeringOutput:
        steering = SteeringOutput()

        for target in self.character.target_list:

            if target == self.character:
                continue
            
            direction = self.character.position - target.position
            distance = direction.length() - 16

            if distance == 0 or distance >= self.character.threshold:
                continue

            strength = min(self.character.decay_coefficient * (distance * distance), self.character.max_acceleration)

            entity_size = pygame.math.Vector2(0, 8)

            direction.normalize()
            
            steering.linear += strength * direction + entity_size

        if steering.linear.length() > self.character.max_acceleration:
            steering.linear.scale_to_length(self.character.max_acceleration)

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

    def execute(self):
        steering = self.get_steering()
        self.character.apply_steering(steering, self.character.delta_time)
    
    def get_steering(self) -> SteeringOutput:
        steering = SteeringOutput()

        for target in self.character.target_list:

            if target == self.character:
                continue
            
            direction = target.position - self.character.position
            distance = direction.length() - 16

            if distance == 0 or distance >= self.character.threshold:
                continue

            strength = min(self.character.decay_coefficient * (distance * distance), self.character.max_acceleration)

            entity_size = pygame.math.Vector2(0, 8)

            direction.normalize()
            
            steering.linear += strength * direction + entity_size

        if steering.linear.length() > self.character.max_acceleration:
            steering.linear.scale_to_length(self.character.max_acceleration)

        if steering.linear.length_squared() == 0:
            self.character.velocity = pygame.math.Vector2(0, 0)

        return steering
    
    def enter(self):
        print(f"[DEBUG] {self.character.ID} -> Attraction")
        self.character.change_color("brown")
    
    def exit(self): pass