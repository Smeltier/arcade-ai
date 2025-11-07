import pygame

class FormationMachine ():
    def __init__(self, owner, start_formation=None):
        self.owner = owner
        self.current_formation = start_formation
        self.previous_formation = None

    def update(self):
        """ Recalcula os slots de owner a cada frame. """

        if self.current_formation:
            self.owner.update_slots()

    def change_formation(self, new_formation):
        """ Muda para um novo padrão de formação. """

        if not new_formation or new_formation == self.current_formation:
            return
        
        self.previous_formation = self.current_formation
        self.current_formation = new_formation

        self.owner.update_slots()

    def revert_to_previous_formation(self):
        """ Volta para o padrão anterior. """

        if self.previous_formation:
            self.change_formation(self.previous_formation)