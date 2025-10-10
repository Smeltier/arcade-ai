import pygame
import math
import random

from state import State
from movimento_autonomo.outputs import KinematicSteeringOutput

def map_to_range(rotation):
    return (rotation + math.pi) % (2 * math.pi) - math.pi

class DummyEntity:
    def __init__(self) -> None:
        self.position = pygame.math.Vector2(0, 0)

class KinematicWander(State):
    def __init__(self, character):
        super().__init__()

        self.character = character

    def execute(self):
        steering = self.get_steering()
        self.character.apply_kinematic_steering(steering, self.character.delta_time)
    
    def get_steering(self) -> KinematicSteeringOutput:
        steering = KinematicSteeringOutput()

        steering.velocity = pygame.math.Vector2(math.sin(self.character.orientation),
                                                -math.cos(self.character.orientation))

        steering.velocity *= self.character.max_speed

        random_rotation = random.uniform(-1.0, 1.0)

        steering.rotation = random_rotation * self.character.max_rotation

        return steering
    
    def enter(self):
        print(f"[DEBUG] {self.character.ID} -> KinematicWander")
        self.character.change_color("white")
    
    def exit(self): pass

class KinematicSeek(State):
    def __init__(self, character, target):
        super().__init__()

        self.character = character
        self.target = target

    def execute(self):
        steering = self.get_steering()
        self.character.apply_kinematic_steering(steering, self.character.delta_time)

        # if self.character.distance <= 200:
        #     self.character.state_machine.change_state(Evade(self.character, self.target)) 

    def get_steering(self) -> KinematicSteeringOutput:
        steering = KinematicSteeringOutput()

        if not self.target:
            return steering

        steering.velocity = self.target.position - self.character.position
        steering.velocity.normalize_ip()
        steering *= self.character.max_speed

        self.character.orientation = self.character.new_orientation(steering)

        steering.rotation = 0.0
        return steering 

    def enter(self):
        print(f"[DEBUG] {self.character.ID} -> KinematicSeek")
        self.character.change_color("green")
    
    def exit(self): pass

class KinematicFlee(State):
    def __init__(self, character, target):
        super().__init__()

        self.character = character
        self.target = target

    def execute(self):
        steering = self.get_steering()
        self.character.apply_kinematic_steering(steering, self.character.delta_time)

        # if self.character.distance <= 200:
        #     self.character.state_machine.change_state(Evade(self.character, self.target)) 

    def get_steering(self) -> KinematicSteeringOutput:
        steering = KinematicSteeringOutput()

        if not self.target:
            return steering

        steering.velocity = self.character.position - self.target.position
        steering.velocity.normalize_ip()
        steering *= self.character.max_speed

        self.character.orientation = self.character.new_orientation(steering)

        steering.rotation = 0.0
        return steering 

    def enter(self):
        print(f"[DEBUG] {self.character.ID} -> KinematicFlee")
        self.character.change_color("yellow")
    
    def exit(self): pass

class KinematicArrive(State):
    def __init__(self, character, target):
        super().__init__()

        self.character = character
        self.target = target

    def execute(self):
        steering = self.get_steering()
        self.character.apply_kinematic_steering(steering, self.character.delta_time)

        # if self.character.distance > 50:
        #     self.character.state_machine.change_state(Pursue(self.character, self.target))

    def get_steering(self) -> KinematicSteeringOutput:
        steering = KinematicSteeringOutput()

        steering.velocity = self.target.position - self.character.position

        if steering.velocity.length() < self.character.slow_radius:
            return KinematicSteeringOutput()
        
        steering.velocity /= self.character.time_to_target

        if steering.velocity.length() > self.character.max_speed:
            steering.velocity.scale_to_length(self.character.max_acceleration)

        self.character.orientation = self.character.new_orientation(steering)

        steering.rotation = 0
        return steering
    
    def enter(self):
        print(f"[DEBUG] {self.character.ID} -> KinematicArrive")
        self.character.change_color("blue")
    
    def exit(self): pass