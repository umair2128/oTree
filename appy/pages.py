from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

class MyPage(Page):
    live_method = 'live_auction'
    
    form_model = 'player'
    #form_fields = ['name', 'age']

class Page_2(Page):
    form_model = 'player'

    form_fields = ['individual_judgment']

class Page_3(Page):
    form_model = 'player'

    form_fields = ['mutual_judgment']

    live_method = "live_slider"


class Results(Page):
    pass


page_sequence = [
    MyPage,
    Page_2,
    Page_3
]
