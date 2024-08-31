from kerykeion.kr_types import KerykeionPointModel, KerykeionException, KerykeionSettingsModel, AstrologicalSubjectModel
from typing import Union, Literal
import logging
import math


def get_number_from_name(name: str) -> int:
    """Utility function, gets planet id from the name."""
    name = name.lower()

    if name == "sun":
        return 0
    elif name == "moon":
        return 1
    elif name == "mercury":
        return 2
    elif name == "venus":
        return 3
    elif name == "mars":
        return 4
    elif name == "jupiter":
        return 5
    elif name == "saturn":
        return 6
    elif name == "uranus":
        return 7
    elif name == "neptune":
        return 8
    elif name == "pluto":
        return 9
    elif name == "mean_node":
        return 10
    elif name == "south_node":
        return 11
    elif name == "true_node":
        return 12
    elif name == "asc":
        return 13
    elif name == "mc":
        return 14
    #elif name == "chiron":
    #    return 15
    
    else:
        return int(name)


def calculate_position(
    degree: Union[int, float], number_name: str, point_type: Literal["Planet", "House"]
) -> KerykeionPointModel:
    """Utility function to create a dictionary dividing the houses or the planets list."""

    if degree < 30:
        dictionary = {
            "name": number_name,
            "quality": "Cardinal",
            "element": "Fire",
            "sign": "Ari",
            "sign_num": 0,
            "position": degree,
            "abs_pos": degree,
            "emoji": "♈️",
            "point_type": point_type,
        }

    elif degree < 60:
        result = degree - 30
        dictionary = {
            "name": number_name,
            "quality": "Fixed",
            "element": "Earth",
            "sign": "Tau",
            "sign_num": 1,
            "position": result,
            "abs_pos": degree,
            "emoji": "♉️",
            "point_type": point_type,
        }
    elif degree < 90:
        result = degree - 60
        dictionary = {
            "name": number_name,
            "quality": "Mutable",
            "element": "Air",
            "sign": "Gem",
            "sign_num": 2,
            "position": result,
            "abs_pos": degree,
            "emoji": "♊️",
            "point_type": point_type,
        }
    elif degree < 120:
        result = degree - 90
        dictionary = {
            "name": number_name,
            "quality": "Cardinal",
            "element": "Water",
            "sign": "Can",
            "sign_num": 3,
            "position": result,
            "abs_pos": degree,
            "emoji": "♋️",
            "point_type": point_type,
        }
    elif degree < 150:
        result = degree - 120
        dictionary = {
            "name": number_name,
            "quality": "Fixed",
            "element": "Fire",
            "sign": "Leo",
            "sign_num": 4,
            "position": result,
            "abs_pos": degree,
            "emoji": "♌️",
            "point_type": point_type,
        }
    elif degree < 180:
        result = degree - 150
        dictionary = {
            "name": number_name,
            "quality": "Mutable",
            "element": "Earth",
            "sign": "Vir",
            "sign_num": 5,
            "position": result,
            "abs_pos": degree,
            "emoji": "♍️",
            "point_type": point_type,
        }
    elif degree < 210:
        result = degree - 180
        dictionary = {
            "name": number_name,
            "quality": "Cardinal",
            "element": "Air",
            "sign": "Lib",
            "sign_num": 6,
            "position": result,
            "abs_pos": degree,
            "emoji": "♎️",
            "point_type": point_type,
        }
    elif degree < 240:
        result = degree - 210
        dictionary = {
            "name": number_name,
            "quality": "Fixed",
            "element": "Water",
            "sign": "Sco",
            "sign_num": 7,
            "position": result,
            "abs_pos": degree,
            "emoji": "♏️",
            "point_type": point_type,
        }
    elif degree < 270:
        result = degree - 240
        dictionary = {
            "name": number_name,
            "quality": "Mutable",
            "element": "Fire",
            "sign": "Sag",
            "sign_num": 8,
            "position": result,
            "abs_pos": degree,
            "emoji": "♐️",
            "point_type": point_type,
        }
    elif degree < 300:
        result = degree - 270
        dictionary = {
            "name": number_name,
            "quality": "Cardinal",
            "element": "Earth",
            "sign": "Cap",
            "sign_num": 9,
            "position": result,
            "abs_pos": degree,
            "emoji": "♑️",
            "point_type": point_type,
        }
    elif degree < 330:
        result = degree - 300
        dictionary = {
            "name": number_name,
            "quality": "Fixed",
            "element": "Air",
            "sign": "Aqu",
            "sign_num": 10,
            "position": result,
            "abs_pos": degree,
            "emoji": "♒️",
            "point_type": point_type,
        }
    elif degree < 360:
        result = degree - 330
        dictionary = {
            "name": number_name,
            "quality": "Mutable",
            "element": "Water",
            "sign": "Pis",
            "sign_num": 11,
            "position": result,
            "abs_pos": degree,
            "emoji": "♓️",
            "point_type": point_type,
        }
    else:
        raise KerykeionException(f"Error in calculating positions! Degrees: {degree}")

    return KerykeionPointModel(**dictionary)

def mean_angle(angle1, angle2):
    x = math.cos(math.radians(angle1)) + math.cos(math.radians(angle2))
    y = math.sin(math.radians(angle1)) + math.sin(math.radians(angle2))
    mean = math.degrees(math.atan2(y, x))
    return mean % 360

def shortest_arc_midpoint(angle1, angle2):
    # Normalize the angles to be between 0 and 360 degrees
    angle1 = (angle1 % 360 + 360) % 360
    angle2 = (angle2 % 360 + 360) % 360

    # Calculate the absolute difference between the angles
    diff = abs(angle1 - angle2)

    # If the difference is greater than 180, we need to go the other way around the circle
    if diff > 180:
        # Calculate the midpoint of the smaller arc
        midpoint = (max(angle1, angle2) + min(angle1, angle2) + 360) / 2
    else:
         # Calculate the midpoint of the arc
        midpoint = (angle1 + angle2) / 2

     # Ensure the result is between 0 and 360 degrees
    return midpoint % 360

def setup_logging(level: str) -> None:
    """Setup logging for testing.
    
    Args:
        level: Log level as a string, options: debug, info, warning, error"""
    logopt: dict[str, int]  = {"debug": logging.DEBUG, 
                               "info": logging.INFO, 
                               "warning": logging.WARNING , 
                               "error": logging.ERROR}
    format: str             = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    loglevel: int           = logopt.get(level, logging.INFO)
    logging.basicConfig(format=format, level=loglevel)