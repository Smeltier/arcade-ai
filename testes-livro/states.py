from abc import ABC, abstractmethod
from steering_behaviors import Seek, Flee, Pursue, Arrive, Evade

class State(ABC):
    @abstractmethod
    def execute(self, entity): pass

    @abstractmethod
    def enter(self, entity): pass
    
    @abstractmethod
    def exit(self, entity): pass

class ArriveState(State):
    def execute(self, entity):
        if entity.arrive_behavior:
            steering = entity.arrive_behavior.get_steering()
            entity.apply_steering(steering, entity.delta_time)

        if entity.distance > 10:
            entity.state_machine.change_state(PursueState())

    def enter(self, entity):
        print(f"[DEBUG] {entity.ID} -> Arrive")
        entity.change_color("blue")
        entity.arrive_behavior = Arrive(entity, entity.target, entity.max_speed, entity.max_acceleration, 50, 5)
    
    def exit(self, entity):
        entity.arrive_behavior = None

class SeekState(State):
    def execute(self, entity):
        if entity.seek_behavior:
            steering = entity.seek_behavior.get_steering()
            entity.apply_steering(steering, entity.delta_time)

        if entity.distance <= 100:
            entity.state_machine.change_state(PursueState())

    def enter(self, entity):
        print(f"[DEBUG] {entity.ID} -> Seek")
        entity.change_color("green")
        entity.seek_behavior = Seek(entity, entity.target, entity.max_acceleration)
    
    def exit(self, entity):
        entity.seek_behavior = None

class PursueState(State):
    def execute(self, entity):
        if entity.pursue_behavior:
            steering = entity.pursue_behavior.get_steering()
            entity.apply_steering(steering, entity.delta_time)

        if entity.distance > 100:
            entity.state_machine.change_state(SeekState())
        elif entity.distance <= 10:
            entity.state_machine.change_state(ArriveState())

    def enter(self, entity):
        print(f"[DEBUG] {entity.ID} -> Pursue")
        entity.change_color("orange")
        entity.pursue_behavior = Pursue(entity, entity.target, entity.max_acceleration)
    
    def exit(self, entity):
        entity.pursue_behavior = None

class EvadeState(State):
    def execute(self, entity):
        if entity.evade_behavior:
            steering = entity.evade_behavior.get_steering()
            entity.apply_steering(steering, entity.delta_time)

        if entity.distance > 200:
            entity.state_machine.change_state(FleeState()) 

    def enter(self, entity):
        print(f"[DEBUG] {entity.ID} -> Evade")
        entity.change_color("purple")
        entity.evade_behavior = Evade(entity, entity.target, entity.max_acceleration, max_prediction=1.0)
    
    def exit(self, entity):
        entity.evade_behavior = None

class FleeState(State):
    def execute(self, entity):
        if entity.flee_behavior:
            steering = entity.flee_behavior.get_steering()
            entity.apply_steering(steering, entity.delta_time)

        if entity.distance <= 200:
            entity.state_machine.change_state(EvadeState()) 

    def enter(self, entity):
        print(f"[DEBUG] {entity.ID} -> Flee")
        entity.change_color("yellow")
        entity.flee_behavior = Flee(entity, entity.target, entity.max_acceleration)
    
    def exit(self, entity):
        entity.flee_behavior = None