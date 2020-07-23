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
        self.military_points = [1, 3, 5]

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

        for p in self.players:
            p.discarded_cards = self.discarded

        self.players[1].built_cards.extend([all_cards.get_card_by_id(141), all_cards.get_card_by_id(211), all_cards.get_card_by_id(212), all_cards.get_card_by_id(213), all_cards.get_card_by_id(214)])
        self.players[2].built_cards.extend([all_cards.get_card_by_id(142), all_cards.get_card_by_id(211), all_cards.get_card_by_id(212), all_cards.get_card_by_id(213), all_cards.get_card_by_id(214)])

        self.players[0].built_cards.extend([all_cards.get_card_by_id(161), all_cards.get_card_by_id(162), all_cards.get_card_by_id(163)])
        self.players[0].build(all_cards.get_card_by_id(251))

        for index, player in enumerate(self.players):
            player.set_cards(self.deck2.splits[index], [], self.age)
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
        if self.round == 3:
            self.make_battle()
            for p in self.players:
                p.end_age = True
            self.start_next_age()

    def start_next_age(self):
        self.age += 1
        self.round = 1
        for index, player in enumerate(self.players):
            player.set_cards(self.deck3.splits[index], [], self.age)

    def make_battle(self):
        for p in self.players:
            if p.calulate_military() > p.left_neighbor.calulate_military():
                p.military_wins += self.military_points[self.age - 1]
                p.last_battle[0] = 1
            elif p.calulate_military() < p.left_neighbor.calulate_military():
                p.military_loses += 1
                p.last_battle[0] = -1
            else:
                p.last_battle[0] = 0

            if p.calulate_military() > p.right_neighbor.calulate_military():
                p.military_wins += self.military_points[self.age - 1]
                p.last_battle[1] = 1
            elif p.calulate_military() < p.right_neighbor.calulate_military():
                p.military_loses += 1
                p.last_battle[1] = -1
            else:
                p.last_battle[1] = 0

    def make_move(self):
        # TODO: Handle move when all players are ready

        for player in self.players:
            player.update_available = True
            player.state = 0
            player.move_available = True

    def prepare_for_build(self, player, building, chosen, discard):
        player.ready_to_built = building
        player.chosen_to_build = chosen if str(chosen) != 'a' else ['none' for _ in all_cards.get_card_by_id(building).cost]
        player.discarding = discard

    def build(self):
        for p in self.players:
            delta = p.money
            for card in p.available_cards:
                if card.id == p.ready_to_built:
                    p.available_cards.remove(card)
                    if p.discarding is True:
                        self.discarded.append(card)
                        p.money += 3
                        p.last_built = -1
                        p.delta = p.money - delta
                        p.ready_to_built = None
                        continue
                    print("CHOSEM", card.cost, p.chosen_to_build)
                    for cost, ch in zip(card.cost, p.chosen_to_build):
                        if ch == 'left':
                            p.buy_from_left(cost)
                        if ch == 'right':
                            p.buy_from_right(cost)
                    print("Removed card!")
                    p.last_built = p.ready_to_built
                    p.delta = p.money - delta
                    p.ready_to_built = None

    def get_card_status(self, index):
        for p in self.players:
            for c in p.built_cards:
                if c.id == index:
                    return 'built'
        for c in p.available_cards:
            if c.id == index:
                return 'available'
        return 'none'

    def check_upgrade(self, player, index):
        for card in self.players[0].built_cards:
            for free in card.next_free:
                if free == index:
                    return True
        return False

    def check_player_resources(self, player, index, wonder=False):
        if wonder is False:
            card = all_cards.get_card_by_id(index)
            cost = card.cost
        else:
            cost = player.get_next_wonder_cost()
        res = ['none' for _ in cost]

        availables_res = player.available_resources()
        available_goods = player.available_goods()

        for idx, c in enumerate(cost):
            if c in availables_res:
                res[idx] = 'own'
                availables_res.remove(c)
            elif c in available_goods:
                res[idx] = 'own'
                available_goods.remove(c)
            elif c not in r and c not in g:
                if player.money >= 0:
                    res[idx] = 'own'

        left = player.left_neighbor.available_resources()
        right = player.right_neighbor.available_resources()
        for idx, c in enumerate(cost):
            if res[idx] != 'none':
                continue
            if c in left and c in right:
                res[idx] = 'both'
            elif c in left:
                res[idx] = 'left'
            elif c in right:
                res[idx] = 'right'

        left = player.left_neighbor.available_goods()
        right = player.right_neighbor.available_goods()
        for idx, c in enumerate(cost):
            if res[idx] != 'none':
                continue
            if c in left and c in right:
                res[idx] = 'both'
            elif c in left:
                res[idx] = 'left'
            elif c in right:
                res[idx] = 'right'

        for idx, c in enumerate(cost):
            print("CHECK perks")
            in_perks = False
            if c in Resource:
                print("In perks")
                for perk in player.active_perks:
                    print("Res perks")
                    if perk[0] == Perk.PRODUCTION and perk[1] == ProductionType.RESOURCES:
                        in_perks = True
            if c in Good:
                for perk in player.active_perks:
                    if perk[0] == Perk.PRODUCTION and perk[1] == ProductionType.GOODS:
                        in_perks = True

            if in_perks is True:
                if res[idx] == 'none':
                    res[idx] = 'own'
                if res[idx] == 'left':
                    res[idx] = 'left_own'
                if res[idx] == 'right':
                    res[idx] = 'right_own'
                if res[idx] == 'both':
                    res[idx] = 'all'

        return res

    def get_player_neighbor_money(self, player):
        return [player.left_neighbor.money, player.money, player.right_neighbor.money]

    def get_player_neighbor_military(self, player):
        return [player.calulate_military(), player.left_neighbor.calulate_military(), player.right_neighbor.calulate_military()]

    def get_player_neighbor_wins(self, player):
        return [player.military_wins, player.left_neighbor.military_wins, player.right_neighbor.military_wins]

    def get_player_neighbor_loses(self, player):
        return [player.military_loses, player.left_neighbor.military_loses, player.right_neighbor.military_loses]


# deck = Deck()
# print(deck.cards[0])
# print(deck)

# g = Game()
