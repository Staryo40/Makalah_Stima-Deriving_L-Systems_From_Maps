import math

# Branch data structure
class Branch:
    def __init__(self, target_id, angle, distance):
        self.target_id = target_id
        self.angle = angle
        self.distance = distance
    
    def __eq__(self, other):
        return isinstance(other, Branch) and \
               math.isclose(self.angle, other.angle, abs_tol=1e-6) and \
               math.isclose(self.distance, other.distance, abs_tol=1e-6)
    
    def __hash__(self):
        return hash((
            round(self.angle, 6),
            round(self.distance, 6)
        ))
    
    def __str__(self):
        return f"→ Target ID: {self.target_id}, Angle: {self.angle:.2f}, Distance: {self.distance:.2f}"

# Solution node
class LocationNode:
    def __init__(self, id, position):
        self.id = id
        self.position = position
        self.branches = []
    
    def __str__(self):
        result = f"Node ID: {self.id}, Position: {self.position}\n"
        if self.branches:
            result += "  Branches:\n"
            length = len(self.branches)
            for i, b in enumerate(self.branches):
                line = f"    → Target ID: {b.target_id}, Angle: {b.angle:.2f}, Distance: {b.distance:.2f}"
                result += line + ("\n" if i < length - 1 else "")
        else:
            result += "  (No branches)"
        
        return result