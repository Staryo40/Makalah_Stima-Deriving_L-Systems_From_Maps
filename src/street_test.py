import os
import matplotlib.pyplot as plt
import networkx as nx
import osmnx as ox
from shapely.geometry import LineString
import numpy as np

# Load graph
path = os.path.join(os.getcwd(), "data", "bandung.graphml")
G = ox.load_graphml(path)

# Calculate turn angles from geometry
def calculate_turn_angles(line):
    coords = np.array(line.coords)
    angles = []
    for i in range(1, len(coords) - 1):
        v1 = coords[i] - coords[i - 1]
        v2 = coords[i + 1] - coords[i]
        angle = np.degrees(np.arctan2(v2[1], v2[0]) - np.arctan2(v1[1], v1[0]))
        angle = (angle + 180) % 360 - 180  # Normalize to [-180, 180]
        angles.append(angle)
    return angles

# Reconstruct synthetic path with fixed end
def reconstruct_path_to_fixed_endpoint(start_point, end_point, angles, step_length):
    points = [np.array(start_point)]
    angle = 0

    # Generate all points except the final two
    for turn in angles[:-1]:  # Leave room for one final bend
        angle += turn
        rad = np.radians(angle)
        dx = step_length * np.cos(rad)
        dy = step_length * np.sin(rad)
        next_point = points[-1] + np.array([dx, dy])
        points.append(next_point)

    # Final two points: second-last bends toward fixed endpoint
    final = np.array(end_point)
    direction = final - points[-1]
    norm = np.linalg.norm(direction)

    if norm != 0:
        direction = direction / norm
        second_last = final - direction * step_length
        points[-1] = second_last
        points.append(final)
    else:
        # If too short, just append final
        points.append(final)

    return np.array(points)

# Build both original and reconstructed maps
original_lines = []
synthetic_lines = []

for u, v, k, data in G.edges(keys=True, data=True):
    if 'geometry' in data and isinstance(data['geometry'], LineString):
        line = data['geometry']
        coords = np.array(line.coords)
        if len(coords) < 2:
            continue
        avg_distance = line.length / (len(coords) - 1)
        angles = calculate_turn_angles(line)
        angles = [0] + angles  # Only prepend 0 to align start heading
        synthetic_coords = reconstruct_path_to_fixed_endpoint(coords[0], coords[-1], angles, avg_distance)
        original_lines.append(coords)
        synthetic_lines.append(synthetic_coords)

# Plot both maps
fig, axs = plt.subplots(1, 2, figsize=(16, 10))

# Original graph
for coords in original_lines:
    axs[0].plot(coords[:, 0], coords[:, 1], color='blue', linewidth=0.8)
axs[0].set_title("Original Bandung Road Network")
axs[0].set_aspect('equal')
axs[0].axis('off')

# Reconstructed graph
for coords in synthetic_lines:
    axs[1].plot(coords[:, 0], coords[:, 1], color='orange', linewidth=0.8)
axs[1].set_title("L-system Reconstructed Network (Fixed Endpoint)")
axs[1].set_aspect('equal')
axs[1].axis('off')

plt.tight_layout()
plt.show()
