import numpy as np
import matplotlib.pyplot as plt

def plot_patterns(patterns, ax=None):
    """
    Plot a list of branching patterns (from extract_patterns) in matplotlib.

    Parameters:
    - patterns: list of LocationNode objects (with position and branches)
    - ax: optional matplotlib axes to draw on
    - show_labels: whether to label nodes with indices
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 10))

    for pattern in patterns:
        origin = np.array(pattern.position)

        for branch in pattern.branches:
            angle_rad = np.radians(branch.angle)
            dx = branch.distance * np.cos(angle_rad)
            dy = branch.distance * np.sin(angle_rad)
            end = origin + np.array([dx, dy])
            ax.arrow(origin[0], origin[1], dx, dy,
                     head_width=0.5, head_length=0.8,
                     length_includes_head=True, fc='orange', ec='orange')

    ax.set_aspect('equal')
    ax.grid(True)
    ax.set_title("Raw GraphML Patterns from Nodes")
    plt.show()