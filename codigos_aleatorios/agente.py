import pygame
    
class Agent:
    def __init__(self, x = 0, y = 0, cor = "black", largura = 0, altura = 0, delta_x = 0, delta_y = 0):
        self.position = pygame.Vector2((x, y))
        self.largura = largura
        self.altura = altura
        self.raio = altura
        self.delta_x = delta_x
        self.delta_y = delta_y
        self.cor = cor

    def __str__(self) -> str:
        return f'Agent => ({self.position.x}, {self.position.y})'