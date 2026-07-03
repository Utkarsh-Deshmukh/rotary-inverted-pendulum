import numpy as np

# Pendulum parameters
PENDULUM_DAMPING_COEFFICIENT = 0.75
PENDULUM_LENGTH_METERS = 1.0
PENDULUM_MASS_KG = 1.0

# simulation parameters
SIMULATION_FPS = 60
TIME_RESOLUTION = 1000

# controller parameters
KP = 30         # best value between 10 - 50
KD = 0.5        # best value between 0.1 - 1.0

# miscellaneous parameters
ANGLE_DOWNWARD_RAD = 0
ANGLE_UPWARD_RAD = np.pi
ANGLE_INCLINE_45_RAD = -np.pi / 4
MAX_ALLOWABLE_TORQUE = 10.0
GRAVITY_ACCELERATION = 9.81