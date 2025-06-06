import os
import math
import json
import osmnx as ox
import networkx as nx
from shapely.geometry import LineString, Point
import matplotlib.pyplot as plt
import numpy as np

# Load the Bandung graph
path = os.path.join(os.getcwd(), "data", "bandung.graphml")
G = ox.load_graphml(path)
G = ox.project_graph(G)

# Convert positions to a hashable and comparable format (tuples)
positions = {n: (data['x'], data['y']) for n, data in G.nodes(data=True)}
# positions = {node: (data['x'], data['y']) for node, data in G.nodes(data=True)}

# Helper: Euclidean distance
def euclidean(p1, p2):
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])

# Helper: angle in degrees from p1 to p2
def angle_from(p1, p2):
    dx, dy = p2[0] - p1[0], p2[1] - p1[1]
    return math.degrees(math.atan2(dy, dx))

# Branch data structure
class Branch:
    def __init__(self, angle, distance):
        self.angle = angle
        self.distance = distance

    def __repr__(self):
        return f"Branch(angle={self.angle:.2f}, distance={self.distance:.2f})"

# Solution node
class SolutionNode:
    def __init__(self, position):
        self.position = position
        self.branches = []

    def __repr__(self):
        return f"SolutionNode(position={self.position}, branches={self.branches})"

# Main function
def extract_patterns(G):
    visited = set()
    E = {(u, v, k): data for u, v, k, data in G.edges(keys=True, data=True) if 'geometry' in data}
    N = set(G.nodes)
    patterns = []

    while N:
        s = N.pop()
        if s in visited:
            continue
        visited.add(s)
        pos_s = positions[s]
        solution = SolutionNode(pos_s)

        # Get connected edges (with geometry)
        connected_edges = [(u, v, k, data) for (u, v, k), data in E.items() if u == s or v == s]
        other_nodes = set()

        for u, v, k, data in connected_edges:
            other = v if u == s else u
            pos_other = positions[other]
            other_nodes.add(tuple(pos_other))

            # Compute angle and distance
            # dist = euclidean(pos_s, pos_other)
            dist = np.linalg.norm(np.array(pos_s) - np.array(pos_other))
            angle = angle_from(pos_s, pos_other)
            solution.branches.append(Branch(angle, dist))

            # Mark other node for future exploration
            if other in N:
                N.remove(other)
            visited.add(other)

            # Remove this edge
            del E[(u, v, k)]
        # print(f"Start node {s} at {pos_s}, other node {other} at {pos_other}, distance = {euclidean(pos_s, pos_other)}")

        patterns.append(solution)

    return patterns

def plot_patterns(patterns, ax=None, show_labels=True):
    """
    Plot a list of branching patterns (from extract_patterns) in matplotlib.

    Parameters:
    - patterns: list of dicts, each with:
        - 'position': (x, y)
        - 'branches': list of {'angle': float (degrees), 'distance': float}
    - ax: optional matplotlib axes to draw on
    - show_labels: whether to label nodes with indices
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 10))

    for i, pattern in enumerate(patterns):
        origin = np.array(pattern.position)
        # ax.plot(*origin, 'o', color='blue')
        if show_labels:
            ax.text(*origin, str(i), fontsize=8, ha='right', va='bottom')

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
    ax.set_title("Extracted L-system-like Branch Patterns")

def save_patterns_to_json(patterns, filename):
    """
    Serialize extracted patterns into a JSON file.

    Parameters:
    - patterns: list of SolutionNode instances
    - filename: path to save the JSON output
    """
    serializable_patterns = []

    for pattern in patterns:
        node_dict = {
            'position': list(pattern.position),
            'branches': [
                {'angle': branch.angle, 'distance': branch.distance}
                for branch in pattern.branches
            ]
        }
        serializable_patterns.append(node_dict)

    with open(filename, 'w') as f:
        json.dump(serializable_patterns, f, indent=2)

    print(f"Saved {len(patterns)} patterns to {filename}")

# Run and print result
patterns = extract_patterns(G)
# save_patterns_to_json(patterns, "bandung.json")
# for pattern in patterns[:10]:  # show a few
#     print(pattern)

plot_patterns(patterns, show_labels=False)
plt.show()
