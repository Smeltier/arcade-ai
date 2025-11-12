import pygame

from movimento_autonomo.outputs import BehaviorAndWeight
from movimento_autonomo.moving_entity import MovingEntity
from movimento_autonomo.states.blended_steering import BlendedSteering
from movimento_autonomo.states.separation import Separation
from movimento_autonomo.states.seek import Seek
from movimento_autonomo.states.maintain_radius import MaintainRadius
from .formation_manager import FormationManager

class FormationEntity (MovingEntity):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.leader = None
        self.slot_number = -1
        self.formation_manager = None

    def become_leader(self, start_pattern):
        if not self.formation_manager:
            self.formation_manager = FormationManager(self, start_pattern)

    def add_follower(self, entity):
        if not self.formation_manager:
            return
        
        if not isinstance(entity, FormationEntity):
            return
        
        self.formation_manager.add_character(entity)

    def set_formation_leader(self, leader_character, slot_number):
        self.leader = leader_character
        self.slot_number = slot_number

        pattern = self.leader.formation_manager.formation_machine.current_formation

        seek = Seek(self, self.leader)
        separation = Separation(self)
        perimeter = MaintainRadius(self, leader_character, pattern, 20)

        behaviors_list = [
            BehaviorAndWeight(separation, 5.0),
            BehaviorAndWeight(perimeter, 2.0),
            # BehaviorAndWeight(seek, 30),
        ]

        self.state_machine.change_state(BlendedSteering(self, behaviors_list))


    def clear_formation_leader(self):
        self.leader = None
        self.slot_number = -1