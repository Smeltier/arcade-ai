import pygame

class Static ():
    def __init__(self, position = (0, 0), orientation = 0.0):
        self.position = pygame.math.Vector2(position)
        self.orientation = orientation # RAD