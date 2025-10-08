import pygame
import math 
import random

from abc import ABC, abstractmethod

from steering_output import SteeringOutput

def map_to_range(rotation):
    return (rotation + math.pi) % (2 * math.pi) - math.pi


class State(ABC):
    @abstractmethod 
    def execute(self): pass

    @abstractmethod
    def enter(self): pass
    
    @abstractmethod
    def exit(self): pass

    @abstractmethod
    def get_steering(self) -> SteeringOutput: pass