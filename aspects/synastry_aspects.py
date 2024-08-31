# -*- coding: utf-8 -*-
"""
    This is part of Kerykeion (C) 2023 Giacomo Battaglia
"""

from kerykeion import AstrologicalSubject
from pathlib import Path
from typing import Union
from functools import cached_property

from kerykeion.aspects.natal_aspects import NatalAspects
from kerykeion.settings.kerykeion_settings import get_settings
from kerykeion.aspects.aspects_utils import planet_id_decoder, get_aspect_from_two_points, get_active_points_list

AXES_LIST = [
    "First_House",
    "Tenth_House",
    "Seventh_House",
    "Fourth_House",
]

class SynastryAspects(NatalAspects):
    """
    Generates an object with all the aspects between two persons.
    """

    def __init__(
        self,
        kr_object_one: AstrologicalSubject,
        kr_object_two: AstrologicalSubject,
        new_settings_file: Union[Path, None] = None,
    ):
        # Subjects
        self.first_user = kr_object_one
        self.second_user = kr_object_two

        # Settings
        self.new_settings_file = new_settings_file
        self.settings = get_settings(self.new_settings_file)

        self.celestial_points = self.settings["celestial_points"]
        self.aspects_settings = self.settings["aspects"]
        self.axes_orbit_settings = self.settings["general_settings"]["axes_orbit"]

        # Private variables of the aspects
        self._all_aspects: Union[list, None] = None
        self._relevant_aspects: Union[list, None] = None

    @cached_property
    def all_aspects(self):
        """
        Return all the aspects of the points in the natal chart in a dictionary,
        first all the individual aspects of each planet, second the aspects
        whiteout repetitions.
        """

        if self._all_aspects is not None:
            return self._all_aspects

        # Celestial Points Lists
        first_active_points_list = get_active_points_list(self.first_user, self.settings)
        second_active_points_list = get_active_points_list(self.second_user, self.settings)

        self.all_aspects_list = []

        for first in range(len(first_active_points_list)):
            # Generates the aspects list whitout repetitions
            for second in range(len(second_active_points_list)):
                verdict, name, orbit, aspect_degrees, color, aid, diff = get_aspect_from_two_points(
                    self.aspects_settings,
                    first_active_points_list[first]["abs_pos"],
                    second_active_points_list[second]["abs_pos"],
                    first_active_points_list[first]["sign_num"],
                    second_active_points_list[second]["sign_num"]
                )

                if verdict == True:
                    d_asp = {
                        "p1_name": first_active_points_list[first]["name"],
                        "p1_abs_pos": first_active_points_list[first]["abs_pos"],
                        "p2_name": second_active_points_list[second]["name"],
                        "p2_abs_pos": second_active_points_list[second]["abs_pos"],
                        "aspect": name,
                        "orbit": orbit,
                        "aspect_degrees": aspect_degrees,
                        "color": color,
                        "aid": aid,
                        "diff": diff,
                        "p1": planet_id_decoder(
                            self.settings.celestial_points, first_active_points_list[first]["name"]
                        ),
                        "p2": planet_id_decoder(
                            self.settings.celestial_points,
                            second_active_points_list[second]["name"],
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

        #logging.debug("Relevant aspects not already calculated, calculating now...")
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

    john = AstrologicalSubject("John", 1940, 10, 9, 10, 30, "Liverpool")
    yoko = AstrologicalSubject("Yoko", 1933, 2, 18, 10, 30, "Tokyo")

    synastry_aspects = SynastryAspects(john, yoko)

    # All aspects
    print(synastry_aspects.all_aspects)

    # Relevant aspects
    print(synastry_aspects.relevant_aspects)
