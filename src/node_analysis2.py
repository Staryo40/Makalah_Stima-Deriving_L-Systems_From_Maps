from util import *
import math
from scipy.spatial import KDTree

def offset_position(position, angle_deg, distance):
    angle_rad = math.radians(angle_deg)
    dx = distance * math.cos(angle_rad)
    dy = distance * math.sin(angle_rad)
    return (position[0] + dx, position[1] + dy)

bandung = os.path.join(os.getcwd(), "data", "bandung.json")
patterns = load_patterns_from_json(bandung)
all_positions = [p.position for p in patterns]
kdtree = KDTree(all_positions)

# Count branch ends that match other node positions
branch_count = 0
for p in patterns:
    branch_count += len(p.branches)

connected_branches = 0
connected_branches = 0
for pattern in patterns:
    for branch in pattern.branches:
        end_pos = offset_position(pattern.position, branch.angle, branch.distance)
        # Query nearest node within 0.01 tolerance
        indices = kdtree.query_ball_point(end_pos, r=0.01)
        if indices:
            connected_branches += 1

print(f"Number of branch: {branch_count}")
print(f"Number of branch ends that match other node positions: {connected_branches}")
