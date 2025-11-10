import math
import pygame

from .pattern import Pattern
from ..static import Static

class DefensiveCirclePattern (Pattern):

    def __init__(self, character_radius):
        self.character_radius = character_radius
        self.number_of_slots = 0

    def calculate_number_of_slots(self, assignments) -> int:
        """ Calcula o número de slots ocupados da formação. """
        return len(assignments)
    
    def get_slot_location(self, slot_number, total_slots) -> Static:
        """ Calcula a localização de um slot específico da formação. """

        if total_slots <= 0:
            return Static(pygame.Vector2(0,0), 0)
        
        if total_slots == 1:
            distance = self.character_radius * 2

            position = pygame.Vector2(-distance, 0)
            orientation = 0

            return Static(position, orientation)
        
        angle_around_circle = (slot_number / total_slots) * 2 * math.pi

        try:
            radius = self.character_radius / math.sin(math.pi / total_slots)
        except ZeroDivisionError:
            radius = self.character_radius * 2
        
        position = pygame.Vector2 (
            radius * math.cos(angle_around_circle),
            radius * math.sin(angle_around_circle)
        )
        orientation = angle_around_circle

        return Static(position, orientation)

    def supports_slots(self, slot_count):
        """ Verifica se o padrão suporta uma quantidade específica de slots. """
        return True