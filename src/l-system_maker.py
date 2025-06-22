from util import *
from classes import *

import turtle
import math

def draw_lsystem(instructions, step=10, angle=30):
    stack = []

    for cmd in instructions:
        if cmd == 'F':
            turtle.forward(step)
        elif cmd == '+':
            turtle.left(angle)
        elif cmd == '-':
            turtle.right(angle)
        elif cmd == '[':
            # Push state: position and heading
            pos = turtle.position()
            heading = turtle.heading()
            stack.append((pos, heading))
        elif cmd == ']':
            # Pop state
            pos, heading = stack.pop()
            turtle.penup()
            turtle.setposition(pos)
            turtle.setheading(heading)
            turtle.pendown()

def simplify_branch_to_lsystem(branch, angle_step=30):
    """
    Converts a branch into a simplified L-system string.
    """
    commands = []

    angle = branch.angle
    quantized_angle = round(angle / angle_step) * angle_step

    # Determine direction
    if quantized_angle > 0:
        commands.append('+' * (abs(quantized_angle) // angle_step))
    elif quantized_angle < 0:
        commands.append('-' * (abs(quantized_angle) // angle_step))

    # Move forward (normalize distance to one F per threshold)
    steps = max(1, round(branch.distance / 50))  # adjust 50 for your desired scale
    commands.append('F' * steps)

    return ''.join(commands)

def convert_nodes_to_lsystem(nodes, angle_step=30):
    """
    Generates a basic L-system axiom and rule set from SolutionNodes.
    """
    axiom = "X"
    rules = {
        "X": ""
    }

    for idx, node in enumerate(nodes):
        if not node.branches:
            continue
        
        rule = ""
        for branch in node.branches:
            segment = simplify_branch_to_lsystem(branch, angle_step)
            rule += f"[{segment}X]"  # Recursive branching
        rules["X"] = rule
        break  # Only use the first branching node for simplicity

    return axiom, rules

data = os.path.join(os.getcwd(), "data", "bandung.json")

patterns = load_patterns_from_json(data)
# plot_patterns(patterns, show_labels=False)
# plt.show()

axiom, rules = convert_nodes_to_lsystem(patterns)
print(axiom)
print(rules)

# turtle.speed(0)          
# turtle.left(90)        
# turtle.penup()
# turtle.goto(0, -200)   
# turtle.pendown()

# lsystem_string = '[+FFFFFX][---FFFFX][---FFFFX][+FFFFFX][FX][FX]'
# draw_lsystem(lsystem_string, step=10, angle=30)
# turtle.done()