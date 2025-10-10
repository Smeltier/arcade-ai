from abc import ABC, abstractmethod

class BaseGameEntity (ABC):
    _next_ID = 0

    def __init__(self):
        self.ID = BaseGameEntity._next_ID
        BaseGameEntity._next_ID += 1

    @abstractmethod
    def update(self, delta_time) -> None: pass