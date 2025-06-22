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