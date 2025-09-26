import pygame
import math

def arredondar_angulo(vetor: pygame.math.Vector2):
    """
        Retorna o ângulo de um vetor representado como multiplo do ângulo pi/2 (45 graus)
    """
    ORIGEM = pygame.math.Vector2(0, 0)
    
    angulo_graus = vetor.angle_to(ORIGEM)
    angulo_normalizado = angulo_graus % 360
    angulo_arredondado = round(angulo_normalizado / 45) * 45

    return angulo_arredondado


def conversor_vetor(vetor: pygame.math.Vector2):
    magnitude = vetor.length()

    angulo = arredondar_angulo(vetor)
    angulo_radianos = math.radians(angulo)

    novo_x = magnitude * math.cos(angulo_radianos) # x' = |v| * cos(θ)
    novo_y = magnitude * math.sin(angulo_radianos) # y' = |v| * sen(θ)

    novo_vetor = pygame.math.Vector2((novo_x, novo_y)) # V' = (x', y')

    return novo_vetor
