from steering_output import SteeringOutput

class Seek:
    def __init__(self, character: object, target: object, max_acceleration: float):
        self.character = character
        self.target = target
        self.max_aceleration = max_acceleration

    def get_steering(self: object) -> SteeringOutput:
        steering = SteeringOutput()
        if not self.target:
            return steering

        steering.linear = self.target.position - self.character.position
        steering.linear.normalize_ip()
        steering.linear *= self.max_aceleration

        return steering
    
class Flee:
    def __init__(self, character: object, target: object, max_acceleration: float):
        self.character = character
        self.target = target
        self.max_aceleration = max_acceleration

    def get_steering(self) -> SteeringOutput:
        steering = SteeringOutput()
        if not self.target:
            return steering

        steering.linear = self.character.position - self.target.position
        steering.linear.normalize_ip()
        steering.linear *= self.max_aceleration

        return steering   

class Arrive:
    def __init__(self, character: object, target: object, max_speed: float, max_acceleration: float, slow_radius: float, target_radius: float, time_to_target: float = 0.1):
        self.character = character
        self.target = target
        self.max_speed = max_speed
        self.max_acceleration = max_acceleration
        self.slow_radius = slow_radius
        self.target_radius = target_radius
        self.time_to_target = time_to_target

    def get_steering(self):
        steering = SteeringOutput()
        if not self.target:
            return steering
            
        direction = self.target.position - self.character.position
        distance = direction.length()

        if distance < self.target_radius:
            return SteeringOutput()
        
        if distance > self.slow_radius: target_speed = self.max_speed
        else: target_speed = self.max_speed * distance / self.slow_radius

        target_velocity = direction.normalize() * target_speed
        
        steering.linear = (target_velocity - self.character.velocity) / self.time_to_target

        if steering.linear.length() > self.max_acceleration:
            steering.linear.scale_to_length(self.max_acceleration)

        return steering
    
class Pursue(Seek):
    def __init__(self, character, target, max_acceleration, max_prediction=1.0):
        super().__init__(character, target, max_acceleration)
        self.max_prediction = max_prediction

    def get_steering(self):
        steering = SteeringOutput()
        if not self.target:
            return steering
            
        direction = self.target.position - self.character.position
        distance = direction.length()
        speed = self.character.velocity.length()

        if speed <= distance / self.max_prediction:
            prediction = self.max_prediction
        else:
            prediction = distance / speed

        predicted_position = self.target.position + self.target.velocity * prediction

        steering.linear = predicted_position - self.character.position
        steering.linear.normalize_ip()
        steering.linear *= self.max_aceleration
        
        return steering
    
class Evade(Flee):
    def __init__(self, character, target, max_acceleration, max_prediction=1.0):
        super().__init__(character, target, max_acceleration)
        self.max_prediction = max_prediction

    def get_steering(self):
        steering = SteeringOutput()
        if not self.target:
            return steering

        direction = self.character.position - self.target.position 
        distance = direction.length()
        speed = self.character.velocity.length()

        if speed <= distance / self.max_prediction:
            prediction = self.max_prediction
        else:
            prediction = distance / speed

        predicted_position = self.target.position + self.target.velocity * prediction

        steering.linear = self.character.position - predicted_position
        steering.linear.normalize_ip()
        steering.linear *= self.max_aceleration
        return steering