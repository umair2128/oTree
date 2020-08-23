from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)

author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'demand_and_supply'
    players_per_group = None
    num_rounds = 1

    instructions_template_d = 'demand_and_supply/Instructions_d.html'
    instructions_template_s = 'demand_and_supply/Instructions_s.html'


class Subsession(BaseSubsession):
    def vars_for_admin_report(self):
        if [float(p.bid_amount) for p in self.get_players() if p.bid_amount != None] != []:
            if 'demand' in self.session.config['experiment']:
                return dict(
                    nothing_to_report = False,
                    participants = self.get_players(),
                    exp_ended = max([float(p.payoff) for p in self.get_players()]),
                    num_players = len([p.id_in_group for p in self.get_players() if p.bid_amount != None]),
                    bids_smallest = float(min(p.bid_amount for p in self.get_players() if p.bid_amount != None)),
                    bids_largest = float(max(p.bid_amount for p in self.get_players() if p.bid_amount != None)),
                    bids_sorted = sorted([p.bid_amount for p in self.get_players() if p.bid_amount != None], reverse=True),
                    bids_graph = sorted([min(float(p.bid_amount) for p in self.get_players() if p.bid_amount != None)] + [float(p.bid_amount) for p in self.get_players() if p.bid_amount != None], reverse=True)
                    )
            else:
                return dict(
                    nothing_to_report = False,
                    participants = self.get_players(),
                    exp_ended = max([float(p.payoff) for p in self.get_players()]),
                    num_players = len([p.id_in_group for p in self.get_players() if p.bid_amount != None]),
                    bids_smallest = float(min(p.bid_amount for p in self.get_players() if p.bid_amount != None)),
                    bids_largest = float(max(p.bid_amount for p in self.get_players() if p.bid_amount != None)),
                    bids_sorted = sorted([p.bid_amount for p in self.get_players() if p.bid_amount != None], reverse=False),
                    bids_graph = sorted([max(float(p.bid_amount) for p in self.get_players() if p.bid_amount != None)] + [float(p.bid_amount) for p in self.get_players() if p.bid_amount != None], reverse=False)
                    )
        else:
            return dict(
                nothing_to_report = True,
                num_players=0
            )


class Group(BaseGroup):
    highest_bid = models.CurrencyField()
    lowest_bid = models.CurrencyField()

    def set_winner(self):
        if [float(p.bid_amount) for p in self.get_players() if p.bid_amount != None] != []:
            import random
            players = self.get_players()

            if 'demand' in self.session.config['experiment']:
                self.highest_bid = max([p.bid_amount for p in players if p.bid_amount != None])
                players_with_highest_bid = [p for p in players if p.bid_amount == self.highest_bid]
                winner = random.choice(players_with_highest_bid)
                winner.is_winner = True
            else:
                self.lowest_bid = min([p.bid_amount for p in players if p.bid_amount != None])
                players_with_lowest_bid = [p for p in players if p.bid_amount == self.lowest_bid]
                winner = random.choice(players_with_lowest_bid)
                winner.is_winner = True

            for p in players:
                p.set_payoff()


class Player(BasePlayer):
    bid_amount = models.CurrencyField()
    is_winner = models.BooleanField(initial=False)

    def set_payoff(self):
        if self.is_winner:
            self.payoff = self.bid_amount
        else:
            self.payoff = 0