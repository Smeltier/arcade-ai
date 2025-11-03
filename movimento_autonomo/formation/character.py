import pygame

from .static import Static

class Character ():
    def __init__ (self, name, position = (0, 0)):
        self.name = name
        self.position = pygame.math.Vector2(position)
        self.orientation = 0.0
        self.target: Static | None = None

    def set_target (self, static):
        self.target = static