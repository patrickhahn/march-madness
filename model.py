import csv
from sklearn.linear_model import LogisticRegression

class SeedModel:
    def __init__(self, seeds):
        self.seeds = seeds

    def win_prob(self, team, opponent):
        return self.seeds[opponent] / (self.seeds[team] + self.seeds[opponent])

class LogRegModel:
    def __init__(self, teams):
        self.teams = teams
        self.compute_features()

    def compute_features(self):
