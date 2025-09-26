from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from states import StateMachine
    from states import GO_HOME_AND_SLEEP_TIL_RESTED

class BaseGameEntity(ABC):
    _next_id = 1000

    def __init__(self): 
        self.ID = BaseGameEntity._next_id
        BaseGameEntity._next_id += 1

    @abstractmethod
    def update(self): pass