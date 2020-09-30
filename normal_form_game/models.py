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
import ast, random

doc = """
This space for rent.
"""


class Constants(BaseConstants):
    name_in_url = 'normal_form_game'
    players_per_group = 2
    num_rounds = 100


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    def set_payoffs(self):
        row_player = self.get_player_by_role('row')
        col_player = self.get_player_by_role('col')
        payoffs = self.session.config['payoffs']

        # recording opp action in player model to make life easier later
        row_player.opp_action = col_player.own_action
        col_player.opp_action = row_player.own_action

        # and now we use the realized actions to look up payoffs
        row_player.own_payoff = payoffs[row_player.own_action][col_player.own_action][0]
        col_player.own_payoff = payoffs[row_player.own_action][col_player.own_action][1]

        # recording opp payoff in player model to make life easier later
        row_player.opp_payoff = col_player.own_payoff
        col_player.opp_payoff = row_player.own_payoff


class Player(BasePlayer):
    def role(self):
        if self.id_in_group == 1:
            return 'row'
        else:
            return 'col'

    action_distribution = models.StringField()

    own_action = models.IntegerField()
    opp_action = models.IntegerField()

    own_payoff = models.FloatField()
    opp_payoff = models.FloatField()


    def other_player(self):
        return self.get_others_in_group()[0]


    def vars_for_template(self):
        #Defining nested lists which store frequencies and proportions of players' actions for decision/waiting and result pages, respectively
        agg_res_inside = [[[0,0,0,0] for i in range(len(self.session.config['row_action_labels']))] for j in range(len(self.session.config['col_action_labels']))]
        agg_res_outside_row = [[0,0,0,0] for i in range(len(self.session.config['row_action_labels']))]
        agg_res_outside_col = [[0,0,0,0] for j in range(len(self.session.config['col_action_labels']))]

        row_player = self.group.get_player_by_role('row')

        #Assigning values for frequencies and proportions to the aggregate results list for each combination of row and
        # column player's actions (first pair of indices is for the decision/waiting page and the second for results page)
        for i in range(0, len(self.session.config['row_action_labels'])):
            for j in range(0, len(self.session.config['col_action_labels'])):
                if self.round_number != 1:
                    agg_res_inside[i][j][0] = sum(1 for p in row_player.in_previous_rounds() if p.own_action == i and p.opp_action == j)
                    agg_res_inside[i][j][1] = int(round(100 * (sum(1 for p in row_player.in_previous_rounds() if p.own_action == i and p.opp_action == j)) / (self.round_number-1)))
                agg_res_inside[i][j][2]= sum(1 for p in row_player.in_all_rounds() if p.own_action == i and p.opp_action== j )
                agg_res_inside[i][j][3]= int(round(100*(sum(1 for p in row_player.in_all_rounds() if p.own_action == i and p.opp_action == j))/self.round_number))

            # Assigning values for frequencies and proportions to the aggregate results list for each of row player's actions
            # (first pair of indices is for the decision/waiting page and the second for results page)
            if self.round_number != 1:
                agg_res_outside_row[i][0] = sum(1 for p in row_player.in_previous_rounds() if p.own_action == i)
                agg_res_outside_row[i][1] = int(round(100 * sum(1 for p in row_player.in_previous_rounds() if p.own_action == i) / (self.round_number - 1)))
            agg_res_outside_row[i][2] = sum(1 for p in row_player.in_all_rounds() if p.own_action == i)
            agg_res_outside_row[i][3] = int(round(100 * sum(1 for p in row_player.in_all_rounds() if p.own_action == i) / self.round_number))

        # Assigning values for frequencies and proportions to the aggregate results list for each of column player's actions
        # (first pair of indices is for the decision/waiting page and the second for results page)
        for j in range(0, len(self.session.config['col_action_labels'])):
            if self.round_number != 1:
                agg_res_outside_col[j][0] = sum(1 for p in row_player.in_previous_rounds() if p.opp_action == j)
                agg_res_outside_col[j][1] = int(round(100 * sum(1 for p in row_player.in_previous_rounds() if p.opp_action == j) / (self.round_number - 1)))
            agg_res_outside_col[j][2] = sum(1 for p in row_player.in_all_rounds() if p.opp_action == j)
            agg_res_outside_col[j][3] = int(round(100 * sum(1 for p in row_player.in_all_rounds() if p.opp_action == j) / self.round_number))

        return dict(
            agg_res_inside=agg_res_inside,
            agg_res_outside_row=agg_res_outside_row,
            agg_res_outside_col=agg_res_outside_col,
            total_payoff=sum(p.own_payoff for p in self.in_all_rounds() if p.own_payoff != None),
        )