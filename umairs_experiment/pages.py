from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

class Welcome(Page):
    def is_displayed(self):
        return self.round_number == 1

class Quiz(Page):
    def is_displayed(self):
        return self.round_number == 1
    form_model = 'player'
    form_fields = ['a_1', 'a_2', 'a_3', 'a_4', 'a_5', 'a_6', 'a_7', 'a_8', 'a_9', 'a_10','a_11', 'a_12', 'a_13', 'a_14']

class Quiz_Result(Page):
    def is_displayed(self):
        return self.round_number == 1
    form_model = 'player'

    def vars_for_template(self):
        self.subsession.get_players()
        return dict(
            a_1=self.player.a_1,
            a_2=self.player.a_2,
            a_3=self.player.a_3,
            a_4=self.player.a_4,
            a_5=self.player.a_5,
            a_6=self.player.a_6,
            a_7=self.player.a_7,
            a_8=self.player.a_8,
            a_9=self.player.a_9,
            a_10=self.player.a_10,
            a_11=self.player.a_11,
            a_12=self.player.a_12,
            a_13=self.player.a_13,
            a_14=self.player.a_14,
        )


class Contribute(Page):
    form_model = 'player'
    form_fields = ['exp_pref']

    def vars_for_template(self):
        player_in_all_rounds = self.player.in_all_rounds()
        return dict(
            image_path='umairs_experiment/{}.png'.format(self.player.id_in_group),
            total_payoff=sum([p.payoff for p in player_in_all_rounds]),
            player_in_all_rounds=player_in_all_rounds,
            prev_rounds=self.subsession.round_number-1,
        )


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = 'set_payoffs2'


class Results(Page):
    def vars_for_template(self):
        self.subsession.get_players()
        player_in_all_rounds = self.player.in_all_rounds()
        return dict(
            exp_pref_1=self.group.get_player_by_id(1).exp_pref,
            exp_pref_2=self.group.get_player_by_id(2).exp_pref,
            exp_pref_3=self.group.get_player_by_id(3).exp_pref,
            exp_pref_4=self.group.get_player_by_id(4).exp_pref,
            exp_pref_5=self.group.get_player_by_id(5).exp_pref,
            exp_pref_6=self.group.get_player_by_id(6).exp_pref,
            total_payoff=sum([p.payoff for p in player_in_all_rounds]),
            player_in_all_rounds=player_in_all_rounds,
        )

class Survey(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds
    form_model = 'player'
    form_fields = ['s_1', 's_2', 's_3', 's_4']

class Results_Summary(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):
        self.subsession.get_players()
        player_in_all_rounds = self.player.in_all_rounds()
        return dict(
            total_payoff=sum([p.payoff for p in player_in_all_rounds]),
            total_cash_payoff=self.participant.payoff_plus_participation_fee()-4,
            player_in_all_rounds=player_in_all_rounds,
        )


page_sequence = [Welcome, Quiz, Quiz_Result, Contribute, ResultsWaitPage, Results, Survey, Results_Summary]

