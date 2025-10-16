class KinematicArrive(State):
    def __init__(self, character, target):
        super().__init__()

        self.character = character
        self.target = target

    def execute(self):
        steering = self.get_steering()
        self.character.apply_kinematic_steering(steering, self.character.delta_time)

        # if self.character.distance > 50:
        #     self.character.state_machine.change_state(Pursue(self.character, self.target))

    def get_steering(self) -> KinematicSteeringOutput:
        steering = KinematicSteeringOutput()

        steering.velocity = self.target.position - self.character.position

        if steering.velocity.length() < self.character.slow_radius:
            return KinematicSteeringOutput()
        
        steering.velocity /= self.character.time_to_target

        if steering.velocity.length() > self.character.max_speed:
            steering.velocity.scale_to_length(self.character.max_acceleration)

        self.character.orientation = self.character.new_orientation(steering)

        steering.rotation = 0
        return steering
    
    def enter(self):
        print(f"[DEBUG] {self.character.ID} -> KinematicArrive")
        self.character.change_color("blue")
    
    def exit(self): pass