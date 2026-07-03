import pygame
import numpy as np

from physics import Pendulum, Controller
from plot import LivePlot, draw_pendulum
import constants

if __name__ == "__main__":

    pygame.init()
    WIDTH = 800
    HEIGHT = 900
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    pendulum = Pendulum()
    controller = Controller()

    angle_plot = LivePlot(x=20,y=500,width=360,height=150,ymin=-180,ymax=180)
    velocity_plot = LivePlot(x=420,y=500,width=360,height=150,ymin=-8,ymax=8)

    torque_plot = LivePlot(x=20,y=720,width=360,height=150,ymin=-controller.max_allowable_torque,ymax=controller.max_allowable_torque,title="Control Torque (N·m)")
    error_plot = LivePlot(x=420,y=720,width=360,height=150,ymin=-180,ymax=180,title="Angle Error (deg)")

    font = pygame.font.SysFont(None, 24)

    running = True
    simulation_time = 0.0
    desired_theta = constants.ANGLE_UPWARD_RAD
    while running:
        dt = clock.tick(constants.SIMULATION_FPS) / constants.TIME_RESOLUTION
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        computed_torque = controller.compute_control(pendulum, desired_theta=desired_theta)
        pendulum.update(dt, torque=computed_torque)
        simulation_time += dt
        
        angle_plot.add(simulation_time, np.degrees(pendulum.theta))
        velocity_plot.add(simulation_time, pendulum.omega)
        
        angle_error = (
            (desired_theta - pendulum.theta + np.pi)
            % (2 * np.pi)
        ) - np.pi

        torque_plot.add(simulation_time, computed_torque)
        error_plot.add(simulation_time,np.degrees(angle_error))

        screen.fill((255,255,255))
        draw_pendulum(screen, pendulum, torque=computed_torque)

        angle_plot.draw(screen)
        label = font.render("Angle (deg)", True, (0,0,0))
        screen.blit(label, (20,475))
        
        velocity_plot.draw(screen, (255,0,0))
        label = font.render("Angular Velocity (rad/s)", True, (0,0,0))
        screen.blit(label, (420,475))

        torque_plot.draw(screen)

        error_plot.draw(screen, (0, 150, 0))

        pygame.display.flip()

    pygame.quit()