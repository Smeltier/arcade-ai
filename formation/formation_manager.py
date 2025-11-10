import math
import pygame

from .static import Static
from .slot_assignment import SlotAssignment
from .formation_machine import FormationMachine
from movimento_autonomo.states.arrive import Arrive

class FormationManager:
    def __init__(self, owner_character, start_pattern=None):
        self.owner_character = owner_character
        self.slot_assignments = []
        self.world_anchor = owner_character.static
        self.formation_machine = FormationMachine(self, start_pattern)

    def update(self) -> None:
        self.formation_machine.update()

    def update_slot_assignments(self) -> None:
        for i, slot in enumerate(self.slot_assignments):
            slot.slot_number = i

    def add_character(self, character) -> bool:
        pattern = self.formation_machine.current_formation

        if not pattern:
            return False

        if not pattern.supports_slots(len(self.slot_assignments) + 1):
            return False
        
        slot = SlotAssignment(character)
        self.slot_assignments.append(slot)
        self.update_slot_assignments()

        return True

    def remove_character(self, character) -> None:
        self.slot_assignments = [s for s in self.slot_assignments if s.character is not character]
        self.update_slot_assignments()

    def get_drift_offset(self, pattern) -> Static:
        return pattern.get_drift_offset(self.slot_assignments)

    def update_slots(self) -> None:
        pattern = self.formation_machine.current_formation

        if not self.slot_assignments or not pattern: 
            return

        drift_offset = self.get_drift_offset(pattern)
        total_slots = len(self.slot_assignments)

        for assignment in self.slot_assignments:

            character = assignment.character
            slot_number = assignment.slot_number

            slot_location = pattern.get_slot_location(slot_number, total_slots)
            
            target_position = self.world_anchor.position + slot_location.position - drift_offset.position
            
            if not hasattr(character, 'formation_target'):
                character.formation_target = Static(target_position)
            else:
                character.formation_target.position = target_position

            if not isinstance(character.state_machine.current_state, Arrive):
                character.state_machine.change_state(Arrive(character, character.formation_target))
            else:
                character.state_machine.current_state.target = character.formation_target