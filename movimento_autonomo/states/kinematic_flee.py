class KinematicFlee(State):
    def __init__(self, character, target):
        super().__init__()

        self.character = character
        self.target = target

    def execute(self):
        steering = self.get_steering()
        self.character.apply_kinematic_steering(steering, self.character.delta_time)

        # if self.character.distance <= 200:
        #     self.character.state_machine.change_state(Evade(self.character, self.target)) 

    def get_steering(self) -> KinematicSteeringOutput:
        steering = KinematicSteeringOutput()

        if not self.target:
            return steering

        steering.velocity = self.character.position - self.target.position
        steering.velocity.normalize_ip()
        steering *= self.character.max_speed

        self.character.orientation = self.character.new_orientation(steering)

        steering.rotation = 0.0
        return steering 

    def enter(self):
        print(f"[DEBUG] {self.character.ID} -> KinematicFlee")
        self.character.change_color("yellow")
    
    def exit(self): pass
