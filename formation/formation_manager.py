import math
import pygame

from .static import Static
from .slot_assignment import SlotAssignment
from movimento_autonomo.states.arrive import Arrive

class FormationManager:
    def __init__(self, pattern):
        self.slot_assignments = []
        self.pattern = pattern
        
        self.world_anchor = Static()

    def update_slot_assignments(self):
        for i, slot in enumerate(self.slot_assignments):
            slot.slot_number = i

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

    def get_drift_offset(self) -> Static:
        return self.pattern.get_drift_offset(self.slot_assignments)

    def update_slots(self):
        if not self.slot_assignments: 
            return

        drift_offset = self.get_drift_offset()
        total_slots = len(self.slot_assignments)

        for assignment in self.slot_assignments:
            character = assignment.character
            slot_number = assignment.slot_number

            slot_location = self.pattern.get_slot_location(slot_number, total_slots)
            
            target_position = self.world_anchor.position + slot_location.position - drift_offset.position
            
            if not hasattr(character, 'formation_target'):
                character.formation_target = Static(target_position)
            else:
                character.formation_target.position = target_position

            if not isinstance(character.state_machine.current_state, Arrive):
                character.state_machine.change_state(Arrive(character, character.formation_target))
            else:
                character.state_machine.current_state.target = character.formation_target