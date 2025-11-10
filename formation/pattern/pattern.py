import pygame

from abc import abstractmethod

from ..static import Static

class Pattern ():

    @abstractmethod
    def calculate_number_of_slots(self, assignments) -> int:
        """ Calcula o número de slots ocupados da formação. """
        pass

    @abstractmethod
    def get_slot_location(self, slot_number, total_slots) -> Static:
        """ Calcula a localização de um slot específico da formação. """
        pass

    @abstractmethod
    def supports_slots(self, slot_count) -> bool:
        """ Verifica se o padrão suporta uma quantidade específica de slots. """
        pass