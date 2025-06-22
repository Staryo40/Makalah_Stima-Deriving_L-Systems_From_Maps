from classes import *
import json

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
            'id': pattern.id,
            'position': list(pattern.position),
            'branches': [
                {'target': branch.target_id, 'angle': branch.angle, 'distance': branch.distance}
                for branch in pattern.branches
            ]
        }
        serializable_patterns.append(node_dict)

    with open(filename, 'w') as f:
        json.dump(serializable_patterns, f, indent=2)

    print(f"Saved {len(patterns)} patterns to {filename}")

def load_patterns_from_json(filename):
    """
    Deserialize a JSON file into a list of SolutionNode instances.

    Parameters:
    - filename: path to the JSON file

    Returns:
    - List of SolutionNode instances
    """
    with open(filename, 'r') as f:
        data = json.load(f)

    patterns = []
    for node_dict in data:
        node = SolutionNode(node_dict['id'], tuple(node_dict['position']))
        node.branches = [Branch(branch['target'], branch['angle'], branch['distance']) for branch in node_dict['branches']]
        patterns.append(node)

    print(f"Loaded {len(patterns)} patterns from {filename}")
    return patterns