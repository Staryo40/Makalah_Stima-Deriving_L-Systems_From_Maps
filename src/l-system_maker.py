from util import *
from classes import *

import turtle
import math
import re


def quantize_angle(angle, unit=15):
    return round(angle / unit) * unit

def quantize_distance(distance, unit=20):
    return max(1, round(distance / unit))

def create_raw_rules(nodes):
    rules = {}
    for node in nodes:
        rule = ''
        for branch in node.branches:
            angle = round(branch.angle)
            distance = round(branch.distance)

            # Add turning (positive = left, negative = right)
            if angle > 0:
                rule += f'+{angle}'
            elif angle < 0:
                rule += f'-{abs(angle)}'

            # Add forward movement
            rule += f'F{distance}'

            # Call to the target node
            rule += f'[X{branch.target_id}]'

        rules[node.id] = rule
    return rules

def filter_rules(rules):
    # Step 1: Identify and remove empty rules
    non_empty_rules = {rid: rule for rid, rule in rules.items() if rule.strip()}

    # Step 2: Get the set of valid referenced rule IDs
    valid_ids = set(non_empty_rules.keys())

    # Step 3: Clean each rule by removing [Xn] where n not in valid_ids
    cleaned_rules = {}
    pattern = re.compile(r'\[X(\d+)\]')

    for rid, rule in non_empty_rules.items():
        cleaned_rule = ''
        i = 0
        while i < len(rule):
            match = pattern.match(rule, i)
            if match:
                target_id = int(match.group(1))
                if target_id in valid_ids:
                    cleaned_rule += match.group(0)  # keep [Xn]
                # else: skip it
                i = match.end()
            else:
                cleaned_rule += rule[i]
                i += 1
        cleaned_rules[rid] = cleaned_rule

    return cleaned_rules


data = os.path.join(os.getcwd(), "data", "bandung.json")
patterns = load_patterns_from_json(data)

raw_rules = create_raw_rules(patterns)
filtered_rules = filter_rules(raw_rules)

print(len(filtered_rules))
# for i, (id, rule) in enumerate(filtered_rules.items()):
#     if i < 10:
#         print(f"{id}: {rule}")





    