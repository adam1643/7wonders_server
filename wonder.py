from enums import *


class Wonder:
    def __init__(self, id_code, name, side, start_res, costs, perks):
        self.id = id_code
        self.name = name
        self.side = side
        self.res = start_res

        self.costs = costs
        self.perks = perks

        self.max_level = len(costs)
