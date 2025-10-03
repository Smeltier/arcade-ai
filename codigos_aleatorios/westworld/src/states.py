import time
import bisect

from abc import ABC, abstractmethod
from entity import BaseGameEntity, ENTITY_MANAGER

class Telegram:
    sender: int
    receiver: int
    message: int
    dispatch_time: float
    extra_info = None

    def __init__(self, dispatch_time, sender, receiver, message, extra_info=None):
        self.sender = sender
        self.receiver = receiver
        self.message = message
        self.dispatch_time = dispatch_time
        self.extra_info = extra_info

    def __str__(self):
        return f"Quem enviou: {self.sender}, quem recebeu: {self.receiver}, mensagem: {self.message}, info {self.extra_info}."

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
        if self.current_state and self.current_state.on_message(self.owner, telegram):
            return True
        if self.global_state and self.global_state.on_message(self.owner, telegram):
            return True
        return False

class MessageDispatcher:
    def __init__(self):
        self.priority_queue = []

    def _discharge(self, receiver, telegram):
        if receiver is None:
            print(f"[WARN] Receptor {telegram.receiver} não encontrado ao disparar telegram.")
            return
        receiver.handle_message(telegram)

    def dispatch_message(self, delay, sender, receiver, message, extra_info=None):
        target_receiver = ENTITY_MANAGER.get_entity_from_id(receiver)
        if not target_receiver:
            print(f"\nEntidade {receiver} não foi encontrada.\n")
            return

        telegram = Telegram(0, sender, receiver, message, extra_info)

        if delay <= 0.0:
            self._discharge(target_receiver, telegram)
        else:
            current_time = time.time()
            telegram.dispatch_time = current_time + delay
            keys = [t.dispatch_time for t in self.priority_queue]
            idx = bisect.bisect_left(keys, telegram.dispatch_time)
            self.priority_queue.insert(idx, telegram)

    def dispatch_delayed_message(self):
        current_time = time.time()
        while self.priority_queue and self.priority_queue[0].dispatch_time <= current_time:
            telegram = self.priority_queue.pop(0)
            receiver = ENTITY_MANAGER.get_entity_from_id(telegram.receiver)
            self._discharge(receiver, telegram)


MESSAGE_DISPATCHER = MessageDispatcher()