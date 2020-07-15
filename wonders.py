from wonder import *

r = Resource
g = Good

olympia_a_costs = [
    [r.WOOD, r.WOOD],
    [r.STONE, r.STONE],
    [r.GOLD, r.GOLD]
]
olympia_a_perks = [
    [Perk.VP, 3],
    [Perk.FREE_BUILD],
    [Perk.VP, 7]
]

babylon_a_costs = [
    [r.BRICK, r.BRICK],
    [r.WOOD, r.WOOD, r.WOOD],
    [r.BRICK, r.BRICK, r.BRICK, r.BRICK]
]
babylon_a_perks = [
    [Perk.VP, 3],
    [Perk.SCIENCE, 1],
    [Perk.VP, 7]
]

gizah_a_costs = [
    [r.STONE, r.STONE],
    [r.WOOD, r.WOOD, r.WOOD],
    [r.STONE, r.STONE, r.STONE, r.STONE]
]
gizah_a_perks = [
    [Perk.VP, 3],
    [Perk.VP, 5],
    [Perk.VP, 7]
]

rhodos_a_costs = [
    [r.WOOD, r.WOOD],
    [r.BRICK, r.BRICK, r.BRICK],
    [r.GOLD, r.GOLD, r.GOLD, r.GOLD]
]
rhodos_a_perks = [
    [Perk.VP, 3],
    [Perk.MILITARY, 2],
    [Perk.VP, 7]
]

ephesos_a_costs = [
    [r.STONE, r.STONE],
    [r.WOOD, r.WOOD],
    [g.PAPYRUS, g.PAPYRUS]
]
ephesos_a_perks = [
    [Perk.VP, 3],
    [Perk.MONEY, 9],
    [Perk.VP, 7]
]

alexandria_a_costs = [
    [r.STONE, r.STONE],
    [r.GOLD, r.GOLD],
    [g.GLASS, g.GLASS]
]
alexandria_a_perks = [
    [Perk.VP, 3],
    [Perk.PRODUCTION, ProductionType.RESOURCES],
    [Perk.VP, 7]
]

halikarnassos_a_costs = [
    [r.BRICK, r.BRICK],
    [r.GOLD, r.GOLD, r.GOLD],
    [g.TEXTILE, g.TEXTILE]
]
halikarnassos_a_perks = [
    [Perk.VP, 3],
    [Perk.FREE_DISCARDED],
    [Perk.VP, 7]
]

olympia_b_costs = [
    [r.WOOD, r.WOOD],
    [r.STONE, r.STONE],
    [g.TEXTILE, r.GOLD, r.GOLD]
]
olympia_b_perks = [
    [Perk.DISCOUNT, ProductionType.RESOURCES, Neighborhood.BOTH],
    [Perk.VP, 5],
    [Perk.PURPLE_COPY, Neighborhood.BOTH]
]

babylon_b_costs = [
    [g.TEXTILE, r.BRICK],
    [g.GLASS, r.WOOD, r.WOOD],
    [g.PAPYRUS, r.BRICK, r.BRICK, r.BRICK]
]
babylon_b_perks = [
    [Perk.VP, 3],
    [Perk.SCIENCE, 1],
    [Perk.USE_BOTH_LAST]
]

gizah_b_costs = [
    [r.WOOD, r.WOOD],
    [r.STONE, r.STONE, r.STONE],
    [r.BRICK, r.BRICK, r.BRICK],
    [g.PAPYRUS, r.STONE, r.STONE, r.STONE, r.STONE]
]
gizah_b_perks = [
    [Perk.VP, 3],
    [Perk.VP, 5],
    [Perk.VP, 5],
    [Perk.VP, 7]
]

rhodos_b_costs = [
    [r.STONE, r.STONE, r.STONE],
    [r.GOLD, r.GOLD, r.GOLD, r.GOLD]
]
rhodos_b_perks = [
    [[Perk.MILITARY, 1], [Perk.VP, 3], [Perk.MONEY, 3]],
    [[Perk.MILITARY, 1], [Perk.VP, 4], [Perk.MONEY, 4]]
]

ephesos_b_costs = [
    [r.STONE, r.STONE],
    [r.WOOD, r.WOOD],
    [g.PAPYRUS, g.TEXTILE, g.GLASS]
]
ephesos_b_perks = [
    [[Perk.VP, 2], [Perk.MONEY, 4]],
    [[Perk.VP, 3], [Perk.MONEY, 4]],
    [[Perk.VP, 5], [Perk.MONEY, 4]]
]

alexandria_b_costs = [
    [r.BRICK, r.BRICK],
    [r.WOOD, r.WOOD],
    [r.STONE, r.STONE, r.STONE]
]
alexandria_b_perks = [
    [Perk.PRODUCTION, ProductionType.RESOURCES],
    [Perk.PRODUCTION, ProductionType.GOODS],
    [Perk.VP, 7]
]

halikarnassos_b_costs = [
    [r.GOLD, r.GOLD],
    [r.BRICK, r.BRICK, r.BRICK],
    [g.GLASS, g.PAPYRUS, g.TEXTILE]
]
halikarnassos_b_perks = [
    [[Perk.VP, 2], [Perk.FREE_DISCARDED]],
    [[Perk.VP, 1], [Perk.FREE_DISCARDED]],
    [Perk.FREE_DISCARDED]
]


wonders_a = [
    Wonder(11, 'Olympia A', Side.A, r.WOOD, costs=olympia_a_costs, perks=olympia_a_perks),
    Wonder(12, 'Babilon A', Side.A, r.BRICK, costs=babylon_a_costs, perks=babylon_a_perks),
    Wonder(13, 'Giza A', Side.A, r.STONE, costs=gizah_a_costs, perks=gizah_a_perks),
    Wonder(14, 'Rodos A', Side.A, r.GOLD, costs=rhodos_a_costs, perks=rhodos_a_perks),
    Wonder(15, 'Efez A', Side.A, g.PAPYRUS, costs=ephesos_a_costs, perks=ephesos_a_perks),
    Wonder(16, 'Aleksandria A', Side.A, g.GLASS, costs=alexandria_a_costs, perks=alexandria_a_perks),
    Wonder(17, 'Halikarnas A', Side.A, g.TEXTILE, costs=halikarnassos_a_costs, perks=halikarnassos_a_perks)
]

wonders_b = [
    Wonder(21, 'Olympia B', Side.B, r.WOOD, costs=olympia_b_costs, perks=olympia_b_perks),
    Wonder(22, 'Babilon B', Side.B, r.BRICK, costs=babylon_b_costs, perks=babylon_b_perks),
    Wonder(23, 'Giza B', Side.B, r.STONE, costs=gizah_b_costs, perks=gizah_b_perks),
    Wonder(24, 'Rodos B', Side.B, r.GOLD, costs=rhodos_b_costs, perks=rhodos_b_perks),
    Wonder(25, 'Efez B', Side.B, g.PAPYRUS, costs=ephesos_b_costs, perks=ephesos_b_perks),
    Wonder(26, 'Aleksandria B', Side.B, g.GLASS, costs=alexandria_b_costs, perks=alexandria_b_perks),
    Wonder(27, 'Halikarnas B', Side.B, g.TEXTILE, costs=halikarnassos_b_costs, perks=halikarnassos_b_perks)
]
