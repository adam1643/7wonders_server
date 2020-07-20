from cards import *
from cards import *
import random


r = Resource
g = Good

class Deck:
    def __init__(self, age):
        self.age = age
        self.cards = None

    def split_deck(self, n):
        n = len(self.cards) // n

        random.shuffle(self.cards)
        split1 = self.cards[0:n]
        split2 = self.cards[n:2 * n]
        split3 = self.cards[2 * n:]

        return split1, split2, split3

    def __str__(self):
        return str([str(card) for card in self.cards])


class DeckAge1(Deck):
    def __init__(self):
        super().__init__(1)
        self.cards = brown_cards_1 + grey_cards_1 + yellow_cards_1 + blue_cards_1 + red_cards_1 + green_cards_1
        self.splits = self.split_deck(3)


class DeckAge2(Deck):
    def __init__(self):
        super().__init__(2)
        self.cards = brown_cards_2 + grey_cards_2 + yellow_cards_2 + blue_cards_2 + red_cards_2 + green_cards_2
        self.splits = self.split_deck(3)


class DeckAge3(Deck):
    def __init__(self):
        super().__init__(3)
        self.cards = yellow_cards_3 + blue_cards_3 + red_cards_3 + green_cards_3 + purple_cards_3[:5]
        self.splits = self.split_deck(3)


class AllCards:
    def __init__(self):
        self.cards = brown_cards_1 + grey_cards_1 + yellow_cards_1 + blue_cards_1 + red_cards_1 + green_cards_1
        self.cards += brown_cards_2 + grey_cards_2 + yellow_cards_2 + blue_cards_2 + red_cards_2 + green_cards_2
        self.cards += yellow_cards_3 + blue_cards_3 + red_cards_3 + green_cards_3 + purple_cards_3

    def get_card_by_id(self, index):
        for card in self.cards:
            if card.id == index:
                return card
        return None

    def get_card_cost(self, index):
        card = self.get_card_by_id(index)
        return card.cost

    def get_card_cost(self, index):
        card = self.get_card_by_id(index)
        costs = []
        for c in card.cost:
            print(c)
            if c == r.WOOD:
                costs.append('wood')
            elif c == r.STONE:
                costs.append('stone')
            elif c == r.BRICK:
                costs.append('brick')
            elif c == r.GOLD:
                costs.append('gold')
            elif c == g.PAPYRUS:
                costs.append('papyrus')
            elif c == g.GLASS:
                costs.append('glass')
            elif c == g.TEXTILE:
                costs.append('textile')
            else:
                costs.append('money')
        return costs
