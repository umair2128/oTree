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
    name_in_url = 'appy'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    
    highest_bidder = models.IntegerField()
    highest_bid = models.CurrencyField(initial=0)

    def live_auction(self, id_in_group, bid):
        if bid > self.highest_bid:
            self.highest_bid = bid
            self.highest_bidder = id_in_group
            broadcast = {'id_in_group': id_in_group, 'bid': bid}
            return {0: broadcast}

    def live_slider(self, id_in_group, package):        
        broadcast = {"slider_value" : package["slider_value"], "disable": package["disable"]}
        return {0: broadcast}
        



class Player(BasePlayer):
    name = models.StringField()
    age = models.IntegerField()
    individual_judgment = models.IntegerField()
    mutual_judgment = models.IntegerField()

