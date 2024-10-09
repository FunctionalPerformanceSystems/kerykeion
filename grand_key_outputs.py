from kerykeion import NatalAspects
import pandas as pd

def aspect_table(astro_subject):
    name=NatalAspects(astro_subject)
    aspect=name.relevant_aspects
    df=pd.DataFrame(aspect)

    columns_to_drop = ['p1_abs_pos', 'p2_abs_pos', 'aspect_degrees', 'color', 'aid', 'diff', 'p1', 'p2']
    df.drop(columns=columns_to_drop, inplace=True)
    
    df.reset_index(drop=True, inplace=True)
    df.index += 1
    return df


def replace_with_unicode(array):
    replacements = {
        'Sun': '☉',
        'Moon': '☽',
        'Mercury': '☿',
        'Venus': '♀',
        'Mars': '♂',
        'Jupiter': '♃',
        'Saturn': '♄',
        'Uranus': '♅',
        'Neptune': '♆',
        'Pluto': '♇',
        'Ari': '♈︎',
        'Tau': '♉︎',
        'Gem': '♊︎',
        'Can': '♋︎',
        'Leo': '♌︎',
        'Vir': '♍︎',
        'Lib': '♎︎',
        'Sco': '♏︎',
        'Sag': '♐︎',
        'Cap': '♑︎',
        'Aqu': '♒︎',
        'Pis': '♓︎',
        'sextile': '|✶',
        'conjunction': '|☌',
        'trine': '|△',
        'square': '|□',
        'opposition': '|☍'
    }

    replaced_array = []
    for subarray in array:
        replaced_subarray = [replacements.get(item, item) for item in subarray]
        replaced_array.append(replaced_subarray)
    
    return replaced_array


def symbol_output(input_array):
    unicode_array = replace_with_unicode(input_array)
    for subarray in unicode_array:
        print(' '.join(subarray))


def text_output(input_array):
    output_lines = []
    for subarray in input_array:
        formatted_subarray = []
        for item in subarray:
            if item in ['conjunction', 'opposition', 'trine', 'sextile', 'square']:
                formatted_subarray.append('|' + item)
            else:
                formatted_subarray.append(item)    
        output_lines.append(' '.join(formatted_subarray))

    return '\n'.join(output_lines)

'''
# Function to build a tree structure from key_array
def build_tree(key_array):
    tree = {}
    
    for entry in key_array:
        # Extract the main aspect and the relationship
        main_aspect = f"{entry[0]} {entry[1]} {entry[2]}"
        relationship = f"{entry[3]} {' '.join(entry[4:])}"
        
        if main_aspect not in tree:
            tree[main_aspect] = []
        
        tree[main_aspect].append(relationship)
    
    return tree

def build_tree(key_array):
    tree = {}

    for entry in key_array:
        main_aspect = f"{entry[0]} {entry[1]} {entry[2]}"

        i = 3
        while i < len(entry):
            relationship = f"{entry[i]} {' '.join(entry[i+1:i+4])}"
            i += 4
            if i < len(entry):
                relationship += f"{' '.join(entry[i:i+3])}"
                i += 3

            if main_aspect not in tree:
                tree[main_aspect] = []

            tree[main_aspect].append(relationship)
'''

def build_tree(key_array):
    tree = {}
    aspects = ['conjunction', 'opposition', 'trine', 'sextile', 'square']
    for entry in key_array:
        main_aspect = f"{entry[0]} {entry[1]} {entry[2]}"

        i = 3
        while i < len(entry):
            if entry[i] in aspects:
                relationship = entry[i]
                i += 1
                while i < len(entry) and entry[i] not in aspects:
                    relationship += f" {entry[i]}"
                    i += 1

                if main_aspect not in tree:
                    tree[main_aspect] = []

                tree[main_aspect].append(relationship)
            else:
                i += 1
    return tree

def build_tree_string(tree, indent="", last=True):
    items = list(tree.items())
    count = len(items)
    output_lines = []
    
    for index, (key, value) in enumerate(items):
        connector = "└── " if index == count - 1 else "├── "
        #output_lines.append(f"{indent}{connector}{key}")
        output_lines.append(f"{key}")
        #new_indent = indent + ("    " if index == count - 1 else "│   ")
        new_indent = indent
        
        for aspect_index, aspect in enumerate(value):
            aspect_connector = "└── " if aspect_index == len(value) - 1 else "├── "
            output_lines.append(f"{new_indent}{aspect_connector}{aspect}")
    
    return "\n".join(output_lines)