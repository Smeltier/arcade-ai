import time

from miner import Miner, ENTER_MINE_AND_DIG_FOR_NUGGET
from elsa import Elsa, DO_HOUSE_WORK
from entity import ENTITY_MANAGER
from states import MESSAGE_DISPATCHER

def main():

    mineiro_bob: Miner = Miner("Jobson", 5)
    esposa_elsa: Elsa = Elsa("Mariana")

    mineiro_bob.wife_id = esposa_elsa.ID
    esposa_elsa.husband_id = mineiro_bob.ID

    ENTITY_MANAGER.register_entity(mineiro_bob)
    ENTITY_MANAGER.register_entity(esposa_elsa)

    goal = 100
    while mineiro_bob.gold_carried < goal:
        mineiro_bob.update()
        esposa_elsa.update()
        time.sleep(1)

        MESSAGE_DISPATCHER.dispatch_delayed_message()

if __name__ == "__main__":
    main()