from pathlib import Path
from kerykeion import AstrologicalSubject
import logging
from typing import Union, Literal

from kerykeion.aspects.natal_aspects import NatalAspects
from kerykeion.utilities import calculate_position, mean_angle, shortest_arc_midpoint
from kerykeion.settings.kerykeion_settings import get_settings
from dataclasses import dataclass
from functools import cached_property
from kerykeion.aspects.aspects_utils import planet_id_decoder, get_aspect_from_two_points, get_active_points_list

AXES_LIST = [
    "First_House",
    "Tenth_House",
    "Seventh_House",
    "Fourth_House",
]

class CompositeAspects(NatalAspects):

    def __init__(
            self,
            kr_object_one: AstrologicalSubject,
            kr_object_two: AstrologicalSubject,
            new_settings_file: Union[Path, None] = None,
    ):
        self.first_user = kr_object_one
        self.second_user = kr_object_two

        self.new_settings_file = new_settings_file
        self.settings = get_settings(self.new_settings_file)

        self.celestial_points = self.settings["celestial_points"]
        self.aspects_settings = self.settings["aspects"]
        self.axes_orbit_settings = self.settings["general_settings"]["axes_orbit"]

        self._all_aspects: Union[list, None] = None
        self._relevant_aspects: Union[list, None] = None

    @cached_property
    def all_aspects(self):

        point_type: Literal["Planet", "House"] = "Planet"

        if self._all_aspects is not None:
            return self._all_aspects
        
        active_points_list = []

        for first, second in zip(get_active_points_list(self.first_user, self.settings),
                                 get_active_points_list(self.second_user, self.settings)):
            #mean_abs_pos = mean_angle(first["abs_pos"], second["abs_pos"]) #
            mean_abs_pos = shortest_arc_midpoint(first["abs_pos"], second["abs_pos"])
            mean_sign_num = calculate_position(mean_abs_pos, first["name"], point_type=point_type)['sign_num']
            active_points_list.append({
                "name": first["name"],
                "abs_pos": mean_abs_pos,
                "sign_num": mean_sign_num
            })

        self.all_aspects_list = []

        for first in range(len(active_points_list)):
            # Generates the aspects list without repetitions
            for second in range(first + 1, len(active_points_list)):
                verdict, name, orbit, aspect_degrees, color, aid, diff = get_aspect_from_two_points(
                    self.aspects_settings, active_points_list[first]["abs_pos"], active_points_list[second]["abs_pos"],
                    active_points_list[first]["sign_num"],active_points_list[second]["sign_num"]
                )

                if verdict == True:
                    d_asp = {
                        "p1_name": active_points_list[first]["name"],
                        "p1_abs_pos": active_points_list[first]["abs_pos"],
                        "p2_name": active_points_list[second]["name"],
                        "p2_abs_pos": active_points_list[second]["abs_pos"],
                        "aspect": name,
                        "orbit": orbit,
                        "aspect_degrees": aspect_degrees,
                        "color": color,
                        "aid": aid,
                        "diff": diff,
                        "p1": planet_id_decoder(self.celestial_points, active_points_list[first]["name"]),
                        "p2": planet_id_decoder(
                            self.celestial_points,
                            active_points_list[second]["name"],
                        ),
                    }

                    self.all_aspects_list.append(d_asp)

        return self.all_aspects_list

    @cached_property
    def relevant_aspects(self):
        """
        Filters the aspects list with the desired points, in this case
        the most important are hardcoded.
        Set the list with set_points and creating a list with the names
        or the numbers of the houses.
        """

        logging.debug("Relevant aspects not already calculated, calculating now...")
        self.all_aspects

        aspects_filtered = []
        for a in self.all_aspects_list:
            if self.aspects_settings[a["aid"]]["is_active"] == True:
                aspects_filtered.append(a)

        axes_list = AXES_LIST
        counter = 0

        aspects_list_subtract = []
        for a in aspects_filtered:
            counter += 1
            name_p1 = str(a["p1_name"])
            name_p2 = str(a["p2_name"])

            if name_p1 in axes_list:
                if abs(a["orbit"]) >= self.axes_orbit_settings:
                    aspects_list_subtract.append(a)

            elif name_p2 in axes_list:
                if abs(a["orbit"]) >= self.axes_orbit_settings:
                    aspects_list_subtract.append(a)

        # Filter out aspects with 'Mean_Node', 'MC', 'ASC', 'True_Node'
        fil_asp = ['Mean_Node', 'MC', 'ASC', 'True_Node', 'South_Node']             
        filtered_aspects = [
        aspect for aspect in aspects_filtered 
        if aspect['p1_name'] not in fil_asp 
        and aspect['p2_name'] not in fil_asp]

        return filtered_aspects

if __name__ == "__main__":
    from kerykeion.utilities import setup_logging
    setup_logging(level="debug")

    john = AstrologicalSubject("John", 2001, 6, 8, 14, 40, "Moscow")
    yoko = AstrologicalSubject("Yoko", 2002, 2, 9, 23, 00, "Moscow")

    composite_aspects = CompositeAspects(john, yoko)

    print(composite_aspects.all_aspects)

    print(composite_aspects.relevant_aspects)