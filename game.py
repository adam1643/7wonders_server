from deck import *
from player import Player
from wonders import *
import random

all_cards = AllCards()


class Game:
    def __init__(self, no_players=3):
        names = ['a', 'b', 'c']
        self.players = [Player(names[i], wonders_a[i]) for i in range(no_players)]
        self.age = 1
        self.round = 1

        self.players[0].set_neighbors(self.players[1], self.players[2])
        self.players[1].set_neighbors(self.players[2], self.players[0])
        self.players[2].set_neighbors(self.players[0], self.players[1])

        self.deck1 = DeckAge1()
        print(self.deck1.splits[0])
        print(self.deck1.splits[1])
        print(self.deck1.splits[2])

        self.deck2 = DeckAge2()
        print(self.deck2.splits[0])
        print(self.deck2.splits[1])
        print(self.deck2.splits[2])

        self.deck3 = DeckAge3()
        print(self.deck3.splits[0])
        print(self.deck3.splits[1])
        print(self.deck3.splits[2])

        wonders = wonders_a #+ wonders_b
        random.shuffle(wonders)

        self.discarded = []

        for index, player in enumerate(self.players):
            player.set_cards(self.deck1.splits[index], [], self.age)
            player.wonder = wonders[index]

    def get_player(self, name):
        for player in self.players:
            if player.name == name:
                return player

    def get_ready_players(self):
        ready = 0
        for player in self.players:
            if player.state == 1:
                ready += 1
        return ready

    def move_ready(self):
        for player in self.players:
            player.move_available = True

    def update_emitted_move(self, player):
        updated_players = 0
        for p in self.players:
            if p == player:
                p.move_available = False
                updated_players += 1
            else:
                updated_players += 1 if p.move_available is False else 0
        if updated_players == 3:
            print("Updated all, start next round")
            self.start_next_round()

    def start_next_round(self):
        for p in self.players:
            p.state = 0
            p.update_available = True

        next_round_cards = [p.available_cards for p in self.players]
        self.players[0].set_cards(next_round_cards[1], [], self.age)
        self.players[1].set_cards(next_round_cards[2], [], self.age)
        self.players[2].set_cards(next_round_cards[0], [], self.age)

        self.round += 1

    def make_move(self):
        # TODO: Handle move when all players are ready

        for player in self.players:
            player.update_available = True
            player.state = 0
            player.move_available = True

    def build(self, player, building):
        for card in player.available_cards:
            if card.id == building:
                player.available_cards.remove(card)
                print("Removed card!")

    def get_card_status(self, index):
        for p in self.players:
            for c in p.built_cards:
                if c.id == index:
                    return 'built'
        for c in p.available_cards:
            if c.id == index:
                return 'available'
        return 'none'

    def check_player_resources(self, player, index):
        card = all_cards.get_card_by_id(index)
        res = ['none' for _ in card.cost]

        availables_res = player.available_resources()
        available_goods = player.available_goods()

        for idx, c in enumerate(card.cost):
            if c in availables_res:
                res[idx] = 'own'
                availables_res.remove(c)
            elif c in available_goods:
                res[idx] = 'own'
                available_goods.remove(c)
            else:
                pass


# deck = Deck()
# print(deck.cards[0])
# print(deck)

# g = Game()
