from kerykeion import NatalAspects
from kerykeion.aspects.aspects_utils import get_active_points_list, get_active_points_list_ruler
from kerykeion.settings.kerykeion_settings import get_settings
from kerykeion.kr_types.kr_literals import Sign
from collections import OrderedDict
from itertools import chain


sign_num = {index: value for index, value in enumerate(Sign.__args__)}


def replace_numbers(lst):
    return [sign_num[num] if num in sign_num else num for num in lst]


def points_and_rulers(astro_subject):
    active_points_list = get_active_points_list(astro_subject, get_settings())
    ruler = get_active_points_list_ruler(astro_subject, get_settings())
    rulership = [[item1['name'], item2] for item1, item2 in zip(active_points_list, ruler)]
    rulership = [[planet, replace_numbers(numbers)] for planet, numbers in rulership]
    return [active_points_list, ruler, rulership]


def sign_to_planet(sign, astro_subject):
    result = []
    for index, (planet, sign_list) in enumerate(points_and_rulers(astro_subject)[2]):
        if sign in sign_list:
            return [index,planet]
    return None


def find_house_by_sign(houses, target_sign):
    for index,house in enumerate(houses,start = 1):
        if house['sign'] == target_sign:
            return [index,house['name']]
    return None


def planet_rulership(planet_name, astro_subject):
    for item in points_and_rulers(astro_subject)[2]:
        if item[0] == planet_name:
            return replace_numbers(item[1])
    return []


def get_house_from_sign(sign_name, astro_subject):
    for house in astro_subject.houses_list:
        if house['sign'] == sign_name:
            return house
        

def factor(object, astro_subject):
    planet_overview=object
    m_rulling = planet_rulership(planet_overview['name'], astro_subject)
    h_rulling = [get_house_from_sign(sign, astro_subject)['name'] for sign in m_rulling]
    factors=[planet_overview['name'], planet_overview['sign'], planet_overview['house'], h_rulling] # removes m_rulling
    factors = list(chain.from_iterable(item if isinstance(item, list) else [item] for item in factors))
    factors =  list(OrderedDict.fromkeys(factors))
    return factors


def get_planet_object(planet_name, planet_objects):
    # Convert the planet name to lowercase for case-insensitive comparison
    planet_name_lower = planet_name.lower()

    # Search for the planet in the list
    for planet_object in planet_objects:
        # Extract the name attribute from the planet_object and convert to lowercase
        current_planet_name = getattr(planet_object, 'name').lower()

        # Check if the current planet name matches the target planet name
        if current_planet_name == planet_name_lower:
            return planet_object

    # If the planet is not found, return None or handle the case accordingly
    #return None


def interactions(original_array, element, planet_objects):
    element_to_check = element
    result_array = []

    for i in range(1, len(original_array)):
        if element_to_check in original_array[i]:
            result_array.extend(original_array[i - 1])

    #Check the first subarray after the second
    if element_to_check in original_array[0]:
        result_array.extend(original_array[1])

    if len(result_array)!=0:
        result_array.insert(0,element_to_check)
        result_array.insert(1,get_planet_object(element_to_check, planet_objects)['sign'])
        result_array.insert(2,get_planet_object(element_to_check, planet_objects)['house'])
    result_array = list(dict.fromkeys(result_array))
    return result_array


def planet_aspects(astro_subject, name):
    subj = NatalAspects(astro_subject)
    aspects = subj.relevant_aspects

    interacting_factors = []

    for aspect in aspects:
        # Check if the aspect involves the specified planet (name)
        if name in [aspect.get('p1_name', ''), aspect.get('p2_name', '')]:
            # Check if the aspect involves unwanted factors (ASC, MC, Mean_Node, True_Node)
            unwanted_factors = {'ASC', 'MC', 'Mean_Node', 'True_Node'}
            if not any(factor in unwanted_factors for factor in [aspect.get('p1_name', ''), aspect.get('p2_name', '')]):
                # Add relevant aspects to the result
                if aspect.get('p1_name') == name:
                    planet_name = aspect.get('p2_name', '')
                    planet_sign = aspect.get('p2_sign', '')
                    planet_house = aspect.get('p2_house', '')
                    aspect_type = aspect.get('aspect', '')
                else:
                    planet_name = aspect.get('p1_name', '')
                    planet_sign = aspect.get('p1_sign', '')
                    planet_house = aspect.get('p1_house', '')
                    aspect_type = aspect.get('aspect', '')
                interacting_factors.append([name, planet_name, aspect_type])
    
    return interacting_factors

def interaction_for_planets(astro_subject,name):
    aspects = planet_aspects(astro_subject,name)
    planet_objects = [
        astro_subject.sun,
        astro_subject.moon,
        astro_subject.mercury,
        astro_subject.venus,
        astro_subject.mars,
        astro_subject.jupiter,
        astro_subject.saturn,
        astro_subject.uranus,
        astro_subject.neptune,
        astro_subject.pluto,
        astro_subject.mean_node,
        astro_subject.true_node,
        astro_subject.asc,
        astro_subject.mc
    ]
    results = []
    for aspect in aspects:
        output = interactions([factor(get_planet_object(aspect[0],planet_objects),astro_subject),factor(get_planet_object(aspect[1],planet_objects),astro_subject)],name, planet_objects)
        output.insert(3,aspect[2])#
        results.append(output)
    return results


def grand_key(astro_subject):
    planet_names = [planet['name'] for planet in astro_subject.planets_list]
    all_interactions = []

    # Collect all interactions
    for planet_name in planet_names:
        buf = interaction_for_planets(astro_subject, planet_name)
        if isinstance(buf, list):  # Check if buf is iterable
            all_interactions.append(buf)

    # Flatten the array
    flattened_array = [item for sublist in all_interactions for item in sublist]

    # Merge and remove duplicates based on the first and fourth elements
    merged_dict = {}
    for subarray in flattened_array:
        key = tuple([subarray[0], subarray[3]])  # Change this line to use the first and fourth elements
        if key in merged_dict:
            merged_dict[key].extend(subarray[3:])
        else:
            merged_dict[key] = subarray

    # Convert the merged dictionary back to a list
    merged_array = list(merged_dict.values())

    return merged_array


def rulership_for_planets(astro_subject):
    result_list = []
    #active_points_list=get_active_points_list(astro_subject,get_settings())[:-3]
    #ruler=get_active_points_list_ruler(astro_subject,get_settings())
    active_points_list = points_and_rulers(astro_subject)[0][:-3] #[:-3] cutting out 3 last elements (ASC, MC, Mean_Node, True_Node)
    #ruler = points_and_rulers(astro_subject)[1]
    sign_array = [item['sign'] for item in active_points_list]
    names = [item['name'] for item in active_points_list]

    for index, (sign_value, name) in enumerate(zip(sign_array, names),start = 1):
        ruler_index, ruler_name = sign_to_planet(sign_value, astro_subject)
        ruler_sign = active_points_list[ruler_index]['sign']
        house_index, house_name = find_house_by_sign(astro_subject.houses_list, sign_value)
        ruler_house_index, ruler_house_name = find_house_by_sign(astro_subject.houses_list, ruler_sign)

        result_list.append({
            'index': index,
            'name': name,
            'sign': sign_value,
            'house': house_name,
            'ruler': ruler_name,
            'ruler_in_sign': ruler_sign,
            'ruler_house': ruler_house_name
        })

    output_lines = []
    for result in result_list:
        output_lines.append(
            f"{result['index']}. {result['name']} in {result['sign']} -> in {result['house']} -> ruled by {result['ruler']} -> ruler in {result['ruler_in_sign']} -> in {result['ruler_house']}"
        )
    return "\n".join(output_lines)