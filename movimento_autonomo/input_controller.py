import pygame

from moving_entity import MovingEntity
from states.state import State
from states.align import Align
from states.seek import Seek
from states.wander import Wander
from states.face import Face
from states.arrive import Arrive
from states.evade import Evade
from states.separation import Separation
from states.obstacle_avoidance import ObstacleAvoidance
from states.collision_avoidance import CollisionAvoidance
from states.pursue import Pursue
from states.velocity_match import VelocityMatch
from states.flee import Flee
from states.attraction import Attraction

class InputController:
    def __init__(self, character, target=None):
        self.character = character
        self.target = target

        self.key_to_state = {
            pygame.K_1: Wander,
            pygame.K_2: Pursue,
            pygame.K_3: Seek,
            pygame.K_4: Flee,
            pygame.K_5: Face,
            pygame.K_6: Align,
            pygame.K_7: Arrive,
            pygame.K_8: Evade,
            pygame.K_9: Separation,
            pygame.K_q: VelocityMatch,
            pygame.K_w: Attraction,
            pygame.K_e: CollisionAvoidance,
            pygame.K_r: ObstacleAvoidance
        }

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            state: State = self.key_to_state.get(event.key)

            if state in [Attraction, Separation, CollisionAvoidance]:
                new_state = state(self.character)
            else:
                new_state = state(self.character, self.target)

            if state: self.character.state_machine.change_state(new_state)