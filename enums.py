from enum import Enum


class CardColor(Enum):
    BROWN = 1
    GREY = 2
    BLUE = 3
    RED = 4
    YELLOW = 5
    GREEN = 6
    PURPLE = 7
    WONDER = 8
    LOST_VP = 9


class Science(Enum):
    CYRKIEL = 1
    ZEBATKA = 2
    PLYTKA = 3


class Resource(Enum):
    WOOD = 1
    BRICK = 2
    STONE = 3
    GOLD = 4


class Good(Enum):
    PAPYRUS = 1
    GLASS = 2
    TEXTILE = 3


class ProductionType(Enum):
    RESOURCES = 1
    GOODS = 2


class Neighborhood(Enum):
    LEFT = 1
    RIGHT = 2
    BOTH = 3
    ALL_THREE = 4
    ONLY_ONE = 5


class Perk(Enum):
    MONEY = 1
    VP = 2
    SCIENCE = 3
    DISCOUNT = 4
    PRODUCTION = 5
    FREE_BUILD = 6
    FREE_DISCARDED = 7
    USE_BOTH_LAST = 8
    MILITARY = 9
    PURPLE_COPY = 10


class Side(Enum):
    A = 1
    B = 2
