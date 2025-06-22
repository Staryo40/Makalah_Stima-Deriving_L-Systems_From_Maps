import os
import math
import json
import matplotlib.pyplot as plt
import numpy as np

from classes import *
from util import *

# Helper: Euclidean distance
def euclidean(p1, p2):
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])

# Helper: angle in degrees from p1 to p2
def angle_from(p1, p2):
    dx, dy = p2[0] - p1[0], p2[1] - p1[1]
    return math.degrees(math.atan2(dy, dx))

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
        solution = SolutionNode(s, pos_s)

        # Get connected edges (with geometry)
        connected_edges = [(u, v, k, data) for (u, v, k), data in E.items() if u == s or v == s]
        other_nodes = set()

        for u, v, k, data in connected_edges:
            other = v if u == s else u
            pos_other = positions[other]
            other_nodes.add(tuple(pos_other))

            # Compute angle and distance
            dist = np.linalg.norm(np.array(pos_s) - np.array(pos_other))
            angle = angle_from(pos_s, pos_other)
            branch = Branch(other, angle, dist)
            if branch not in solution.branches:
                solution.branches.append(branch)

            # Mark other node for future exploration
            # if other in N:
            #     N.remove(other)
            # visited.add(other)

            # Remove this edge
            del E[(u, v, k)]

        patterns.append(solution)

    return patterns

def remap_node_ids(patterns):
    # Step 1: Build old_id → new_id mapping
    old_ids = [node.id for node in patterns]
    id_map = {old_id: new_id for new_id, old_id in enumerate(old_ids, start=1)}

    # Step 2: Update each node and its branches
    for node in patterns:
        node.id = id_map[node.id]
        for branch in node.branches:
            if branch.target_id in id_map:
                branch.target_id = id_map[branch.target_id]

    return patterns

# pos_s = (6582675165, 9232478.797442723)
# pos_other = (794048.9783622319, 9234230.572373135)
# a1 = angle_from(pos_s, pos_other)
# a2 = angle_from(pos_other, pos_s)

# print(f"a1 = {a1}, a2 = {a2}, diff = {abs(a1 - (a2 + 180) % 360)}")

# Load the Bandung graph
path = os.path.join(os.getcwd(), "data", "bandung.graphml")
G = ox.load_graphml(path)
G = ox.project_graph(G)

# Convert positions to a hashable and comparable format (tuples)
positions = {n: (data['x'], data['y']) for n, data in G.nodes(data=True)}

# Run and print result
patterns = extract_patterns(G)
patterns_new = remap_node_ids(patterns)
save_patterns_to_json(patterns_new, "bandung_new.json")

# print(len(patterns))
# plot_patterns(patterns, show_labels=False)
# plt.show()
