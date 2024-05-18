class VELOCITY_PLANNER:
    def __init__(self) -> None:
        self.max_velocity = 50 ## TODO: Refer from system as input 
    def basic_velocity_planner(self,):
        pass

    def calculate_longitudinal_acceleration(initial_speed, final_speed, time):
        return (final_speed - initial_speed) / time

    def calculate_lateral_acceleration(speed, curvature):
        return speed ** 2 * curvature


    