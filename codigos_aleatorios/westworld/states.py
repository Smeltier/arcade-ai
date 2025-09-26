from abc import ABC, abstractmethod

from entity import BaseGameEntity

class Telegram:
    sender: int
    receiver: int
    message: int
    dispatch_time: float
    extra_info = None

    def __str__(self):
        return f"Quem enviou: {self.sender}, quem recebeu: {self.receiver}, mensagem: {self.mensage}, info {self.extra_info}."

class Message:
    HI_HONEY_IM_HOME = 1
    STEW_READY = 2

class State (ABC):
    @abstractmethod
    def execute(self, entity: BaseGameEntity): pass

    @abstractmethod
    def enter(self, entity: BaseGameEntity): pass

    @abstractmethod
    def exit(self, entity: BaseGameEntity): pass 

    @abstractmethod
    def on_message(self, entity: BaseGameEntity, telegram: Telegram) -> bool: pass


class StateMachine: 

    def __init__(self, owner: BaseGameEntity, start_state: State, global_state: State = None):
        self.owner: BaseGameEntity  =   owner
        self.global_state: State    =   global_state
        self.current_state: State   =   start_state
        self.previous_state: State  =   None

    def update(self) -> None:
        if self.global_state:
            self.global_state.execute(self.owner)
        if self.current_state:
            self.current_state.execute(self.owner)

    def change_state(self, new_state) -> None:
        if new_state is None: return

        self.previous_state = self.current_state
        self.current_state = new_state

        self.previous_state.exit(self.owner)
        self.current_state.enter(self.owner)

    def reverse_to_previous(self) -> None:
        if self.previous_state:
            self.change_state(self.previous_state)

    def is_in_state(self, state) -> bool:
        return isinstance(self.current_state, state)
    
    def handle_message(self, telegram: Telegram) -> bool:
        if self.current_state and self.global_state.on_message(self.owner, telegram):
            return True
        if self.global_state and self.global_state.on_message(self.owner, telegram):
            return True
        return False