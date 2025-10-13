
class Limits:
    
    def __init__(
            self, 
            max_speed=1, 
            max_acceleration=1, 
            max_force=1, 
            max_prediction=1.0, 
            max_rotation=50, 
            max_angular_acceleration=50
        ) -> None:

        self.max_speed = max_speed
        self.max_force = max_force
        self.max_acceleration = max_acceleration
        self.max_prediction = max_prediction
        self.max_rotation = max_rotation
        self.max_angular_acceleration = max_angular_acceleration

class WanderThresholds:

    def __init__(
            self, 
            offset=2.0, 
            radius=1.0, 
            rate=0.4, 
            orientation=1
        ) -> None:

        self.wander_offset = offset
        self.wander_radius = radius
        self.wander_rate = rate
        self.wander_orientation = orientation 

class BehaviorThresholds:

    def __init__(
            self, 
            threshold=100, 
            decay_coefficient=100000, 
            time_to_target=0.25, 
            target_radius=2.0, 
            slow_radius=20, 
            detection_radius=50, 
            effect_radius=20, 
            avoid_distance=25, 
            collision_ray=50
        ) -> None:

        self.threshold = threshold
        self.decay_coefficient = decay_coefficient
        self.time_to_target = time_to_target
        self.target_radius = target_radius
        self.slow_radius = slow_radius
        self.detection_radius = detection_radius
        self.effect_radius = effect_radius
        self.avoid_distance = avoid_distance
        self.collision_ray = collision_ray