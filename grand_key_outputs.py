from kerykeion import NatalAspects
import pandas as pd

def aspect_table(astro_subject):
    name=NatalAspects(astro_subject)
    aspect=name.relevant_aspects
    df=pd.DataFrame(aspect)
    
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
    for subarray in input_array:
        formatted_subarray = []
        for item in subarray:
            if item in ['conjunction', 'opposition', 'trine', 'sextile', 'square']:
                formatted_subarray.append('|' + item)
            else:
                formatted_subarray.append(item)    
        print(' '.join(formatted_subarray))