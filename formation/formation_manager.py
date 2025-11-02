import math
import pygame

from .static import Static
from .slot_assignment import SlotAssignment

class FormationManager:
    def __init__(self, pattern):
        self.slot_assignments = []
        self.pattern = pattern
        self.drift_offset = Static()

    def update_slot_assignments(self):
        for i, slot in enumerate(self.slot_assignments):
            slot.slot_number = i
        self.drift_offset = self.pattern.get_drift_offset(self.slot_assignments)

    def add_character(self, character):
        if not self.pattern.supports_slots(len(self.slot_assignments) + 1):
            return False
        
        slot = SlotAssignment(character)
        self.slot_assignments.append(slot)
        self.update_slot_assignments()

        return True

    def remove_character(self, character):
        self.slot_assignments = [s for s in self.slot_assignments if s.character is not character]
        self.update_slot_assignments()

    def get_anchor_point(self):
        return self.pattern.get_drift_offset(self.slot_assignments)

    # TODO
    def update_slots(self):
        pass