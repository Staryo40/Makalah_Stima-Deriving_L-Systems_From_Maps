import os
import math, time
from collections import deque, defaultdict
import matplotlib.pyplot as plt
import numpy as np

from classes import *
from util import *

# Angle from source to target point, + means counter clockwise, - means clockwise from the origin of positive x-axis
def angle_from(p1, p2):
    dx, dy = p2[0] - p1[0], p2[1] - p1[1]
    return math.degrees(math.atan2(dy, dx))

# Main function
def extract_patterns(G, positions):
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
        solution = LocationNode(s, pos_s)

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

            # Remove this edge
            del E[(u, v, k)]

        patterns.append(solution)

    return remap_node_ids(patterns)

# Optimized version
def optimized_extract_patterns(G, positions):
    visited = set()
    patterns = []
    edge_dict = defaultdict(list)

    # Pre-process edges with geometry into a node-indexed dictionary
    for u, v, k, data in G.edges(keys=True, data=True):
        if 'geometry' in data:
            edge_dict[u].append((u, v, k, data))
            edge_dict[v].append((u, v, k, data))

    for s in G.nodes:
        if s in visited:
            continue
        visited.add(s)
        pos_s = positions[s]
        solution = LocationNode(s, pos_s)

        for u, v, k, data in edge_dict[s]:
            if 'geometry' not in data:
                continue
            other = v if u == s else u
            if other in visited:
                continue  # skip reverse direction to avoid double-counting

            pos_other = positions[other]
            dist = np.linalg.norm(np.array(pos_s) - np.array(pos_other))
            angle = angle_from(pos_s, pos_other)
            branch = Branch(other, angle, dist)

            if branch not in solution.branches:
                solution.branches.append(branch)

        patterns.append(solution)

    return remap_node_ids(patterns)

def preprocess_edges(G):
    """Preprocess edges with geometry into a node-to-edges map."""
    E = {(u, v, k): data for u, v, k, data in G.edges(keys=True, data=True) if 'geometry' in data}
    node_to_edges = defaultdict(list)
    for (u, v, k), data in E.items():
        node_to_edges[u].append((u, v, k, data))
        node_to_edges[v].append((u, v, k, data))
    return node_to_edges

def bfs_extract_patterns(G, positions):
    visited = set()
    patterns = []
    node_to_edges = preprocess_edges(G)

    for start in G.nodes:
        if start in visited or start not in node_to_edges:
            continue

        queue = deque([start])
        visited.add(start)

        while queue:
            s = queue.popleft()
            pos_s = positions[s]
            solution = LocationNode(s, pos_s)

            for u, v, k, data in node_to_edges[s]:
                other = v if u == s else u
                if other not in positions:
                    continue
                pos_other = positions[other]

                dist = np.linalg.norm(np.array(pos_s) - np.array(pos_other))
                angle = angle_from(pos_s, pos_other)
                branch = Branch(other, angle, dist)
                if branch not in solution.branches:
                    solution.branches.append(branch)

                if other not in visited:
                    visited.add(other)
                    queue.append(other)

            patterns.append(solution)

    return remap_node_ids(patterns)

def dfs_extract_patterns(G, positions):
    visited = set()
    patterns = []
    node_to_edges = preprocess_edges(G)

    def dfs(s):
        pos_s = positions[s]
        solution = LocationNode(s, pos_s)

        for u, v, k, data in node_to_edges[s]:
            other = v if u == s else u
            if other not in positions:
                continue
            pos_other = positions[other]

            dist = np.linalg.norm(np.array(pos_s) - np.array(pos_other))
            angle = angle_from(pos_s, pos_other)
            branch = Branch(other, angle, dist)
            if branch not in solution.branches:
                solution.branches.append(branch)

            if other not in visited:
                visited.add(other)
                dfs(other)

        patterns.append(solution)

    for start in G.nodes:
        if start not in visited and start in node_to_edges:
            visited.add(start)
            dfs(start)

    return remap_node_ids(patterns)


def summarize_patterns(patterns):
    node_count = len(patterns)
    branch_count = sum(len(p.branches) for p in patterns)
    return node_count, branch_count

def compare_bfs_dfs(G, positions):
    bfs_start_time = time.time()
    bfs_patterns = bfs_extract_patterns(G, positions)
    bfs_end_time = time.time()
    print(f"Finished BFS pattern extraction in {bfs_end_time - bfs_start_time}")

    dfs_start_time = time.time()
    dfs_patterns = dfs_extract_patterns(G, positions)
    dfs_end_time = time.time()
    print(f"Finished DFS pattern extraction in {dfs_end_time - dfs_start_time}")

    bfs_nodes, bfs_branches = summarize_patterns(bfs_patterns)
    dfs_nodes, dfs_branches = summarize_patterns(dfs_patterns)

    print("Comparison of BFS vs DFS pattern extraction")
    print("--------------------------------------------")
    print(f"BFS - Nodes: {bfs_nodes}, Branches: {bfs_branches}")
    print(f"DFS - Nodes: {dfs_nodes}, Branches: {dfs_branches}")
    
    if bfs_nodes != dfs_nodes or bfs_branches != dfs_branches:
        print("Difference detected between BFS and DFS results.")
    else:
        print("BFS and DFS results are consistent.")

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

if __name__ == '__ main __':
    # Load the Bandung graph
    path = os.path.join(os.getcwd(), "data", "bandung.graphml")
    G = ox.load_graphml(path)
    G = ox.project_graph(G)
    positions = {n: (data['x'], data['y']) for n, data in G.nodes(data=True)}

    # Run and print result
    compare_bfs_dfs(G, positions)
