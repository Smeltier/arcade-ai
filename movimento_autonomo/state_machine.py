from states.state import State
 
class StateMachine:
    def __init__(self, owner, start_state=None):
        self.owner = owner

        self.current_state = start_state
        self.previous_state = None

        if self.current_state: 
            self.current_state.enter()

    def update(self):
        if self.current_state:
            self.current_state.execute()

    def change_state(self, new_state: State):
        if not new_state: return

        if self.current_state:
            self.current_state.exit()

        self.previous_state = self.current_state
        self.current_state = new_state

        self.current_state.enter()

    def revert_to_previous_state(self):
        if self.previous_state:
            self.change_state(self.previous_state)