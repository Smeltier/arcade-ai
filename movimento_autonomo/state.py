import pygame
import math 
import random

from abc import ABC, abstractmethod

from outputs import SteeringOutput

class State(ABC):
    @abstractmethod 
    def execute(self): pass

    @abstractmethod
    def enter(self): pass
    
    @abstractmethod
    def exit(self): pass

    @abstractmethod
    def get_steering(self) -> SteeringOutput: pass