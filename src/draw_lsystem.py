import turtle
from analysis import *

data = os.path.join(os.getcwd(), "data", "bandung.json")
patterns = load_patterns_from_json(data)

raw_rules = create_raw_rules(patterns)
filtered_rules = filter_rules(raw_rules)
split, gen_rules = generalize_rule(filtered_rules, original_id=True, split=True)

t = turtle.Turtle()
t.penup()
t.goto(0, 0)  # Center of screen
t.pendown()

t.forward(100)
t.left(90)
t.forward(100)

turtle.done()