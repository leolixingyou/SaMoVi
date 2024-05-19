import math
import time
import numpy as np
import matplotlib.pyplot as plt

PID_STEADY_STATE_ERROR = 1  # km/h
MIN_ACC = -20
MAX_ACC = 20

class VELOCITY_PLANNER:
    def __init__(self, target_velocity, max_velocity=50, current_velocity=0) -> None:
        self.target_v = target_velocity
        self.max_velocity = max_velocity
        self.acc_state = 'Accel'
        self.scenario_age = 2
        self.update_frequency = 10
        self.velocity = 0
        self.start_time = 0
        self.step_counter = 0
        self.current_velocity = current_velocity
        self.scenarios_flag = False
        self.scenarios_overtime = False
        self.init_scenarios = True
        self.time_log = []
        self.acc_time_log = []
        self.velocity_log = []
        self.target_velocity_log = []
        self.acc_log = []
        self.velocity_diff_log = []

    

    def velocity_scheduling(self):
        ### t:0~100 s: 0~78.210785211
        # self.current_velocity = 2*(self.step_counter-10)**(7/9)
        self.current_velocity = 6*self.step_counter**(1/3)
        self.current_velocity = self.current_velocity.real
        self.current_velocity = min(self.current_velocity, self.max_velocity)
        self.current_velocity = max(self.current_velocity, 0)
        self.step_counter += 1

    def scenarios_scheduling(self):
        if self.init_scenarios:
            self.init_scenarios = False
            self.step_counter = 0
            self.start_time = time.time()

        if self.current_velocity > self.target_v + PID_STEADY_STATE_ERROR:
            self.acc_state = 'Brake'
            self.scenarios_flag = True
            self.scenario_age = 100

        elif self.current_velocity < self.target_v - PID_STEADY_STATE_ERROR:
            self.acc_state = 'Accel'
            self.scenarios_flag = True
            self.scenario_age = 100

        else:
            self.acc_state = 'Keeping'
            self.scenario_age = np.inf
            self.scenarios_flag = False

        if self.scenarios_flag and not self.scenarios_overtime:
            self.velocity_scheduling()
            if self.step_counter > self.scenario_age:
                self.scenarios_overtime = True

        self.current_time = time.time()
        self.time_length = self.current_time - self.start_time
        self.velocity_log.append(self.current_velocity)
        self.target_velocity_log.append(self.target_v)
        self.velocity_diff_log.append(abs(self.current_velocity - self.target_v))
        self.time_log.append(self.time_length)
        return self.current_velocity
    
    def plot_velo(self):
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 15))

        ax1.plot(self.time_log, self.velocity_log, label='Current Velocity (km/h)', color='blue')
        ax1.plot(self.time_log, self.target_velocity_log, label='Target Velocity (km/h)', color='red', linestyle='--')
        ax1.set_title('Current and Target Velocity over Time')
        ax1.set_xlabel('Time (s)')
        ax1.set_ylabel('Velocity (km/h)')
        ax1.grid(True)
        ax1.legend()

        ax2.plot(self.time_log, self.velocity_diff_log, label='Velocity Difference (km/h)', color='purple')
        ax2.set_title('Velocity Difference over Time')
        ax2.set_xlabel('Time (s)')
        ax2.set_ylabel('Velocity Difference (km/h)')
        ax2.grid(True)
        ax2.legend()

        ax3.plot(self.acc_time_log, self.acc_log, label='Acceleration (m/s^2)', color='green')
        ax3.set_title('Acceleration over Time')
        ax3.set_xlabel('Time (s)')
        ax3.set_ylabel('Acceleration (m/s^2)')
        ax3.grid(True)
        ax3.legend()

        plt.tight_layout()
        plt.show()

if __name__ == '__main__':
    vel_p = VELOCITY_PLANNER(target_velocity=40, max_velocity=50, current_velocity=0)
    count = 0
    start_time = time.time()
    while True:
        step_time = time.time() - start_time
        vel_p.scenarios_scheduling()
        time.sleep(1 / vel_p.update_frequency)
        count += 1
        if count > 100:
            break
        if count > 800:
            vel_p.target_v = 0
    vel_p.plot_velo()
