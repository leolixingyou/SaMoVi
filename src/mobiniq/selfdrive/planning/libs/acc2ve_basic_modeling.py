import numpy as np
import matplotlib.pyplot as plt

# Define the time range
t = np.linspace(0, 20, 400)

# Define the parabolic acceleration function (opens downwards)
a = -0.05 * (t - 10)**2 + 5

# Integrate the acceleration to get the velocity
# Initial velocity is assumed to be zero
v = np.cumsum(a) * (t[1] - t[0])

# Plotting the acceleration vs time
plt.figure(figsize=(12, 6))

plt.subplot(2, 1, 1)
plt.plot(t, a, label='Acceleration', color='blue')
plt.title('Acceleration vs Time')
plt.xlabel('Time (s)')
plt.ylabel('Acceleration (m/s^2)')
plt.grid(True)
plt.legend()

# Plotting the velocity vs time
plt.subplot(2, 1, 2)
plt.plot(t, v, label='Velocity', color='red')
plt.title('Velocity vs Time')
plt.xlabel('Time (s)')
plt.ylabel('Velocity (m/s)')
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()
