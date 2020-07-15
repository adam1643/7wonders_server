from enums import *


class Card:
    def __init__(self, id_code, color, name, cost=None, prev_free=None, next_free=None):
        self.id = id_code
        self.name = name
        self.color = color
        self.type = ''
        self.cost = cost if cost is not None else []

        self.prev_free = prev_free
        self.next_free = next_free

    def __str__(self):
        return f'{self.color.name.upper()}: {self.name} - {self.type}'

    def __repr__(self):
        return f'{self.color.name.upper()}: {self.name} - {self.type}'


class RedCard(Card):
    def __init__(self, id_code, name, value, cost=None, prev_free=None, next_free=None):
        super().__init__(id_code, CardColor.RED, name, cost, prev_free, next_free)
        self.combat_value = value


class YellowCard(Card):
    def __init__(self, id_code, name, perks=None, cost=None, prev_free=None, next_free=None):
        super().__init__(id_code, CardColor.YELLOW, name, cost, prev_free, next_free)
        self.perks = perks


class BrownCard(Card):
    def __init__(self, id_code, name, resource, cost=None, prev_free=None, next_free=None):
        super().__init__(id_code, CardColor.BROWN, name, cost, prev_free, next_free)
        self.resource = resource

    def __str__(self):
        return super().__str__() + f'  |  {self.resource.name}'


class GreyCard(Card):
    def __init__(self, id_code, name, good, cost=None, prev_free=None, next_free=None):
        super().__init__(id_code, CardColor.GREY, name, cost, prev_free, next_free)
        self.good = good


class BlueCard(Card):
    def __init__(self, id_code, name, vp, cost=None, prev_free=None, next_free=None):
        super().__init__(id_code, CardColor.BLUE, name, cost, prev_free, next_free)
        self.vp = vp


class GreenCard(Card):
    def __init__(self, id_code, name, science_type, cost=None, prev_free=None, next_free=None):
        super().__init__(id_code, CardColor.GREEN, name, cost, prev_free, next_free)

        self.science_type = science_type


class PurpleCard(Card):
    def __init__(self, id_code, name, perks, cost=None, prev_free=None, next_free=None):
        super().__init__(id_code, CardColor.PURPLE, name, cost, prev_free, next_free)
        self.perks = perks
