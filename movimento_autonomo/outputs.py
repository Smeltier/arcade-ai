import pygame

class SteeringOutput:
    def __init__(self):
        self.linear = pygame.math.Vector2(0, 0)
        self.angular = 0.0

class KinematicSteeringOutput(SteeringOutput):
    def __init__(self):
        self.velocity = pygame.math.Vector2(0, 0)
        self.rotation = 0.0

class Collision:
    def __init__(self):
        self.position = pygame.math.Vector2
        self.normal = pygame.math.Vector2

class BehaviorAndWeight:
    def __init__(self, behavior, weight=1.0) -> None:
        self.behavior = behavior
        self.weight: float = weight