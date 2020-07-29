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

class Constants(BaseConstants):
    name_in_url = 'umairs_experiment'
    players_per_group = 6
    num_rounds = 12
    marginal_payoff = 60
    matching_bonus_payoff = 10
    neighbors = [[2, 3, 4, 6], [1, 3, 4, 5], [1, 2, 5], [1, 2, 6], [2, 3], [1, 4]]
    q_1="True"
    q_2=12
    q_3=2
    q_4=4
    q_5 = "False"
    q_6 = "False"
    q_7 = "True"
    q_8 = "True"
    q_9 = "True"
    q_10 = "False"
    q_11=24
    q_12=35
    q_13="36 points = 1 US $"
    q_14="True"



    instructions_template = 'umairs_experiment/Instructions.html'

class Subsession(BaseSubsession):
    def creating_session(self):
        c_round = self.round_number-1
        for p in self.get_players():
            if p.id_in_group <= c_round:
                p.int_pref = "Y"
            else:
                p.int_pref = "X"


class Group(BaseGroup):
    def set_payoffs2(self):
        for p in self.get_players():
            neighbors = []
            for o in p.get_others_in_group():
                if o.id_in_group in Constants.neighbors[p.id_in_group-1]:
                    neighbors.append(o)
            matching_neighbors = []
            neighbor_reports = []
            for n in neighbors:
                neighbor_reports.append(n.exp_pref)
                if p.exp_pref == n.exp_pref:
                    matching_neighbors.append(n)
            p.neighbor_reports = ", ".join(neighbor_reports)
            p.payoff = Constants.marginal_payoff * (1 + len(matching_neighbors)) / (1 + len(neighbors))
            if p.int_pref != p.exp_pref:
                p.payoff = p.payoff - Constants.matching_bonus_payoff


class Player(BasePlayer):
    exp_pref = models.StringField(widget=widgets.RadioSelect, choices=["X", "Y"])
    int_pref = models.StringField()
    neighbor_reports = models.LongStringField()

    a_1 = models.StringField(widget=widgets.RadioSelect, choices=["True", "False"])
    a_2 = models.IntegerField(widget=widgets.RadioSelect, choices=[6, 10, 12, 20])
    a_3 = models.IntegerField(widget=widgets.RadioSelect, choices=[1, 2, 3, 4])
    a_4 = models.IntegerField(widget=widgets.RadioSelect, choices=[2, 3, 4, 5])
    a_5 = models.StringField(widget=widgets.RadioSelect, choices=["True", "False"])
    a_6 = models.StringField(widget=widgets.RadioSelect, choices=["True", "False"])
    a_7 = models.StringField(widget=widgets.RadioSelect, choices=["True", "False"])
    a_8 = models.StringField(widget=widgets.RadioSelect, choices=["True", "False"])
    a_9 = models.StringField(widget=widgets.RadioSelect, choices=["True", "False"])
    a_10 = models.StringField(widget=widgets.RadioSelect, choices=["True", "False"])
    a_11 = models.IntegerField(widget=widgets.RadioSelect, choices=[14, 24, 38, 48])
    a_12 = models.IntegerField(widget=widgets.RadioSelect, choices=[20, 30, 35, 45])
    a_13 = models.StringField(widget=widgets.RadioSelect, choices=["1 point = 26 US $", "1 point = 36 US $", "26 points = 1 US $", "36 points = 1 US $"])
    a_14 = models.StringField(widget=widgets.RadioSelect, choices=["True", "False"])

    s_1=models.StringField(widget=widgets.RadioSelect, choices=["Less than 18 years old", "18-24 years old", "25-34 years old", "35-44 years old", "45 years or older"])
    s_2=models.StringField(widget=widgets.RadioSelect, choices=["Male", "Female", "Other"])
    s_3=models.StringField(widget=widgets.RadioSelect, choices=["White", "Hispanic or Latino", "Black or African American", "Native American or American Indian", "Asian/Pacific Islander","Other"])
    s_4=models.StringField(widget=widgets.RadioSelect, choices=["Single, never married", "Married or domestic partnership", "Widowed", "Divorced", "Separated"])
