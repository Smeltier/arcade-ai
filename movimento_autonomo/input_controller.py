import pygame

from moving_entity import MovingEntity
from dynamic_states import *

class InputController:
    def __init__(self, character, target=None):
        self.character = character
        self.target = target

        self.WANDER = Wander(character, target)
        self.PURSUE = Pursue(character, target)
        self.SEEK = Seek(character, target)
        self.FLEE = Flee(character, target)
        self.FACE = Face(character, target)
        self.ALIGN = Align(character, target)
        self.ARRIVE = Arrive(character, target)
        self.EVADE = Evade(character, target)
        self.SEPARATION = Separation(character)
        self.VELOCITY_MATCH = VelocityMatch(character, target)
        self.ATTRACTION = Attraction(character)
        self.COLLISION_AVOIDANCE = CollisionAvoidance(character)
        self.OBSTACLE_AVOIDANCE = ObstacleAvoidance(character, target)

        self.key_to_state = {
            pygame.K_1: self.WANDER,
            pygame.K_2: self.PURSUE,
            pygame.K_3: self.SEEK,
            pygame.K_4: self.FLEE,
            pygame.K_5: self.FACE,
            pygame.K_6: self.ALIGN,
            pygame.K_7: self.ARRIVE,
            pygame.K_8: self.EVADE,
            pygame.K_9: self.SEPARATION,
            pygame.K_q: self.VELOCITY_MATCH,
            pygame.K_w: self.ATTRACTION,
            pygame.K_e: self.COLLISION_AVOIDANCE,
            pygame.K_r: self.OBSTACLE_AVOIDANCE
        }

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            state = self.key_to_state.get(event.key)
            if state: self.character.state_machine.change_state(state)