from entity import BaseGameEntity
from states import State, StateMachine, Telegram, Message
import random

class Elsa(BaseGameEntity):
    def __init__(self):
        super().__init__()

        self.state_machine = StateMachine(self, start_state=None, global_state=None)

    def handle_message(self, telegram: Telegram) -> bool:
        if telegram.menssage == Message.HI_HONEY_IM_HOME:
            print("")

class ElsaGlobalState(State):
    def execute(self, elsa):
        pass

    def enter(self, elsa):
        pass

    def exit(self, elsa):
        pass


class CookStew(State):
    def execute(self, elsa):
        pass

    def enter(self, elsa):
        pass

    def exit(self, elsa):
        pass

 
class DoHouseWork(State):
    tasks = ["Limpando o banheiro..",
             "Arrumando a cama",
             "Varrendo a casa",
             "Lavando os pratos"
    ]

    def enter(self, elsa: Elsa):
        pass

    def execute(self, elsa: Elsa):
        random_task = random.randint(0, 4)
        print(f"{self.name} - {self.ID}: " + self.tasks[random_task])

    def exit(self, elsa: Elsa):
        pass


class VisitBathroom(State):
    def execute(self, elsa):
        pass

    def enter(self, elsa):
        pass

    def exit(self, elsa):
        pass


ELSA_GLOBAL_STATE = ElsaGlobalState()
VISIT_BATHROOM = VisitBathroom()
DO_HOUSE_WORK = DoHouseWork()
COOK_STEW = CookStew()