import numpy as np
import constants

class Pendulum:
    def __init__(self):
        self.length = constants.PENDULUM_LENGTH_METERS
        self.gravity = constants.GRAVITY_ACCELERATION
        self.mass = constants.PENDULUM_MASS_KG
        
        # Initial state
        self.theta = constants.ANGLE_INCLINE_45_RAD
        self.omega = 0.0

        # Damping coefficient
        self.damping = constants.PENDULUM_DAMPING_COEFFICIENT

    def update(self, dt, torque = 0.0):
        I = self.mass * self.length**2
        gravity = -self.mass * self.gravity * self.length * np.sin(self.theta)
        damping = -self.damping * self.omega

        alpha = (gravity + damping + torque) / I
        self.omega += alpha * dt
        self.theta += self.omega * dt

class Controller:
    def __init__(self, Kp=constants.KP, Kd=constants.KD):
        self.Kp = Kp
        self.Kd = Kd
        self.max_allowable_torque = constants.MAX_ALLOWABLE_TORQUE

    def compute_control(self, pendulum, desired_theta=0.0):
        error = (desired_theta - pendulum.theta + np.pi) % (2*np.pi) - np.pi        # Computes the shortest angulur error. for example 540 degress == 180 degrees. this computation will ensure this.

        error_dot = -pendulum.omega

        control_torque = (self.Kp * error) + (self.Kd * error_dot)
        control_torque = np.clip(control_torque, -self.max_allowable_torque, self.max_allowable_torque)
        return control_torque