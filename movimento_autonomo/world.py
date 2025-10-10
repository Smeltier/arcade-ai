import pygame

class World:
    def __init__(self, SCREEN):

        self.domain = SCREEN
        self.width = SCREEN.get_width()
        self.height = SCREEN.get_height()
        self.entities_list = []

    def add_entity(self, new_entity):
        if new_entity is None: 
            raise RuntimeError("Sua nova entidade não pode ser nula.")

        self.entities_list.append(new_entity)

    def remove_entity(self, remove_entity):
        if remove_entity is None: return

        for iterator, entity,  in enumerate(self.entities_list):
            if remove_entity is entity:
                self.entities_list.pop(iterator)

    def update(self, delta_time):
        for entity in self.entities_list:
            entity.update(delta_time)
            entity.draw(self.domain)