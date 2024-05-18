import time
import numpy as np
import matplotlib.pyplot as plt

PID_STEADY_STATE_ERROR = 1  # km/h

class VELOCITY_PLANNER:
    def __init__(self, target_velocity, max_velocity=50, current_velocity=0) -> None:
        self.target_v = target_velocity  # Refer from system as input
        self.max_velocity = max_velocity  # TODO: Refer from system as input
        # Accel, Brake, Keep
        self.acc_state = 'Accel'
        self.scenario_age = 2  # seconds
        self.update_frequency = 10  # Hz
        self.velocity = 0
        self.start_time = 0
        self.step_counter = 0  # Reset step counter
        self.current_velocity = current_velocity  # it should be current velocity TODO: Refer from system as input
        self.scenarios_flag = False
        self.init_scenarios = True
        self.time_log = []
        self.velocity_log = []

    def basic_velocity_planner(self):
        if self.acc_state == 'Accel':
            self.longitudinal_acc_2_velocity()

    def longitudinal_acc_scheduling(self, ref_time):
        # In the model a(x-b)^2 + c, b is fix to -10 and c is a*100
        a = 1 / (self.scenario_age * self.update_frequency)
        ## erci hanshu
        acc = (a * (ref_time - 10)**2 + a * 100) 
        ## sanci hanshu
        # acc = (a * (ref_time )**3 ) 

        if self.acc_state == 'Brake':
            acc = -acc  
        return acc
    
    def acc_to_velocity(self, acc):
        return acc * (1 / self.update_frequency)  # instantaneous speed

    def velocity_scheduling(self):
        acc = self.longitudinal_acc_scheduling(self.step_counter)
        self.current_velocity += self.acc_to_velocity(acc)
        self.current_velocity = min(self.current_velocity, self.max_velocity)
        self.current_velocity = max(self.current_velocity, 0)  # Ensure velocity doesn't go negative
        self.step_counter += 1  # Increment step counter

    def scenarios_scheduling(self):
        if self.init_scenarios:
            self.init_scenarios = False
            self.step_counter = 0  # Reset step counter
            self.start_time = time.time()

        if self.current_velocity > self.target_v + PID_STEADY_STATE_ERROR:
            self.acc_state = 'Brake'
            self.scenarios_flag = True
            self.scenario_age = 2  # seconds

        elif self.current_velocity < self.target_v - PID_STEADY_STATE_ERROR:
            self.acc_state = 'Accel'
            self.scenarios_flag = True
            self.scenario_age = 4  # seconds

        else:
            self.acc_state = 'Keeping'
            self.scenario_age = np.inf  # seconds
            self.scenarios_flag = False

        if self.scenarios_flag:
            self.velocity_scheduling()  # -> current velocity
            self.current_time = time.time()
            self.time_length = self.current_time - self.start_time
            # if self.time_length > self.scenario_age:  # -> if timeout set target v directly
            #     self.scenarios_flag = False  # timeout for scenarios
            #     self.init_scenarios = True  # Initialize the scenarios
            #     self.current_velocity = self.target_v

        self.velocity_log.append(self.current_velocity)
        return self.current_velocity
    
    def plot_velo(self):
        plt.figure(figsize=(10, 6))
        plt.plot(self.time_log, self.velocity_log, label='Velocity (km/h)', color='blue')
        plt.title('Current Velocity over Time')
        plt.xlabel('Time (s)')
        plt.ylabel('Velocity (km/h)')
        plt.grid(True)
        plt.legend()
        plt.show()

if __name__ == '__main__':
    vel_p = VELOCITY_PLANNER(target_velocity=40, max_velocity=50, current_velocity=0)
    count = 0
    start_time = time.time()
    while True:  # Simulate with 10Hz update frequency
        step_time = time.time() - start_time
        vel_p.scenarios_scheduling()
        vel_p.time_log.append(step_time)
        time.sleep(1 / vel_p.update_frequency)
        count += 1
        if count >500:
            break
        if count > 200:
            vel_p.target_v = -1
    vel_p.plot_velo()
