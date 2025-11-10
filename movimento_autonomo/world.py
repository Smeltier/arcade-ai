import pygame

class World:

    def __init__(self, SCREEN):
        self.domain = SCREEN
        self.width = SCREEN.get_width()
        self.height = SCREEN.get_height()
        self.entities_list = []

    def add_entity(self, new_entity) -> None:
        """ Adiciona uma nova entidade ao mundo. Lança uma Exceção caso a entidade seja do tipo None. """

        if new_entity is None: 
            raise RuntimeError("Sua nova entidade não pode ser nula.")

        self.entities_list.append(new_entity)

    def remove_entity(self, entity) -> None:
        """ Remove uma entidade do mundo. """

        if entity is None: return

        for iterator, entity,  in enumerate(self.entities_list):
            if entity is entity:
                self.entities_list.pop(iterator)

    def update(self, delta_time: float) -> None:
        """ Atualiza o mundo baseado em uma variação de tempo. """

        for entity in self.entities_list:
            entity.update(delta_time)
            entity.draw(self.domain)