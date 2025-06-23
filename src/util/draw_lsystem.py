import turtle
from analysis import *

def interpret_numeric_rule(rules, visited, id_to_pos, start_id, rule, ax, depth=0):
    if start_id not in id_to_pos:
        return
    x, y = id_to_pos[start_id]
    angle = 0
    stack = []

    i = 0
    while i < len(rule):
        if rule[i] in '+-':
            sign = -1 if rule[i] == '-' else 1
            i += 1
            num = ''
            while i < len(rule) and rule[i].isdigit():
                num += rule[i]
                i += 1
            angle += sign * int(num)
        elif rule[i] == 'F':
            i += 1
            num = ''
            while i < len(rule) and rule[i].isdigit():
                num += rule[i]
                i += 1
            dist = int(num)
            rad = math.radians(angle)
            new_x = x + dist * math.cos(rad)
            new_y = y + dist * math.sin(rad)
            ax.plot([x, new_x], [y, new_y], color='blue', linewidth=0.5)
            x, y = new_x, new_y
        elif rule[i] == '[':
            stack.append((x, y, angle))
            i += 1
        elif rule[i] == ']':
            x, y, angle = stack.pop()
            i += 1
        elif rule[i] == 'X':
            i += 1
            num = ''
            while i < len(rule) and rule[i].isdigit():
                num += rule[i]
                i += 1
            ref_id = int(num)
            if ref_id in rules and ref_id not in visited:
                visited.add(ref_id)
                interpret_numeric_rule(rules, visited, id_to_pos, ref_id, rules[ref_id], ax, depth + 1)
                visited.remove(ref_id)
        else:
            i += 1

def draw_numeric_lsystem(rules, patterns):
    id_to_pos = {p.id: p.position for p in patterns}
    visited = set()
    fig, ax = plt.subplots()

    for id, rule in rules.items():
        interpret_numeric_rule(rules, visited, id_to_pos, id, rule, ax)

    ax.set_aspect('equal')
    ax.set_title("Numeric L-System Visualization")
    plt.show()

def interpret_referential_virtual(gen_rules, visited, rule, ax, x=0, y=0, angle=0, angle_unit=15, dist_unit=50, depth=0):
    stack = []
    i = 0

    while i < len(rule):
        if rule[i] in '+-':
            sign = -1 if rule[i] == '-' else 1
            i += 1
            angle += sign * angle_unit
        elif rule[i] == 'F':
            i += 1
            rad = math.radians(angle)
            new_x = x + dist_unit * math.cos(rad)
            new_y = y + dist_unit * math.sin(rad)
            ax.plot([x, new_x], [y, new_y], color='green', linewidth=0.5)
            x, y = new_x, new_y
        elif rule[i] == '[':
            stack.append((x, y, angle))
            i += 1
        elif rule[i] == ']':
            x, y, angle = stack.pop()
            i += 1
        elif rule[i] == 'X':
            i += 1
            num = ''
            while i < len(rule) and rule[i].isdigit():
                num += rule[i]
                i += 1
            ref_id = int(num)
            if ref_id in gen_rules and ref_id not in visited:
                visited.add(ref_id)
                pattern_id, sub_rule = gen_rules[ref_id]
                x, y = interpret_referential_virtual(
                    gen_rules, visited, sub_rule, ax,
                    x, y, angle, angle_unit, dist_unit, depth + 1
                )
                visited.remove(ref_id)
        else:
            i += 1

    return x, y  # Return final position to support nested calls

def draw_virtual_lsystem(gen_rules, split, angle_unit=15, dist_unit=50):
    visited = set()
    fig, ax = plt.subplots()

    start_index = split[0] + 1
    for id in sorted(gen_rules.keys()):
        if id >= start_index:
            pattern_id, rule = gen_rules[id]
            interpret_referential_virtual(gen_rules, visited, rule, ax, 0, 0, 0, angle_unit, dist_unit)

    ax.set_aspect('equal')
    ax.set_title("Virtual Referential L-System")
    plt.show()

def draw_pattern_and_numeric_lsystem(patterns, rules):
    id_to_pos = {p.id: p.position for p in patterns}
    visited = set()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

    # --- Left: Raw Patterns ---
    for pattern in patterns:
        origin = np.array(pattern.position)

        for branch in pattern.branches:
            angle_rad = np.radians(branch.angle)
            dx = branch.distance * np.cos(angle_rad)
            dy = branch.distance * np.sin(angle_rad)
            ax1.arrow(origin[0], origin[1], dx, dy,
                      head_width=0.5, head_length=0.8,
                      length_includes_head=True, fc='orange', ec='orange')

    ax1.set_aspect('equal')
    ax1.grid(True)
    ax1.set_title("Raw GraphML Patterns from Nodes")

    # --- Right: Numeric L-System ---
    for id, rule in rules.items():
        interpret_numeric_rule(rules, visited, id_to_pos, id, rule, ax2)

    ax2.set_aspect('equal')
    ax2.set_title("Numeric L-System Visualization")

    plt.tight_layout()
    plt.show()

if __name__ == '__ main __':
    data = os.path.join(os.getcwd(), "data", "bandung.json")
    patterns = load_patterns_from_json(data)

    raw_rules = create_raw_rules(patterns)
    filtered_rules = filter_rules(raw_rules)
    split, gen_rules = generalize_rule(filtered_rules, original_id=True, split=True)

    # draw_numeric_lsystem(filtered_rules, patterns)
    draw_virtual_lsystem(gen_rules, split)