from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

class Introduction(Page):
    pass

class Bid(Page):
    def get_timeout_seconds(self):
            return (self.session.config['timeout'])

    form_model = 'player'
    form_fields = ['bid_amount']

    def before_next_page(self):
        if self.timeout_happened:
            self.player.bid_amount = None


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = 'set_winner'


class Results(Page):

    def js_vars(self):
        if [float(p.bid_amount) for p in self.group.get_players() if p.bid_amount != None] != []:
            players = self.group.get_players()

            if 'demand' in self.session.config['experiment']:
                return dict(
                    nothing_to_report = False,
                    num_players = len([p.id_in_group for p in players if p.bid_amount != None]),
                    player_bid = self.player.bid_amount,
                    bids_smallest = min(p.bid_amount for p in players if p.bid_amount != None),
                    bids_largest = max(p.bid_amount for p in players if p.bid_amount != None),
                    player_position = sorted([p.bid_amount for p in players if p.bid_amount != None], reverse=True).index(self.player.bid_amount) + 1 if self.player.bid_amount != None else 0,
                    bids_sorted = sorted([p.bid_amount for p in players if p.bid_amount != None], reverse = True),
                    bids_graph = sorted([min(p.bid_amount for p in players if p.bid_amount != None)] + [p.bid_amount for p in players if p.bid_amount != None], reverse=True)
                )
            else:
                return dict(
                    nothing_to_report = False,
                    num_players = len([p.id_in_group for p in players if p.bid_amount != None]),
                    player_bid = self.player.bid_amount,
                    player_position = sorted([p.bid_amount for p in players if p.bid_amount != None], reverse=False).index(self.player.bid_amount) + 1 if self.player.bid_amount != None else 0,
                    bids_smallest = min(p.bid_amount for p in players if p.bid_amount != None),
                    bids_largest = max(p.bid_amount for p in players if p.bid_amount != None),
                    bids_sorted = sorted([p.bid_amount for p in players if p.bid_amount != None], reverse=False),
                    bids_graph = sorted([max(p.bid_amount for p in players if p.bid_amount != None)] + [p.bid_amount for p in players if p.bid_amount != None], reverse=False)
                )
        else:
            return dict(
                nothing_to_report = True
            )

page_sequence = [Introduction, Bid, ResultsWaitPage, Results]
