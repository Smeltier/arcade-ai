import pygame

class SteeringOutput:
    def __init__(self):
        self.linear = pygame.math.Vector2(0, 0)
        self.angular = 0.0

# Virou uma derivação do SteeringOutput, talvez tenha uma forma melhor de lidar com isso..
class KinematicSteeringOutput(SteeringOutput):
    def __init__(self):
        self.velocity = pygame.math.Vector2(0, 0)
        self.rotation = 0.0