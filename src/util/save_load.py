from classes import *
import json
import osmnx as ox

def load_gposition_from_graphml(filepath):
    G = ox.load_graphml(filepath)
    G = ox.project_graph(G)
    positions = {n: (data['x'], data['y']) for n, data in G.nodes(data=True)}
    return G, positions

def save_patterns_to_json(patterns, filename):
    """
    Serialize extracted patterns into a JSON file.

    Parameters:
    - patterns: list of LocationNode instances
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
    Deserialize a JSON file into a list of LocationNode instances.

    Parameters:
    - filename: path to the JSON file

    Returns:
    - List of LocationNode instances
    """
    with open(filename, 'r') as f:
        data = json.load(f)

    patterns = []
    for node_dict in data:
        node = LocationNode(node_dict['id'], tuple(node_dict['position']))
        node.branches = [Branch(branch['target'], branch['angle'], branch['distance']) for branch in node_dict['branches']]
        patterns.append(node)

    print(f"Loaded {len(patterns)} patterns from {filename}")
    return patterns

def save_numeric_lsystem_to_json(lsystem, filepath):
    """
    Save the filtered numeric L-system rules to a JSON file.
    Format: { rule_id: rule_string }
    """
    with open(filepath, "w") as f:
        json.dump(lsystem, f, indent=2)

def load_numeric_lsystem_from_json(filepath):
    """
    Load a numeric L-system from JSON file.
    Returns: dict[int, str]
    """
    with open(filepath, "r") as f:
        data = json.load(f)
        return {int(k): v for k, v in data.items()}
    
def save_referential_lsystem_to_json(split, lsystem, filepath):
    """
    Save the referential generalized L-system to a JSON file.
    Format:
    {
        "split": [nonref_count, ref_count],
        "rules": {
            rule_id: [pattern_id, rule_string],
            ...
        }
    }
    """
    output = {
        "split": list(split),
        "rules": {str(k): [v[0], v[1]] for k, v in lsystem.items()}
    }
    with open(filepath, "w") as f:
        json.dump(output, f, indent=2)

def load_referential_lsystem_from_json(filepath):
    """
    Load a referential L-system from JSON file.
    Returns: (tuple[int, int], dict[int, tuple[int, str]])
    """
    with open(filepath, "r") as f:
        data = json.load(f)
        split = tuple(data["split"])
        rules = {int(k): (v[0], v[1]) for k, v in data["rules"].items()}
        return split, rules