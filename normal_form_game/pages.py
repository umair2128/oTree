import ast
import random

from ._builtin import Page, WaitPage


class Introduction(Page):
    def get_timeout_seconds(self):
        return self.session.config['timeout_intro']

    timer_text = 'Time remaining to read instructions:'

    def is_displayed(self):
        return self.round_number == 1



class Decision(Page):
    def get_timeout_seconds(self):
        return self.session.config['timeout_decision']

    form_model = 'player'
    form_fields = ['action_distribution']

    def before_next_page(self):
        # add automated strategy profile if human did not submit
        if self.timeout_happened:
            if self.player.id_in_group == 1:
                self.player.action_distribution = self.session.config['row_automated_strategy']
            else:
                self.player.action_distribution = self.session.config['col_automated_strategy']
        # realize an action from strategy profile
        dist = ast.literal_eval(self.player.action_distribution)
        self.player.own_action = random.choices(population=list(range(len(dist))), weights=dist)[0]

    def vars_for_template(self):
        return dict(
        self.player.vars_for_template(),
        payoffs=self.session.config['payoffs'],
        row_action_labels=self.session.config['row_action_labels'],
        col_action_labels=self.session.config['col_action_labels'],
        )


class IntroWait(WaitPage):
    def is_displayed(self):
        return self.round_number == 1

    title_text = "Experiment starting soon"
    body_text = "Please wait for others to finish reading instructions"


class Wait(WaitPage):
    template_name = 'normal_form_game/Wait.html'

    def vars_for_template(self):
        return dict(
            self.player.vars_for_template(),
            payoffs=self.session.config['payoffs'],
            row_action_labels=self.session.config['row_action_labels'],
            col_action_labels=self.session.config['col_action_labels'],
            choice=self.player.own_action,
        )

    after_all_players_arrive = 'set_payoffs'


class Results(Page):
    def get_timeout_seconds(self):
        return self.session.config['timeout_result']

    timer_text = 'Time remaining to view results:'

    def vars_for_template(self):
        return dict(
            self.player.vars_for_template(),
            payoffs=self.session.config['payoffs'],
            row_action_labels=self.session.config['row_action_labels'],
            col_action_labels=self.session.config['col_action_labels'],
        )


class AggResults(Page):
    def is_displayed(self):
        return self.round_number == self.session.config['total_rounds']

    def vars_for_template(self):
        return dict(
            self.player.vars_for_template(),
            payoffs=self.session.config['payoffs'],
            row_action_labels=self.session.config['row_action_labels'],
            col_action_labels=self.session.config['col_action_labels'],
        )


page_sequence = [Introduction, IntroWait, Decision, Wait, Results, AggResults]
