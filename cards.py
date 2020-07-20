from card import *

r = Resource
g = Good


#########
# 1 AGE #
#########
brown_cards_1 = [
    BrownCard(111, 'Złoże rudy', [r.GOLD]),
    BrownCard(112, 'Złoże gliny', [r.BRICK]),
    BrownCard(113, 'Złoże kamienia', [r.STONE]),
    BrownCard(114, 'Skład drzewny', [r.WOOD]),
    BrownCard(115, 'Glinianka', [r.BRICK, r.GOLD], cost=[1]),
    BrownCard(116, 'Eksploracja drzewa', [r.WOOD, r.STONE], cost=[1])
]

grey_cards_1 = [
    GreyCard(121, 'Huta szkła', [g.GLASS]),
    GreyCard(122, 'Prasa', [g.PAPYRUS]),
    GreyCard(123, 'Warsztat tkacki', [g.TEXTILE])
]

blue_cards_1 = [
    BlueCard(131, 'Ołtarz', 2, next_free=231),
    BlueCard(132, 'Teatr', 2, next_free=232),
    BlueCard(133, 'Termy', 3, cost=[r.STONE], next_free=[233])
]

red_cards_1 = [
    RedCard(141, 'Wieża strażnicza', 1, cost=[r.BRICK]),
    RedCard(142, 'Koszary', 1, cost=[r.GOLD]),
    RedCard(143, 'Palisada', 1, cost=[r.WOOD])
]

yellow_cards_1 = [
    YellowCard(151, 'Handel wschodni', perks=[[Perk.DISCOUNT, ProductionType.RESOURCES, Neighborhood.RIGHT]], next_free=[252]),
    YellowCard(152, 'Handel zachodni', perks=[[Perk.DISCOUNT, ProductionType.RESOURCES, Neighborhood.LEFT]], next_free=[252]),
    YellowCard(153, 'Targowisko', perks=[[Perk.DISCOUNT, ProductionType.GOODS, Neighborhood.BOTH]], next_free=[251])
]

green_cards_1 = [
    GreenCard(161, 'Warsztat', Science.ZEBATKA, cost=[g.GLASS], next_free=[243, 261]),
    GreenCard(162, 'Skryptorium', Science.PLYTKA, cost=[g.PAPYRUS], next_free=[234, 262]),
    GreenCard(163, 'Apteka', Science.CYRKIEL, cost=[g.TEXTILE], next_free=[242, 263]),
]


#########
# 2 AGE #
#########
brown_cards_2 = [
    BrownCard(211, 'Tartak', [r.WOOD, r.WOOD], cost=[1]),
    BrownCard(212, 'Cegielnia', [r.BRICK, r.BRICK], cost=[1]),
    BrownCard(213, 'Kamieniołom', [r.STONE, r.STONE], cost=[1]),
    BrownCard(214, 'Odlewnia', [r.GOLD, r.GOLD], cost=[1])
]

grey_cards_2 = [
    GreyCard(221, 'Huta szkła', [g.GLASS]),
    GreyCard(222, 'Prasa', [g.PAPYRUS]),
    GreyCard(223, 'Warsztat tkacki', [g.TEXTILE])
]

blue_cards_2 = [
    BlueCard(231, 'Świątynia', 3, cost=[r.WOOD, r.BRICK, g.GLASS], prev_free=[131], next_free=[331]),
    BlueCard(232, 'Posąg', 4, cost=[r.GOLD, r.GOLD, r.WOOD], prev_free=[132], next_free=[332]),
    BlueCard(233, 'Akwedukt', 5, cost=[r.STONE, r.STONE, r.STONE], prev_free=[133]),
    BlueCard(234, 'Sąd', 4, cost=[r.BRICK, r.BRICK, g.TEXTILE], prev_free=[162])
]

red_cards_2 = [
    RedCard(241, 'Mury obronne', 2, cost=[r.STONE, r.STONE, r.STONE], next_free=[341]),
    RedCard(242, 'Stajnie', 2, cost=[r.BRICK, r.STONE, r.GOLD], prev_free=[163]),
    RedCard(243, 'Tor łuczniczy', 2, cost=[r.WOOD, r.WOOD, r.GOLD], prev_free=[161])
]

yellow_cards_2 = [
    YellowCard(251, 'Karawanseraj', cost=[r.WOOD, r.WOOD], perks=[[Perk.PRODUCTION, ProductionType.RESOURCES]], prev_free=[153], next_free=[351]),
    YellowCard(252, 'Rynek', cost=[r.BRICK, r.BRICK], perks=[[Perk.PRODUCTION, ProductionType.GOODS]], prev_free=[151, 152], next_free=[352]),
    YellowCard(253, 'Winnica', perks=[[Perk.MONEY, 1, CardColor.BROWN, Neighborhood.ALL_THREE]])
]

green_cards_2 = [
    GreenCard(261, 'Laboratorium', Science.ZEBATKA, cost=[r.BRICK, r.BRICK, g.PAPYRUS], prev_free=[161], next_free=[361, 342]),
    GreenCard(262, 'Biblioteka', Science.PLYTKA, cost=[r.STONE, r.STONE, g.TEXTILE], prev_free=[162], next_free=[362, 333]),
    GreenCard(263, 'Ambulatorium', Science.CYRKIEL, cost=[r.GOLD, r.GOLD, g.GLASS], prev_free=[163], next_free=[363, 353]),
    GreenCard(264, 'Szkoła', Science.PLYTKA, cost=[r.WOOD, g.PAPYRUS], next_free=[364, 365])
]


#########
# 3 AGE #
#########
blue_cards_3 = [
    BlueCard(331, 'Panteon', 7, cost=[r.BRICK, r.BRICK, r.GOLD, g.GLASS, g.PAPYRUS, g.TEXTILE], prev_free=[231]),
    BlueCard(332, 'Ogrody', 5, cost=[r.BRICK, r.BRICK, r.WOOD], prev_free=[232]),
    BlueCard(333, 'Senat', 6, cost=[r.WOOD, r.WOOD, r.STONE, r.GOLD], prev_free=[262]),
    BlueCard(334, 'Ratusz', 6, cost=[r.STONE, r.STONE, r.GOLD, g.GLASS]),
    BlueCard(335, 'Pałac', 8, cost=[r.STONE, r.GOLD, r.WOOD, r.BRICK, g.GLASS, g.PAPYRUS, g.TEXTILE])
]

red_cards_3 = [
    RedCard(341, 'Umocnienia', 3, cost=[r.GOLD, r.GOLD, r.GOLD, r.STONE], prev_free=[241]),
    RedCard(342, 'Machiny oblężnicze', 3, cost=[r.BRICK, r.BRICK, r.BRICK, r.WOOD], prev_free=[261]),
    RedCard(343, 'Arsenał', 3, cost=[r.WOOD, r.WOOD, r.GOLD, g.TEXTILE])
]

yellow_cards_3 = [
    YellowCard(351, 'Latarnia morska', perks=[[Perk.MONEY, 1, CardColor.YELLOW, Neighborhood.ONLY_ONE], [Perk.VP, 1, CardColor.YELLOW, Neighborhood.ONLY_ONE]], prev_free=[251]),
    YellowCard(352, 'Port', perks=[[Perk.MONEY, 1, CardColor.BROWN, Neighborhood.ONLY_ONE], [Perk.VP, 1, CardColor.BROWN, Neighborhood.ONLY_ONE]], prev_free=[252]),
    YellowCard(353, 'Arena', perks=[[Perk.MONEY, 3, CardColor.WONDER, Neighborhood.ONLY_ONE], [Perk.VP, 1, CardColor.WONDER, Neighborhood.ONLY_ONE]], prev_free=[263])
]

green_cards_3 = [
    GreenCard(361, 'Obserwatorium', Science.ZEBATKA, cost=[r.GOLD, r.GOLD, g.GLASS, g.TEXTILE], prev_free=[261]),
    GreenCard(362, 'Uniwersytet', Science.PLYTKA, cost=[r.WOOD, r.WOOD, g.PAPYRUS, g.GLASS], prev_free=[262]),
    GreenCard(363, 'Loża', Science.CYRKIEL, cost=[r.BRICK, r.BRICK, g.PAPYRUS, g.TEXTILE], prev_free=[263]),
    GreenCard(364, 'Pracownia', Science.ZEBATKA, cost=[r.WOOD, g.PAPYRUS, g.TEXTILE], prev_free=[264]),
    GreenCard(365, 'Akademia', Science.CYRKIEL, cost=[r.STONE, r.STONE, r.STONE, g.GLASS], prev_free=[264])
]

purple_cards_3 = [
    PurpleCard(370, 'Gildia armatorów', perks=[[Perk.VP, 1, CardColor.BROWN, Neighborhood.ONLY_ONE], [Perk.VP, 1, CardColor.GREY, Neighborhood.ONLY_ONE], [Perk.VP, 1, CardColor.PURPLE, Neighborhood.ONLY_ONE]], cost=[r.WOOD, r.WOOD, r.WOOD, g.GLASS, g.PAPYRUS]),
    PurpleCard(371, 'Gildia robotników', perks=[[Perk.VP, 1, CardColor.BROWN, Neighborhood.BOTH]], cost=[r.GOLD, r.GOLD, r.BRICK, r.STONE, r.WOOD]),
    PurpleCard(372, 'Gildia rzemieślników', perks=[[Perk.VP, 2, CardColor.GREY, Neighborhood.BOTH]], cost=[r.GOLD, r.GOLD, r.STONE, r.STONE]),
    PurpleCard(373, 'Gildia sędziów', perks=[[Perk.VP, 1, CardColor.BLUE, Neighborhood.BOTH]], cost=[r.WOOD, r.WOOD, r.WOOD, r.STONE, g.TEXTILE]),
    PurpleCard(374, 'Gildia szpiegów', perks=[[Perk.VP, 1, CardColor.RED, Neighborhood.BOTH]], cost=[r.BRICK, r.BRICK, r.BRICK, g.GLASS]),
    PurpleCard(375, 'Gildia kupców', perks=[[Perk.VP, 1, CardColor.YELLOW, Neighborhood.BOTH]], cost=[g.GLASS, g.TEXTILE, g.PAPYRUS]),
    PurpleCard(376, 'Gildia filozofów', perks=[[Perk.VP, 1, CardColor.GREEN, Neighborhood.BOTH]], cost=[r.BRICK, r.BRICK, r.BRICK, g.PAPYRUS, g.TEXTILE]),
    PurpleCard(377, 'Gildia budowniczych', perks=[[Perk.VP, 1, CardColor.WONDER, Neighborhood.ALL_THREE]], cost=[r.STONE, r.STONE, r.BRICK, r.BRICK, g.GLASS]),
    PurpleCard(378, 'Gildia strategów', perks=[[Perk.VP, 1, CardColor.LOST_VP, Neighborhood.BOTH]], cost=[r.GOLD, r.GOLD, r.STONE, g.TEXTILE]),
    PurpleCard(379, 'Gildia naukowcóc', perks=[[Perk.SCIENCE, 1, None, None]], cost=[r.WOOD, r.WOOD, r.GOLD, r.GOLD, g.PAPYRUS])
]



# Tests
# 1. wszystkie karty maja next free None albo != 0
# 2. wszystkie karty maja prev free None albo != 0
# 3. nie ma powtorzonych id
# 4. setki odpowiadaja erom, dziesiatki odpowiadaja kolorom
# 5. jesli jakas karta ma prev free to jej odpowiednik musi miec next free i na odwrot
# 6. trzecia era nie ma next, a pierwsza nie ma prev

