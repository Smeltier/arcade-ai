
class Limits:
    def __init__(self, max_speed=1, max_acceleration=1, max_force=1, max_prediction=1.0, max_rotation=50, max_angular_acceleration=50) -> None:
        self.max_speed = max_speed
        self.max_force = max_force
        self.max_acceleration = max_acceleration
        self.max_prediction = max_prediction
        self.max_rotation = max_rotation
        self.max_angular_acceleration = max_angular_acceleration

class WanderThresholds:
    def __init__(self) -> None:
        # self.wander_offset = 2.0
        # self.wander_radius = 1.0
        # self.wander_rate = 0.4
        # self.wander_orientation = 1 
        pass