import pygame

from states.state import State
from outputs import SteeringOutput

class Separation (State):
    def __init__(self, character) -> None:
        super().__init__()

        self.character = character
        self.target_list = character.world.entities_list
        self.threshold = character.threshold
        self.decay_coefficient = character.decay_coefficient
        self.max_acceleration = character.max_acceleration

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