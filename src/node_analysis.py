import json, os
import matplotlib.pyplot as plt
from collections import Counter

# Load bandung.json
bandung = os.path.join(os.getcwd(), "data", "bandung.json")
with open(bandung, "r") as f:
    data = json.load(f)

# Collect rounded angles and distances
rounded_angles = []
rounded_distances = []

for node in data:
    for branch in node.get("branches", []):
        rounded_angles.append(round(branch["angle"]))
        rounded_distances.append(round(branch["distance"]))

print("Angle Stats:")
print(f"  Min: {min(rounded_angles)}°")
print(f"  Max: {max(rounded_angles)}°")
print(f"  Avg: {sum(rounded_angles)/len(rounded_angles):.2f}°")

print("Distance Stats:")
print(f"  Min: {min(rounded_distances)} units")
print(f"  Max: {max(rounded_distances)} units")
print(f"  Avg: {sum(rounded_distances)/len(rounded_distances):.2f} units")

# Count occurrences
angle_counts = Counter(rounded_angles)
distance_counts = Counter(rounded_distances)

# Plot distributions
plt.figure(figsize=(14, 6))

# Angle distribution
plt.subplot(1, 2, 1)
plt.bar(angle_counts.keys(), angle_counts.values(), width=1)
plt.title("Rounded Angle Distribution")
plt.xlabel("Angle (degrees)")
plt.ylabel("Frequency")

# Distance distribution
plt.subplot(1, 2, 2)
plt.bar(distance_counts.keys(), distance_counts.values(), width=1)
plt.title("Rounded Distance Distribution")
plt.xlabel("Distance")
plt.ylabel("Frequency")

plt.tight_layout()
plt.show()
