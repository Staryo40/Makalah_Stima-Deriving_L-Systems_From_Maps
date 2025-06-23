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

            # (positive = left, negative = right)
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
    # Remove empty rules
    non_empty_rules = {rid: rule for rid, rule in rules.items() if rule.strip()}

    # Valid referenced rule IDs
    valid_ids = set(non_empty_rules.keys())

    # Clean each rule by removing [Xn] where n not in valid_ids
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
                    cleaned_rule += match.group(0)
                i = match.end()
            else:
                cleaned_rule += rule[i]
                i += 1
        cleaned_rules[rid] = cleaned_rule

    return cleaned_rules

def remove_rule_numerics(rules):
    referential_rules = {}
    
    for id, rule in rules.items():
        referential_rules[id] = re.sub(r'\+\d+', '+', rule)
        referential_rules[id] = re.sub(r'\-\d+', '-', referential_rules[id])
        referential_rules[id] = re.sub(r'F\d+', 'F', referential_rules[id])
    
    return referential_rules

def generalize_rule(rules, original_id=False, split=False):
    referential_rules = remove_rule_numerics(rules)
    raw_non_referential = {}
    referential = {}

    # Split between referential (X) and non-referential (no X)
    for id, rule in referential_rules.items():
        if re.search(r'X\d+', rule):
            referential[id] = rule
        else:
            raw_non_referential[id] = rule
    
    # Make mapping of non-referential to new id starting from 1
    shape_to_new = {}
    i = 1
    for id, nonref_rule in raw_non_referential.items():
        if nonref_rule not in shape_to_new:
            shape_to_new[nonref_rule] = i
            i += 1
    
    # Mapping old to new id
    old_new_nonref = {}
    for id, nonref_rule in raw_non_referential.items():
        old_new_nonref[id] = shape_to_new[nonref_rule]
    
    # Flipping shape_to_new
    new_to_shape = {v: k for k, v in shape_to_new.items()} # starts at 1 index

    # Referential refered by other referentials
    referentials = []
    for id, ref_rule in referential.items():
        refer_ids = [int(x) for x in re.findall(r'X(\d+)', ref_rule)]
        for id in refer_ids:
            if id in referential and id not in referentials:
                referentials.append(id)

    # Append referential to final maps and change the non-referential to the new mapping
    index = len(new_to_shape) + 1
    ref_start = index
    referential_to_new = {}
    for id, ref_rule in referential.items():
        new_to_shape[index] = re.sub(r'X(\d+)', lambda m: f"X{old_new_nonref.get(int(m.group(1)), m.group(1))}", ref_rule)
        referential_to_new[id] = index
        index += 1

    # Change the referential to new referentials
    for id, rule in new_to_shape.items():
        if id >= ref_start:
            new_to_shape[id] = re.sub(r'X(\d+)', lambda m: f"X{referential_to_new[int(m.group(1))]}" if int(m.group(1)) in referential_to_new else m.group(0), rule)

    if original_id:
        new_to_referential = {v: k for k, v in referential_to_new.items()}
        for id, rule in new_to_shape.items():
            if id >= ref_start:
                new_to_shape[id] = (new_to_referential[id], rule)
            else:
                new_to_shape[id] = (-1, rule) 
                
    if split:
        return (ref_start-1, len(new_to_shape) - ref_start + 1), new_to_shape
    else:
        return new_to_shape

if __name__ == '__ main __':
    data = os.path.join(os.getcwd(), "data", "bandung.json")
    patterns = load_patterns_from_json(data)

    raw_rules = create_raw_rules(patterns)
    filtered_rules = filter_rules(raw_rules)
    split, gen_rules = generalize_rule(filtered_rules, True)

    print(len(filtered_rules))
    for i, (id, rule) in enumerate(filtered_rules.items()):
        if i < 10:
            print(f"{id}: {rule}")

    print("Non reference: " + str(split[0]))
    print("Reference: " + str(split[1]))
    print(len(gen_rules))
    for i, (id, rule) in enumerate(gen_rules.items()):
        if i < 10:
            print(f"{id}: {rule}")