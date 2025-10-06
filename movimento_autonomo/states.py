import pygame
import math
import random

from abc import ABC, abstractmethod

class SteeringOutput:
    def __init__(self):
        self.linear = pygame.math.Vector2(0, 0)
        self.angular = 0.0

class KinematicSteeringOutput:
    def __init__(self):
        self.velocity = pygame.math.Vector2(0, 0)
        self.rotation = 0.0

class State(ABC):
    @abstractmethod 
    def execute(self): pass

    @abstractmethod
    def enter(self): pass
    
    @abstractmethod
    def exit(self): pass

    @abstractmethod
    def get_steering(self) -> SteeringOutput: pass


class Arrive(State):
    def __init__(self, character: object, target: object):
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

        if distance < self.character.detection_radius:
            return SteeringOutput()
        
        if distance > self.character.slow_radius: 
            target_speed = self.character.max_speed
        else: 
            target_speed = self.character.max_speed * distance / self.character.slow_radius

        target_velocity = direction.normalize() * target_speed
        
        steering.linear = (target_velocity - self.character.velocity) / self.character.time_to_target

        if steering.linear.length() > self.character.max_acceleration:
            steering.linear.scale_to_length(self.character.max_acceleration)

        return steering
    
    def enter(self):
        print(f"[DEBUG] {self.character.ID} -> Arrive")
        self.character.change_color("blue")
    
    def exit(self): pass


class Seek(State):
    def __init__(self, character: object, target: object):
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

        return steering  

    def enter(self):
        print(f"[DEBUG] {self.character.ID} -> Seek")
        self.character.change_color("green")
    
    def exit(self): pass


class Flee(State):
    def __init__(self, character: object, target: object):
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

    def get_steering(self):
        steering = SteeringOutput()
        if not self.target:
            return steering
            
        direction = self.target.position - self.character.position
        distance = direction.length()
        speed = self.character.velocity.length()

        prediction = min(self.character.max_prediction, distance / speed) if speed > 0 else self.character.max_prediction
        predicted_position = self.target.position + self.target.velocity * prediction

        steering.linear = predicted_position - self.character.position
        steering.linear.normalize_ip()
        steering.linear *= self.character.max_acceleration
        
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

        direction = self.character.position - self.target.position 
        distance = direction.length()
        speed = self.character.velocity.length()

        prediction = min(self.character.max_prediction, distance / speed) if speed > 0 else self.character.max_prediction
        predicted_position = self.target.position + self.target.velocity * prediction

        steering.linear = self.character.position - predicted_position
        steering.linear.normalize_ip()
        steering.linear *= self.character.max_acceleration

        return steering

    def enter(self):
        print(f"[DEBUG] {self.character.ID} -> Evade")
        self.character.change_color("purple")
    
    def exit(self): pass

class KinematicWander(State):
    def __init__(self, character: object):
        super().__init__()

        self.character = character

    def execute(self):
        steering = self.get_steering()
        self.character.apply_kinematic_steering(steering, self.character.delta_time)
    
    def get_steering(self):
        steering = KinematicSteeringOutput()

        steering.velocity = pygame.math.Vector2(math.sin(self.character.orientation),
                                                -math.cos(self.character.orientation))

        steering.velocity *= self.character.max_speed

        random_rotation = random.uniform(-1.0, 1.0)

        steering.rotation = random_rotation * self.character.max_rotation

        return steering
    
    def enter(self):
        print(f"[DEBUG] {self.character.ID} -> Wander")
        self.character.change_color("white")
    
    def exit(self): pass