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

class EntityManager:
    entity_map: dict = {}

    def register_entity(self, new_entity):
        self.entity_map[new_entity.ID] = new_entity

    def remove_entity(self, entity: BaseGameEntity):
        if entity.ID in self.entity_map:
            del self.entity_map[entity.ID]

    def get_entity_from_id(self, id):
        return self.entity_map.get(id, None)

ENTITY_MANAGER = EntityManager()