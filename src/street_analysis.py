import networkx as nx
import os, sys, math
import osmnx as ox
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Point, LineString
from shapely.plotting import plot_line, plot_points
from descartes import PolygonPatch

def encode_node(node, G):
    degree = G.degree(node)
    if degree == 1:
        return "T"  # Terminal
    elif degree == 2:
        return "F"  # Forward (straight)
    else:
        return "B"  # Branching
    
def calculate_angle(p1, p2):
    return math.degrees(math.atan2(p2[1] - p1[1], p2[0] - p1[0]))

def calculate_turn_angles(line):
    coords = list(line.coords)
    angles = []

    for i in range(1, len(coords) - 1):
        p0 = np.array(coords[i - 1])
        p1 = np.array(coords[i])
        p2 = np.array(coords[i + 1])

        v1 = p1 - p0
        v2 = p2 - p1

        angle_rad = np.arctan2(v2[1], v2[0]) - np.arctan2(v1[1], v1[0])
        angle_deg = np.degrees(angle_rad)

        # Normalize angle to [-180, 180]
        angle_deg = (angle_deg + 180) % 360 - 180
        angles.append(angle_deg)

    return angles


def reconstruct_path(start_point, angles_deg, step_length):
    points = [np.array(start_point)]
    
    # Initial heading: from the first segment
    if len(angles_deg) < 2:
        return np.array(points)  # not enough data

    current_heading_rad = None

    # Use the first angle as absolute heading
    current_heading_rad = np.deg2rad(angles_deg[0])

    for turn_deg in angles_deg[1:]:
        # Apply turn
        current_heading_rad += np.deg2rad(turn_deg)
        
        # Move forward
        dx = step_length * np.cos(current_heading_rad)
        dy = step_length * np.sin(current_heading_rad)
        
        new_point = points[-1] + np.array([dx, dy])
        points.append(new_point)

    return np.array(points)


def plot_comparison(line):
    coords = np.array(line.coords)
    num_vertices = len(coords)
    avg_distance = line.length / (num_vertices - 1 if num_vertices > 1 else 1)

    # Get angles
    angles = calculate_turn_angles(line)

    # Get the initial heading from the first two points
    dx, dy = coords[1] - coords[0]
    initial_heading = np.rad2deg(np.arctan2(dy, dx))

    # Prepend it as the first absolute heading
    angles = [initial_heading] + angles + [0]  # last 0 = go straight at end

    # Reconstruct synthetic path
    synthetic_points = reconstruct_path(coords[0], angles, avg_distance)

    # Plotting
    fig, axs = plt.subplots(1, 2, figsize=(14, 6))

    axs[0].plot(coords[:, 0], coords[:, 1], color='blue', linewidth=3)
    axs[0].plot(coords[:, 0], coords[:, 1], 'o', color='gray')
    axs[0].set_title("Original LineString")
    axs[0].set_aspect('equal')
    axs[0].grid(True)

    axs[1].plot(synthetic_points[:, 0], synthetic_points[:, 1], color='orange', linewidth=3)
    axs[1].plot(synthetic_points[:, 0], synthetic_points[:, 1], 'o', color='gray')
    axs[1].set_title("Reconstructed L-System")
    axs[1].set_aspect('equal')
    axs[1].grid(True)

    plt.tight_layout()
    plt.show()

path = os.path.join(os.getcwd(), "data", "bandung.graphml")
G = ox.load_graphml(path)  

node = list(G.nodes)[0]
print(G.nodes[node])
# u1, v1, key1, data1 = list(G.edges(keys=True, data=True))[1]
found_data = None
length = 0
for u, v, key, data in G.edges(keys=True, data=True):
    if 'geometry' in data and isinstance(data['geometry'], LineString):
        line_geometry = data['geometry']
        num_vertices = len(line_geometry.coords)

        # Check if the number of vertices is greater than 5
        # if (num_vertices > max):
        #     max = num_vertices
        if num_vertices > 20:
            found_u = u
            found_v = v
            found_key = key
            found_data = data
            length = num_vertices
            print(f"Found an edge with vertices more than threshold")
            print(f"  Edge: ({found_u}, {found_v}, {found_key})")
            if 'name' in data:
                print(f"  Name: {found_data['name']}")
            print(f"  Linestring: {found_data['geometry']}")
            print(f"  Number of Vertices: {num_vertices}")
            break 

# if found_data == None:
#     print(f"Max: {length}")
#     print("No edge fit the bill")
#     sys.exit()

# line = found_data['geometry']
# plot_comparison(line)
# avg_distance = line.length / (1 if num_vertices <= 1 else (num_vertices - 1))

# fig, ax = plt.subplots(1, 1, figsize=(8, 6))

# x, y = line.xy
# ax.plot(x, y, color='blue', linewidth=3, solid_capstyle='round', zorder=1)

# # You can also add markers for the start and end points for clarity
# ax.plot(x[0], y[0], 'o', color='green', markersize=8, label='Start Point')
# if len(x) > 2: # Check if there are middle points
#     ax.plot(x[1:-1], y[1:-1], 'o', color='purple', markersize=6, label='Intermediate Points') # Plot middle points
# ax.plot(x[-1], y[-1], 'o', color='red', markersize=8, label='End Point')

# ax.set_title("Plot of the LineString")
# ax.set_xlabel("Longitude")
# ax.set_ylabel("Latitude")

# ax.set_aspect('equal', adjustable='box')

# # Add a legend
# ax.legend()
# ax.grid(True, linestyle='--', alpha=0.7)
# plt.show()

# INITIAL STUDY OF GEOMETRY
# if 'geometry' in data1:
#     print("\nInternal dictionary of data1['geometry']:")
#     print(f"Points: {data1['geometry']}")
#     print(f"Coords: {data1['geometry'].coords}") # Not needed
#     print(f"Length: {data1['geometry'].length}") # Euclidean distance over segments
#     print(f"Simple: {data1['geometry'].is_simple}")
#     print(f"Valid: {data1['geometry'].is_valid}")
#     print(f"Bounds: {data1['geometry'].bounds}") # Maybe (minx, miny, maxx, maxy)

# if 'geometry' in data1 and isinstance(data1['geometry'], LineString):
#     linestring_geometry = data1['geometry']

#     first_point_coords = linestring_geometry.coords[0]
#     last_point_coords = linestring_geometry.coords[-1]
#     first_shapely_point = Point(first_point_coords)
#     last_shapely_point = Point(last_point_coords)

#     print(f"\nSearching for nodes intersecting with the LineString's start point ({first_shapely_point.x}, {first_shapely_point.y})...")
#     found_nodes_for_start = []
#     found_nodes_for_end = []

#     for node_id, node_data in G.nodes(data=True):
#         if node_data['x'] == first_shapely_point.x and node_data['y'] == first_shapely_point.y:
#             found_nodes_for_start.append(node_id)
#         elif node_data['x'] == last_shapely_point.x and node_data['y'] == last_shapely_point.y:
#             found_nodes_for_end.append(node_id)

#     print("\nNodes intersecting with the first point of the LineString:")
#     if found_nodes_for_start:
#         for node_id in found_nodes_for_start:
#             print(f"- Node ID: {node_id}, Node Data: {G.nodes[node_id]}")
#     else:
#         print("No nodes found intersecting with the first point.")

#     print("\nNodes intersecting with the last point of the LineString:")
#     if found_nodes_for_end:
#         for node_id in found_nodes_for_end:
#             print(f"- Node ID: {node_id}, Node Data: {G.nodes[node_id]}")
#     else:
#         print("No nodes found intersecting with the last point.")

# else:
#     print("The 'geometry' key in data1 is either missing or not a Shapely LineString object.")
#     print("Cannot proceed with node intersection search.")