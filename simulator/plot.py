import pygame
import numpy as np

def draw_torque(screen, pivot_x, pivot_y, torque=0.0):
    scale = 0.02  # tune this visually
    length = torque * scale
    if abs(length) < 1e-3:
        return

    direction = 1 if length > 0 else -1
    radius = 30
    start_angle = 0
    end_angle = direction * abs(length)
    rect = pygame.Rect(
        pivot_x - radius,
        pivot_y - radius,
        2 * radius,
        2 * radius
    )
    pygame.draw.arc(
        screen,
        (0, 120, 255),
        rect,
        start_angle,
        end_angle,
        2
    )

def draw_pendulum(screen, pendulum, torque=0.0):
    pivot_x = 400
    pivot_y = 250

    pixels_per_meter = 200
    x = pivot_x + pendulum.length * pixels_per_meter * np.sin(pendulum.theta)
    y = pivot_y + pendulum.length * pixels_per_meter * np.cos(pendulum.theta)
    pygame.draw.line(
        screen,
        (0,0,0),
        (pivot_x,pivot_y),
        (x,y),
        3
    )
    pygame.draw.circle(     # pendulum bob
        screen,
        (255,0,0),
        (int(x),int(y)),
        15
    )
    pygame.draw.circle(     # pivot point
        screen,
        (0,0,0),
        (pivot_x,pivot_y),
        5
    )

    draw_torque(screen, pivot_x, pivot_y, torque=torque)


class LivePlot:
    def __init__(
        self,
        x,
        y,
        width,
        height,
        time_window=30.0,
        ymin=None,
        ymax=None,
        title=""
    ):

        self.rect = pygame.Rect(x, y, width, height)
        self.time_window = time_window
        self.points = []
        # If these are None, auto-scale
        self.ymin = ymin
        self.ymax = ymax
        self.title = title
        self.font = pygame.font.SysFont(None, 22)

    def add(self, t, value):
        self.points.append((t, value))
        # Remove anything older than the window
        while self.points and self.points[0][0] < t - self.time_window:
            self.points.pop(0)

    def draw(self, screen, color=(0,0,255)):
        # =========================
        # 1. BACKGROUND
        # =========================
        pygame.draw.rect(screen, (245,245,245), self.rect)
        pygame.draw.rect(screen, (0,0,0), self.rect, 2)

        # =========================
        # 2. TITLE
        # =========================
        if self.title:
            text = self.font.render(self.title, True, (0,0,0))
            screen.blit(text, (self.rect.x, self.rect.y - 22))

        if len(self.points) < 2:
            return

        # =========================
        # 3. Y-AXIS SCALING
        # =========================
        if self.ymin is None or self.ymax is None:
            values = [v for _, v in self.points]
            minimum = min(values)
            maximum = max(values)

            if abs(maximum - minimum) < 1e-6:
                maximum += 1
        else:
            minimum = self.ymin
            maximum = self.ymax

        # =========================
        # 4. TIME WINDOW
        # =========================
        current_time = self.points[-1][0]
        start_time = max(0.0, current_time - self.time_window)

        # =========================
        # 5. X-AXIS (TIME AXIS)
        # =========================
        axis_y = self.rect.bottom

        pygame.draw.line(
            screen,
            (0, 0, 0),
            (self.rect.left, axis_y),
            (self.rect.right, axis_y),
            1
        )

        num_ticks = 5

        for i in range(num_ticks + 1):
            t_tick = start_time + (i / num_ticks) * self.time_window
            x_tick = self.rect.left + ((t_tick - start_time) / self.time_window) * self.rect.width

            # tick mark
            pygame.draw.line(
                screen,
                (120, 120, 120),
                (x_tick, axis_y),
                (x_tick, axis_y + 5),
                1
            )

            # label
            label = self.font.render(f"{t_tick:.0f}", True, (0, 0, 0))
            screen.blit(label, (x_tick - 8, axis_y + 8))

        # =========================
        # 6. DATA CURVE
        # =========================
        plot_points = []

        for t, value in self.points:

            if t < start_time:
                continue

            value = max(minimum, min(maximum, value))

            x = self.rect.left + (
                (t - start_time) / self.time_window
            ) * self.rect.width

            y = self.rect.bottom - (
                (value - minimum) / (maximum - minimum)
            ) * self.rect.height

            plot_points.append((x, y))

        pygame.draw.lines(screen, color, False, plot_points, 2)