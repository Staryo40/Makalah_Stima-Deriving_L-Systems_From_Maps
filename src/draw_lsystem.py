import turtle
from analysis import *

def interpret_rule(rules, visited, id_to_pos, start_id, rule, ax, depth=0):
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
            ax.plot([x, new_x], [y, new_y], color='black', linewidth=0.5)
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
                interpret_rule(rules, visited, id_to_pos, ref_id, rules[ref_id], ax, depth + 1)
                visited.remove(ref_id)
        else:
            i += 1

def draw_numeric_lsystem(rules, patterns):
    id_to_pos = {p.id: p.position for p in patterns}
    visited = set()
    fig, ax = plt.subplots()

    for id, rule in rules.items():
        interpret_rule(rules, visited, id_to_pos, id, rule, ax)

    ax.set_aspect('equal')
    ax.set_title("Numeric L-System Visualization")
    plt.show()

data = os.path.join(os.getcwd(), "data", "bandung.json")
patterns = load_patterns_from_json(data)

raw_rules = create_raw_rules(patterns)
filtered_rules = filter_rules(raw_rules)
split, gen_rules = generalize_rule(filtered_rules, original_id=True, split=True)

draw_numeric_lsystem(filtered_rules, patterns)