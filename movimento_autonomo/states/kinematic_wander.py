class KinematicWander(State):
    def __init__(self, character):
        super().__init__()

        self.character = character

    def execute(self):
        steering = self.get_steering()
        self.character.apply_kinematic_steering(steering, self.character.delta_time)
    
    def get_steering(self) -> KinematicSteeringOutput:
        steering = KinematicSteeringOutput()

        steering.velocity = pygame.math.Vector2(math.sin(self.character.orientation),
                                                -math.cos(self.character.orientation))

        steering.velocity *= self.character.max_speed

        random_rotation = random.uniform(-1.0, 1.0)

        steering.rotation = random_rotation * self.character.max_rotation

        return steering
    
    def enter(self):
        print(f"[DEBUG] {self.character.ID} -> KinematicWander")
        self.character.change_color("white")
    
    def exit(self): pass