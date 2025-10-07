#!/usr/bin/env python3
from __future__ import annotations

"""Minimal demo: animate a single moving point in matplotlib.

No CLI. All configuration is done via the variables below.
"""

import collections
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# ----- Configuration (edit these constants) ---------------------------------
image_width = 320
image_height = 200
point_color = "tab:blue"
point_size = 100  # scatter marker size (area)
frame_rate = 30  # frames per second
duration_seconds = 8
trail_length = 25  # how many previous positions to show
# ---------------------------------------------------------------------------


def main() -> None:
    total_frames = int(frame_rate * duration_seconds)

    # initial center position and simple velocity
    pos_x = image_width / 2.0
    pos_y = image_height / 2.0
    vel_x = 3.0
    vel_y = 1.5

    trail = collections.deque(maxlen=trail_length)
    trail.append((pos_x, pos_y))

    fig, ax = plt.subplots(figsize=(image_width / 100.0, image_height / 100.0))
    ax.set_xlim(0, image_width)
    ax.set_ylim(0, image_height)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title("Moving point")

    head = ax.scatter([pos_x], [pos_y], s=point_size, c=point_color)
    (trail_line,) = ax.plot([pos_x], [pos_y], lw=2, color=point_color, alpha=0.6)

    def step(frame_index: int):
        nonlocal pos_x, pos_y, vel_x, vel_y

        # update position
        pos_x += vel_x
        pos_y += vel_y

        # bounce on walls
        if pos_x <= 0:
            pos_x = 0
            vel_x = abs(vel_x)
        if pos_x >= image_width:
            pos_x = image_width
            vel_x = -abs(vel_x)
        if pos_y <= 0:
            pos_y = 0
            vel_y = abs(vel_y)
        if pos_y >= image_height:
            pos_y = image_height
            vel_y = -abs(vel_y)

        # small jitter to avoid perfectly linear motion
        jitter_x = (np.random.rand() - 0.5) * 0.6
        jitter_y = (np.random.rand() - 0.5) * 0.6
        pos_x += jitter_x
        pos_y += jitter_y

        trail.append((pos_x, pos_y))

        # update artists
        head.set_offsets([[pos_x, pos_y]])
        x_positions = [position[0] for position in trail]
        y_positions = [position[1] for position in trail]
        trail_line.set_data(x_positions, y_positions)

        return head, trail_line

    anim = FuncAnimation(fig, step, frames=total_frames, interval=1000.0 / frame_rate, blit=True)
    plt.show()


if __name__ == "__main__":
    main()
