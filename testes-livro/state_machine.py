from states import State

class StateMachine:
    def __init__(self, owner, start_state=None):
        self.owner = owner
        self.current_state = start_state
        self.previous_state = None

        if start_state: self.current_state.enter(self.owner)

    def update(self):
        if self.current_state:
            self.current_state.execute(self.owner)

    def change_state(self, new_state: State):
        if not new_state: return

        if self.current_state:
            self.current_state.exit(self.owner)

        self.previous_state = self.current_state
        self.current_state = new_state

        self.current_state.enter(self.owner)

    def revert_to_previous_state(self):
        if self.previous_state:
            self.change_state(self.previous_state)