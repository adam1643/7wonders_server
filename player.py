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
        self.perks_vp = 0
        self.military_points = 0

        self.total_vp = 0

        self.military_wins = 0
        self.military_loses = 0
        self.last_battle = [0, 0]

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
        self.end_age = False

        self.ready_to_built = None
        self.chosen_to_build = None
        self.last_built = None
        self.discarding = False
        self.delta = 0
        self.build_discarded = False

    def set_neighbors(self, left, right):
        self.left_neighbor = left
        self.right_neighbor = right

    def set_cards(self, cards, discarded, age):
        self.available_cards = cards
        self.discarded_cards = discarded

        self.age = age
        self.round = 8 - (len(cards))

    def buy_from_left(self, res):
        if res in r:
            for perk in self.active_perks:
                if perk[0] == Perk.DISCOUNT and perk[1] == ProductionType.RESOURCES and perk[2] == Neighborhood.LEFT:
                    self.money -= 1
                    self.left_neighbor.money += 1
                    return
            self.money -= 2
            self.left_neighbor.money += 2
            return
        if res in g:
            for perk in self.active_perks:
                if perk[0] == Perk.DISCOUNT and perk[1] == ProductionType.GOODS and perk[2] == Neighborhood.BOTH:
                    self.money -= 1
                    self.left_neighbor.money += 1
                    return
            self.money -= 2
            self.left_neighbor.money += 2
            return

    def buy_from_right(self, res):
        if res in r:
            for perk in self.active_perks:
                if perk[0] == Perk.DISCOUNT and perk[1] == ProductionType.RESOURCES and perk[2] == Neighborhood.RIGHT:
                    self.money -= 1
                    self.right_neighbor.money += 1
                    return
            self.money -= 2
            self.right_neighbor.money += 2
            return
        if res in g:
            for perk in self.active_perks:
                if perk[0] == Perk.DISCOUNT and perk[1] == ProductionType.GOODS and perk[2] == Neighborhood.BOTH:
                    self.money -= 1
                    self.right_neighbor.money += 1
                    return
            self.money -= 2
            self.right_neighbor.money += 2
            return

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

        return self.military_points

    def calculate_blue_vp(self):
        self.blue_vp = 0

        for card in self.built_cards:
            if card.color == CardColor.BLUE:
                self.blue_vp += card.vp

    def calculate_perks_vp(self):
        vp = 0
        player = lambda color: sum([1 if card.color == color else 0 for card in self.built_cards])
        left = lambda color: sum([1 if card.color == color else 0 for card in self.left_neighbor.built_cards])
        right = lambda color: sum([1 if card.color == color else 0 for card in self.right_neighbor.built_cards])
        for perk in self.active_perks:
            if perk[0] == Perk.VP:
                amount = perk[1]
                giver = perk[2]
                owner = perk[3]

                if giver == CardColor.WONDER:
                    vp += amount * self.built_wonders if owner in [Neighborhood.ALL_THREE or Neighborhood.ONLY_ONE] else 0
                    vp += amount * self.left_neighbor.built_wonders if owner in [Neighborhood.LEFT, Neighborhood.BOTH, Neighborhood.ALL_THREE] else 0
                    vp += amount * self.right_neighbor.built_wonders if owner in [Neighborhood.RIGHT, Neighborhood.BOTH, Neighborhood.ALL_THREE] else 0
                    continue
                if giver == CardColor.LOST_VP:
                    vp += amount * self.military_loses if owner in [Neighborhood.ALL_THREE or Neighborhood.ONLY_ONE] else 0
                    vp += amount * self.left_neighbor.military_loses if owner in [Neighborhood.LEFT, Neighborhood.BOTH, Neighborhood.ALL_THREE] else 0
                    vp += amount * self.right_neighbor.military_loses if owner in [Neighborhood.RIGHT, Neighborhood.BOTH, Neighborhood.ALL_THREE] else 0
                    continue

                vp += amount * left(giver) if owner in [Neighborhood.LEFT, Neighborhood.BOTH, Neighborhood.ALL_THREE] else 0
                vp += amount * right(giver) if owner in [Neighborhood.RIGHT, Neighborhood.BOTH, Neighborhood.ALL_THREE] else 0
                vp += amount * player(giver) if owner in [Neighborhood.ALL_THREE or Neighborhood.ONLY_ONE] else 0

        self.perks_vp = vp
        return vp

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
                    to_remove.append(perk)
                    continue

                color = perk[2]
                if perk[3] == Neighborhood.ALL_THREE:
                    self.money += self.get_built_by_color(color)
                    self.money += self.left_neighbor.get_built_by_color(color)
                    self.money += self.right_neighbor.get_buily_by_color(color)
                # TODO: implement for other types
                to_remove.append(perk)

            if perk[0] == Perk.FREE_DISCARDED:
                # TODO: implement discarded handling
                self.build_discarded = True
                to_remove.append(perk)

            # TODO: implement other wonder perks

        for perk in to_remove:
            self.active_perks.remove(perk)

    def can_build_with_promotion(self, card_to_build):
        for card in self.built_cards:
            if card.id in card_to_build.prev_free:
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

    def can_build(self, card, chosen, wonder=False):
        if wonder is True:
            cost = self.get_next_wonder_cost()
        else:
            cost = card.cost
        money = self.money
        left_res, left_goods = self.left_neighbor.available_resources(), self.left_neighbor.available_goods()
        right_res, right_goods = self.right_neighbor.available_resources(), self.right_neighbor.available_goods()
        left_res_discount, left_goods_discount = False, False
        right_res_discount, right_goods_discount = False, False
        for perk in self.active_perks:
            if perk[0] == Perk.DISCOUNT:
                if perk[1] == ProductionType.RESOURCES:
                    if perk[2] in [Neighborhood.LEFT, Neighborhood.BOTH]:
                        left_res_discount = True
                    if perk[2] in [Neighborhood.RIGHT, Neighborhood.BOTH]:
                        right_res_discount = True

                if perk[1] == ProductionType.GOODS:
                    if perk[2] in [Neighborhood.LEFT, Neighborhood.BOTH]:
                        left_goods_discount = True
                    if perk[2] in [Neighborhood.RIGHT, Neighborhood.BOTH]:
                        right_goods_discount = True

        res_perks, goods_perks = 0, 0
        for perk in self.active_perks:
            if perk[0] == Perk.PRODUCTION:
                if perk[1] == ProductionType.RESOURCES:
                    res_perks += 1

                if perk[1] == ProductionType.GOODS:
                    goods_perks += 1

        for c, ch in cost, chosen:
            if ch == 'none':
                return False
            if ch == 'own':
                continue
            if ch == 'down':
                if c in r and res_perks > 0:
                    res_perks -= 1
                    continue
                if c in g and goods_perks > 0:
                    goods_perks -= 1
                    continue
            if ch == 'left':
                if c in left_res:
                    if left_res_discount and money >= 1:
                        left_res.remove(c)
                        money -= 1
                    elif money >= 2:
                        left_res.remove(c)
                        money -= 2
                    else:
                        return False
                elif c in left_goods:
                    if left_goods_discount and money >= 1:
                        left_goods.remove(c)
                        money -= 1
                    elif money >= 2:
                        left_goods.remove(c)
                        money -= 2
                    else:
                        return False
                else:
                    return False

            if ch == 'right':
                if c in right_res:
                    if right_res_discount and money >= 1:
                        right_res.remove(c)
                        money -= 1
                    elif money >= 2:
                        right_res.remove(c)
                        money -= 2
                    else:
                        return False
                elif c in right_goods:
                    if right_goods_discount and money >= 1:
                        right_goods.remove(c)
                        money -= 1
                    elif money >= 2:
                        right_goods.remove(c)
                        money -= 2
                    else:
                        return False
                else:
                    return False
        return True

    def can_build_wonder(self, chosen):
        self.can_build(1, chosen, wonder=True)

    def build(self, card):

        self.built_cards.append(card)

        if 1 in card.cost:
            self.money -= 1

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

        perks = self.wonder.perks[self.built_wonders]
        self.built_wonders += 1
        self.activate_perks(perks)

    def get_next_wonder_cost(self):
        if self.built_wonders == self.wonder.max_level:
            return []

        costs = []
        for c in self.wonder.costs[self.built_wonders]:
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
