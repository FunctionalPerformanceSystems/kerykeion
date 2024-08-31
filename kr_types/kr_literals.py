# -*- coding: utf-8 -*-
"""
    This is part of Kerykeion (C) 2023 Giacomo Battaglia
"""


from typing import Literal

# Zodiac Types:
ZodiacType = Literal["Tropic", "Sidereal"]

# Sings:
Sign = Literal[
    "Ari", "Tau", "Gem", "Can", "Leo", "Vir", "Lib", "Sco", "Sag", "Cap", "Aqu", "Pis"
]

Houses = Literal[
    "H1",
    "H2",
    "H3",
    "H4",
    "H5",
    "H6",
    "H7",
    "H8",
    "H9",
    "H10",
    "H11",
    "H12",
]

Planet = Literal[
    "Sun",
    "Moon",
    "Mercury",
    "Venus",
    "Mars",
    "Jupiter",
    "Saturn",
    "Uranus",
    "Neptune",
    "Pluto",
    "Mean_Node",
    "South_Node",
    "True_Node",
    "ASC",
    "MC"
]

Element = Literal["Air", "Fire", "Earth", "Water"]

Quality = Literal[
    "Cardinal",
    "Fixed",
    "Mutable",
]

ChartType = Literal["Natal", "ExternalNatal", "Synastry", "Transit", "Composite"]

LunarPhaseEmoji = Literal["🌑", "🌒", "🌓", "🌔", "🌕", "🌖", "🌗", "🌘"]
