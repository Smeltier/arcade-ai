import pygame
import math 
import random

from abc import ABC, abstractmethod

def map_to_range(rotation):
    return (rotation + math.pi) % (2 * math.pi) - math.pi

class DummyEntity:
    def __init__(self) -> None:
        self.position = pygame.math.Vector2(0, 0)

class SteeringOutput:
    def __init__(self):
        self.linear = pygame.math.Vector2(0, 0)
        self.angular = 0.0

# Virou uma derivação do SteeringOutput, talvez tenha uma forma melhor de lidar com isso..
class KinematicSteeringOutput(SteeringOutput):
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

        if self.character.distance > 50:
            self.character.state_machine.change_state(Pursue(self.character, self.target))

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