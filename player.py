from wonders import *
from deck import *
from enums import *


class Player:
    def __init__(self, name, wonder):
        self.name = name
        self.wonder = wonder
        self.available_cards = []
        self.discarded_cards = []

        self.blue_vp = 0
        self.military_points = 0

        self.total_vp = 0

        self.military_wins = 0
        self.military_loses = 0

        self.money = 3

        self.active_perks = []
        self.built_cards = []
        self.built_wonders = 0

        self.left_neighbor = None
        self.right_neighbor = None

        self.age = 1
        self.round = 1

        self.state = 0
        self.update_available = True
        self.move_available = False

    def set_neighbors(self, left, right):
        self.left_neighbor = left
        self.right_neighbor = right

    def set_cards(self, cards, discarded, age):
        self.available_cards = cards
        self.discarded_cards = discarded

        self.age = age
        self.round = 8 - (len(cards))

    def end_age(self, age):
        pass

    def trade_available(self, neighbor, resource):
        if resource.__class__ == Resource:
            if neighbor == Neighborhood.LEFT:
                if resource in self.left_neighbor.available_resources():
                    if self.money >= 2:
                        return True
            elif neighbor == Neighborhood.RIGHT:
                if resource in self.right_neighbor.available_resources():
                    if self.money >= 2:
                        return True
        elif resource.__class__ == Good:
            if neighbor == Neighborhood.LEFT:
                if resource in self.left_neighbor.available_goods():
                    if self.money >= 2:
                        return True
            elif neighbor == Neighborhood.RIGHT:
                if resource in self.right_neighbor.available_goods():
                    if self.money >= 2:
                        return True

            # TODO: Implement discounts
        return False

    def get_built_by_color(self, color):
        built = 0
        if color == CardColor.WONDER:
            return self.built_wonders

        if color == CardColor.LOST_VP:
            return self.military_loses

        for card in self.built_cards:
            if card.color == color:
                built += 1
        return built

    def available_resources(self):
        resources = []
        if self.wonder.res in Resource:
            resources.append(self.wonder.res)
        for card in self.built_cards:
            if card.color == CardColor.BROWN:
                for resource in card.resource:
                    resources.append(resource)
        return resources.copy()

    def available_goods(self):
        goods = []
        if self.wonder.res in Good:
            goods.append(self.wonder.res)
        for card in self.built_cards:
            if card.color == CardColor.GREY:
                for resource in card.resource:
                    goods.append(resource)
        return goods.copy()

    def calulate_military(self):
        self.military_points = 0

        # calculate military points gained by perks
        for perk in self.active_perks:
            if perk[0] == Perk.MILITARY:
                self.military_points += perk[1]

        for card in self.built_cards:
            if card.color == CardColor.RED:
                self.military_points += card.combat_value

    def calculate_blue_vp(self):
        self.blue_vp = 0

        for card in self.built_cards:
            if card.color == CardColor.BLUE:
                self.blue_vp += card.vp

    def activate_perks(self, perks):
        try:
            self.active_perks.extend(perks)
        except NameError:
            pass
        finally:
            self.use_immediate_perks()

    def use_immediate_perks(self):
        to_remove = []
        for idx, perk in enumerate(self.active_perks):
            if perk[0] == Perk.MONEY:
                if len(perk) == 2:
                    self.money += perk[1]
                else:
                    color = perk[2]
                    if perk[3] == Neighborhood.ALL_THREE:
                        self.money += self.get_built_by_color(color)
                        self.money += self.left_neighbor.get_built_by_color(color)
                        self.money += self.right_neighbor.get_buily_by_color(color)
                    # TODO: implement for other types
                to_remove.append(perk)

            if perk[0] == Perk.FREE_DISCARDED:
                # TODO: implement discarded handling
                pass

            # TODO: implement other wonder perks

        for perk in to_remove:
            self.active_perks.remove(perk)

    def can_build_with_promotion(self, card_to_build):
        for card in self.built_cards:
            if card_to_build.prev_free.any() == card.id:
                return True
        return False

    def can_build_with_own_resources(self, card_to_build):
        res = card_to_build.cost

        # TODO: Implement check for money costs

        if res is None:
            return True

        if self.wonder.res in res:
            res.remove(self.wonder.res)

        for card in self.built_cards:
            if card.color == CardColor.BROWN:
                for resource in card.resource:
                    if resource in res:
                        res.remove(resource)

            if card.color == CardColor.GREY:
                for good in card.good:
                    if good in res:
                        res.remove(good)

        if len(res) == 0:
            return True

        for perk in self.active_perks:
            if perk[0] == Perk.PRODUCTION:
                if perk[1] == ProductionType.RESOURCES:
                    for rem_r in res:
                        if rem_r in Resource:
                            res.remove(rem_r)
                            break

                if perk[1] == ProductionType.GOODS:
                    if perk[1] == ProductionType.GOODS:
                        for rem_r in res:
                            if rem_r in Good:
                                res.remove(rem_r)
                                break
        if len(res) == 0:
            return True
        return False

    def build(self, card):

        self.built_cards.append(card)

        if card.color == CardColor.RED:
            self.calulate_military()

        if card.color == CardColor.BLUE:
            self.calculate_blue_vp()

        if card.color == CardColor.YELLOW:
            self.activate_perks(card.perks)

        if card.color == CardColor.PURPLE:
            self.activate_perks(card.perks)

    def build_wonder(self):
        if self.built_wonders == self.wonder.max_level:
            return

        self.built_wonders += 1
        perks = self.wonder.perks[self.built_wonders]
        self.activate_perks(perks)