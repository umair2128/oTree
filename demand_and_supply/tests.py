from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
from otree.api import Submission


class PlayerBot(Bot):
    def play_round(self):
        yield pages.Introduction
        import random

        self.bot_idle = random.randint(1,10)

        if self.player.id_in_group != self.bot_idle:
            yield pages.Bid, dict(bid_amount=round(random.uniform(0, 100),2))
        else:
            yield Submission(pages.Bid, dict(bid_amount=None), timeout_happened=True)

