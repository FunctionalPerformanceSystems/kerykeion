import os
import requests
import matplotlib.pyplot as plt
import math
import matplotlib.pyplot as plt
from matplotlib.patches import ConnectionPatch
import matplotlib.image as mpimg
from kerykeion import NatalAspects


def degrees_into_coords(pos, first_house):
    r = 145.3
    x0 = 350
    y0 = 350
    degrees = 180 + first_house - pos
    radians = degrees * (math.pi / 180)
    x = x0 + r * math.cos(radians)
    y = y0 + r * math.sin(radians)
    return (x,y)


def draw_aspect_lines(astro_subject, image_path):

    aspect_list = NatalAspects(astro_subject).relevant_aspects

    image = mpimg.imread(image_path)

    fig, ax = plt.subplots(dpi = 200)
    ax.imshow(image)

    for aspect in aspect_list:
        planet1_position = degrees_into_coords(aspect['p1_abs_pos'], astro_subject.first_house['abs_pos'])
        planet2_position = degrees_into_coords(aspect['p2_abs_pos'], astro_subject.first_house['abs_pos'])

        con = ConnectionPatch(planet1_position, planet2_position, 'data', 'data',
                              arrowstyle='-', lw=0.35, color=aspect['color'])
        ax.add_artist(con)

    ax.axis('off')

    output_folder = 'aspected_charts'

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    output_file = os.path.join(output_folder, os.path.basename(image_path).lstrip('\\'))

    plt.savefig(output_file, bbox_inches='tight', pad_inches=0, dpi=200)
    plt.show()


def astro_seek_chart(astro_subject):
    year = astro_subject.year
    month = astro_subject.month
    day = astro_subject.day
    hour = astro_subject.hour
    minute = astro_subject.minute
    city = astro_subject.city
    country = astro_subject.nation
    lat = astro_subject.lat
    long = astro_subject.lng

    planets = {
        'slunce': astro_subject.sun,
        'luna': astro_subject.moon,
        'merkur': astro_subject.mercury,
        'venuse': astro_subject.venus,
        'mars': astro_subject.mars,
        'jupiter': astro_subject.jupiter,
        'saturn': astro_subject.saturn,
        'uran': astro_subject.uranus,
        'neptun': astro_subject.neptune,
        'pluto': astro_subject.pluto,
        'uzel': astro_subject.mean_node
    }

    planet_positions = {}
    for planet, data in planets.items():
        planet_positions[planet] = data['abs_pos']
    
    retrograde_params = ''.join(f'&r_{planet}=ANO' for planet, data in planets.items() if data['retrograde']==True)

    asc = astro_subject.asc['abs_pos']
    mc = astro_subject.mc['abs_pos']

    h1 = astro_subject.first_house['abs_pos']
    
    change_url = f"https://horoscopes.astro-seek.com/horoscope-chart4def-700__radix_{day}-{month}-{year}_{hour}-{minute}.png?" + \
       "hide_aspects=1&fortune_seda=1&vertex_seda=1&chiron_seda=1&lilith_seda=1&fortune_asp=1&vertex_asp=1&" + \
       f"chiron_asp=1&lilith_asp=1&asc_ukazat=1&&horizon_line=1&dum_1_new={asc}&dum_10_new={mc}&" + \
       f"no_domy=&dum_1={h1}&"
    
    for i in range(1, 6):
        h_angle = h1 + i * 30
        if h_angle > 360:
            h_angle -= 360
        change_url += f"dum_{i+1}={h_angle}&"

    change_url +=  "&pd_3=ANO&pd_4=ANO&pd_5=ANO&pd_8=ANO&" + \
       f"pd_9=ANO&planeta_slunce={planet_positions['slunce']}&planeta_luna={planet_positions['luna']}&planeta_merkur={planet_positions['merkur']}&" + \
       f"planeta_venuse={planet_positions['venuse']}&planeta_mars={planet_positions['mars']}&planeta_jupiter={planet_positions['jupiter']}&planeta_saturn={planet_positions['saturn']}&" + \
       f"planeta_uran={planet_positions['uran']}&planeta_neptun={planet_positions['neptun']}&planeta_pluto={planet_positions['pluto']}&planeta_uzel={planet_positions['uzel']}&" + \
       "planeta_lilith=321.60207496562&planeta_chiron=266.44514705258&planeta_fortune=30.34506214899&planeta_spirit=335.64419214579&&" + \
       "planeta_vertex=6.943843273885" + \
       retrograde_params + \
       f"&tolerance=&tolerance_paral=0&house_system=whole&&narozeni_den=8&narozeni_mesic=6&narozeni_rok={year}&narozeni_hodina={hour}&" + \
       f"narozeni_minuta={minute}&narozeni_mesto_hidden={city}&narozeni_stat_hidden={country}&narozeni_podstat_kratky_hidden=&" + \
       f"narozeni_city={city},%20Russia&narozeni_sirka_stupne={lat}&narozeni_sirka_minuty=45&narozeni_sirka_smer=0&" + \
       f"narozeni_delka_stupne={long}&narozeni_delka_minuty=37&narozeni_delka_smer=0&narozeni_timezone_form=auto&" + \
       "narozeni_timezone_dst_form=auto&&nocache=13&&barva_stupne=0&tvar_ukazat="
    
    return change_url


def download_chart_image(url, folder="charts_downloads"):
    if not os.path.exists(folder):
        os.makedirs(folder)

    filename = os.path.join(folder, url.split('/')[-1].split('?')[0])

    response = requests.get(url)

    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"Chart image downloaded successfully: {filename}")
    else:
        print(f"Failed to download chart image from {url}. Status code: {response.status_code}")
        filename = None
        
    return filename