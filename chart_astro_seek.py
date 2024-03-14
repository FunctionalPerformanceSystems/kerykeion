import os
import requests
import matplotlib.pyplot as plt
import math
import matplotlib.pyplot as plt
from matplotlib.patches import ConnectionPatch
import matplotlib.image as mpimg
from kerykeion import NatalAspects


def degrees_into_coords(pos, starting_pt):
    r = 146
    x0 = 350
    y0 = 350
    degrees = 180 + starting_pt - pos
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
        planet1_position = degrees_into_coords(aspect['p1_abs_pos'], astro_subject.asc['abs_pos'])
        planet2_position = degrees_into_coords(aspect['p2_abs_pos'], astro_subject.asc['abs_pos'])

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


def astro_seek_chart_with_numbers(astro_subject):
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
       "planeta_lilith=0&planeta_chiron=0&planeta_fortune=0&planeta_spirit=0&&" + \
       "planeta_vertex=0" + \
       retrograde_params + \
       f"&tolerance=&tolerance_paral=0&house_system=whole&&narozeni_den={day}&narozeni_mesic={month}&narozeni_rok={year}&narozeni_hodina={hour}&" + \
       f"narozeni_minuta={minute}&narozeni_mesto_hidden={city}&narozeni_stat_hidden={country}&narozeni_podstat_kratky_hidden=&" + \
       f"narozeni_city={city},%20Germany&narozeni_sirka_stupne={lat}&narozeni_sirka_minuty=45&narozeni_sirka_smer=0&" + \
       f"narozeni_delka_stupne={long}&narozeni_delka_minuty=37&narozeni_delka_smer=0&narozeni_timezone_form=auto&" + \
       "narozeni_timezone_dst_form=auto&&nocache=13&&barva_stupne=0&tvar_ukazat="
    
    return change_url


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
    
    change_url = f"https://horoscopes.astro-seek.com/horoscope-chart1-700__radix_astroseek_customized_{day}-{month}-{year}_{hour}-{minute}.png?" + \
       "&nologo=1&seeklogo=1&domy_cisla=1&barva_planet=0&barva_stupne=2&barva_pozadi=0&barva_domy=1&barva_vzduch=1" + \
       "&barva_invert=0&hide_aspects=1&fortune_seda=1&spirit_seda=1&syzygy_seda=1&vertex_seda=1&chiron_seda=1&lilith_seda=1" +\
       "&fortune_asp=1&spirit_asp=1&syzygy_asp=1&vertex_asp=1&chiron_asp=1&lilith_asp=1&uzel_asp=1" +\
       f"&dum_1_new={asc}&dum_10_new={mc}&no_domy=&dum_1={h1}" 
    
    for i in range(1, 6):
        h_angle = h1 + i * 30
        if h_angle > 360:
            h_angle -= 360
        change_url += f"dum_{i+1}={h_angle}&"

    change_url +=  f"&planeta_slunce={planet_positions['slunce']}&planeta_luna={planet_positions['luna']}&planeta_merkur={planet_positions['merkur']}&" + \
       f"planeta_venuse={planet_positions['venuse']}&planeta_mars={planet_positions['mars']}&planeta_jupiter={planet_positions['jupiter']}&planeta_saturn={planet_positions['saturn']}&" + \
       f"planeta_uran={planet_positions['uran']}&planeta_neptun={planet_positions['neptun']}&planeta_pluto={planet_positions['pluto']}&planeta_uzel={planet_positions['uzel']}&" + \
       "planeta_lilith=0&planeta_chiron=0&planeta_fortune=0&planeta_bstesti=0&planeta_bspirit=0&planeta_spirit=0&&planeta_syzygy=0&&planeta_vertex=0" + \
       retrograde_params + \
       f"&tolerance=1&tolerance_paral=0&house_system=whole&&narozeni_den={day}&narozeni_mesic={month}&narozeni_rok={year}&narozeni_hodina={hour}&" + \
       f"narozeni_minuta={minute}&narozeni_mesto_hidden={city}&narozeni_stat_hidden={country}&narozeni_podstat_kratky_hidden=&" + \
       f"narozeni_city={city},%20Germany&narozeni_sirka_stupne={lat}&narozeni_sirka_minuty=45&narozeni_sirka_smer=0&" + \
       f"narozeni_delka_stupne={long}&narozeni_delka_minuty=37&narozeni_delka_smer=0&narozeni_timezone_form=auto&" + \
       "&narozeni_timezone_dst_form=auto&&seeklogo=0"
    
    return change_url


def test_astro_seek_chart(astro_subject):
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
    
    change_url = (f"https://horoscopes.astro-seek.com/horoscope-chart4-700__radix_astroseek_customized_{day}-{month}-{year}_{hour}-{minute}.png?"
                  "&nologo=1&seeklogo=1&domy_cisla=1&barva_planet=0&barva_stupne=2&barva_pozadi=0&barva_domy=1&barva_vzduch=1"
                  "&barva_invert=0&hide_aspects=1&fortune_seda=1&spirit_seda=1&syzygy_seda=1&vertex_seda=1&chiron_seda=1&lilith_seda=1"
                  "&fortune_asp=1&spirit_asp=1&syzygy_asp=1&vertex_asp=1&chiron_asp=1&lilith_asp=1&uzel_asp=1"
                  f"&dum_1_new={asc}&dum_10_new={mc}&no_domy=&dum_1={h1}")

    for i in range(1, 6):
        h_angle = h1 + i * 30
        if h_angle > 360:
            h_angle -= 360
        change_url += f"&dum_{i+1}={h_angle}"

    change_url += (f"&planeta_slunce={planet_positions['slunce']}&planeta_luna={planet_positions['luna']}&planeta_merkur={planet_positions['merkur']}"
                   f"&planeta_venuse={planet_positions['venuse']}&planeta_mars={planet_positions['mars']}&planeta_jupiter={planet_positions['jupiter']}"
                   f"&planeta_saturn={planet_positions['saturn']}&planeta_uran={planet_positions['uran']}&planeta_neptun={planet_positions['neptun']}"
                   f"&planeta_pluto={planet_positions['pluto']}&planeta_uzel={planet_positions['uzel']}"
                   "&planeta_lilith=0&planeta_chiron=0&planeta_fortune=0&planeta_bstesti=0&planeta_bspirit=0&planeta_spirit=0"
                   "&planeta_syzygy=0&planeta_vertex=0"
                   + retrograde_params +
                   f"&tolerance=1&tolerance_paral=0&house_system=whole&narozeni_den={day}&narozeni_mesic={month}&narozeni_rok={year}"
                   f"&narozeni_hodina={hour}&narozeni_minuta={minute}&narozeni_mesto_hidden={city}&narozeni_stat_hidden={country}"
                   "&narozeni_podstat_kratky_hidden=&narozeni_city=Moscow,%20Russia&narozeni_sirka_stupne=55&narozeni_sirka_minuty=45"
                   "&narozeni_sirka_smer=0&narozeni_delka_stupne=37&narozeni_delka_minuty=37&narozeni_delka_smer=0"
                   "&narozeni_timezone_form=auto&narozeni_timezone_dst_form=auto&seeklogo=0")

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