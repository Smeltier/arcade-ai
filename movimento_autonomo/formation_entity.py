import pygame

from .moving_entity import MovingEntity
from ..formation.formation_manager import FormationManager

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
