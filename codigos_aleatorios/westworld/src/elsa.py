from entity import BaseGameEntity
from states import State, StateMachine, Telegram, Message, MESSAGE_DISPATCHER
import random

class Elsa(BaseGameEntity):
    name: str
    cooking: bool
    husband_id: int

    def __init__(self, name):
        super().__init__()

        self.state_machine = StateMachine(self, start_state=DO_HOUSE_WORK, global_state=ELSA_GLOBAL_STATE)

        self.cooking = False
        self.name = name

    def update(self):
        self.state_machine.update()

    def handle_message(self, telegram: Telegram) -> bool:
        if telegram.message == Message.HI_HONEY_IM_HOME:
            self.state_machine.change_state(COOK_STEW)
            return True
        if telegram.message == Message.STEW_READY:
            MESSAGE_DISPATCHER.dispatch_message(0, self.ID, self.husband_id, Message.STEW_READY)
            self.state_machine.change_state(DO_HOUSE_WORK)
            return True
        return False

class ElsaGlobalState(State):
    def execute(self, elsa):
        pass

    def enter(self, elsa):
        pass

    def exit(self, elsa):
        pass

    def on_message(self, elsa: Elsa, telegram: Telegram) -> bool:
        if telegram.message == Message.HI_HONEY_IM_HOME:
            elsa.state_machine.change_state(COOK_STEW)
            return True
        return False

class CookStew(State):
    def enter(self, elsa: Elsa):
        if not elsa.cooking:
            print(f"{elsa.name} - {elsa.ID}: Começando a cozinhar o ensopado.")
            elsa.cooking = True

            MESSAGE_DISPATCHER.dispatch_message(1.5, elsa.ID, elsa.ID, Message.STEW_READY)

    def execute(self, elsa: Elsa):
        print(f"{elsa.name} - {elsa.ID}: Cozinhando o ensopado..")

    def exit(self, elsa: Elsa):
        print(f"{elsa.name} - {elsa.ID}: O ensopado está pronto..")
        elsa.cooking = False

    def on_message(self, elsa: Elsa, telegram) -> bool:
        return False

 
class DoHouseWork(State):
    tasks = ["Limpando o banheiro..",
             "Arrumando a cama",
             "Varrendo a casa",
             "Lavando os pratos"
    ]

    def enter(self, elsa: Elsa):
        pass

    def execute(self, elsa: Elsa):
        random_task = random.randint(0, 3)
        print(f"{elsa.name} - {elsa.ID}: " + self.tasks[random_task])

    def exit(self, elsa: Elsa):
        pass

    def on_message(self, elsa: Elsa, telegram: Telegram) -> bool:
        return False


class VisitBathroom(State):
    def execute(self, elsa):
        print(f"{elsa.name} - {elsa.ID}: Preciso ir no banheiro..")

    def enter(self, elsa):
        pass

    def exit(self, elsa):
        print(f"{elsa.name} - {elsa.ID}: Agora estou aliviada..")

    def on_message(self, elsa: Elsa, telegram: Telegram) -> bool:
        return False


ELSA_GLOBAL_STATE = ElsaGlobalState()
VISIT_BATHROOM = VisitBathroom()
DO_HOUSE_WORK = DoHouseWork()
COOK_STEW = CookStew()