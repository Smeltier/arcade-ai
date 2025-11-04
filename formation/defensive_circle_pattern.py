import math
import pygame

from .static import Static

class DefensiveCirclePattern ():
    def __init__(self, character_radius):
        self.character_radius = character_radius
        self.number_of_slots = 0

    def calculate_number_of_slots(self, assignments):
        return len(assignments)
    
    def get_drift_offset(self, assignments) -> Static:
        center = Static()
        
        if not assignments: return center

        for assignment in assignments:
            location: Static = self.get_slot_location(assignment.slot_number, len(assignments))

            center.position    += location.position
            center.orientation += location.orientation

        size = len(assignments)

        center.position    /= size
        center.orientation /= size

        return center
    
    def get_slot_location(self, slot_number, total_slots):
        angle_around_circle = slot_number / total_slots * 2 * math.pi
        radius = self.character_radius / math.sin(math.pi / total_slots)

        pos = pygame.Vector2(
            radius * math.cos(angle_around_circle),
            radius * math.sin(angle_around_circle)
        )

        orientation = angle_around_circle 

        return Static(pos, orientation)

    def supports_slots(self, slot_count):
        return True