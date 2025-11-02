import pygame
from abc import abstractmethod

class Ghost ():
    def __init__(self, x, y, environment) -> None:
        self.position = pygame.Vector2((x, y))
        self.environment = environment
