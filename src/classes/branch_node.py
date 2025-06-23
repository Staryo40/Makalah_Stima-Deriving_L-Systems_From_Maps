import math

# Branch data structure
class Branch:
    def __init__(self, target_id, angle, distance):
        self.target_id = target_id
        self.angle = angle
        self.distance = distance

    def __repr__(self):
        return f"Branch(angle={self.angle:.2f}, distance={self.distance:.2f})"
    
    def __eq__(self, other):
        return isinstance(other, Branch) and \
               math.isclose(self.angle, other.angle, abs_tol=1e-6) and \
               math.isclose(self.distance, other.distance, abs_tol=1e-6)
    
    def __hash__(self):
        return hash((
            round(self.angle, 6),
            round(self.distance, 6)
        ))
    
    def print(self):
        print(f"→ Target ID: {self.target_id}, Angle: {self.angle:.2f}, Distance: {self.distance:.2f}")

# Solution node
class LocationNode:
    def __init__(self, id, position):
        self.id = id
        self.position = position
        self.branches = []

    def __repr__(self):
        return f"SolutionNode(position={self.position}, branches={self.branches})"
    
    def print(self):
        print(f"Node ID: {self.id}, Position: {self.position}")
        if self.branches:
            print("  Branches:")
            for b in self.branches:
                print(f"    → Target ID: {b.target_id}, Angle: {b.angle:.2f}, Distance: {b.distance:.2f}")
        else:
            print("  (No branches)")