import csv
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

class Model(object):
    def __init__(self, teams, year):
        self.features = dict()
        with open('data/TeamFeatures.csv') as f:
            reader = csv.DictReader(f, fieldnames=['Season','Team','Id'], restkey='features')
            for row in reader:
                if row['Season'] == year and row['Team'] in teams:
                    self.features[row['Team']] = map(float, row['features'])

class SeedModel(object): # just used for testing
    def __init__(self, seeds):
        self.seeds = seeds

    def win_prob(self, team, opponent):
        return self.seeds[opponent] / (self.seeds[team] + self.seeds[opponent])

class LogRegModel(Model):
    def __init__(self, teams, year):
        super(LogRegModel, self).__init__(teams, year)

    def train(self):
        with open('data/train.csv') as f:
            reader = csv.reader(f)
            data = np.array([map(float,row) for row in reader])
            y = data[:,0]
            X = data[:,1:]

            # Standardize features and save scaling parameters to use for predictions
            self.scaler = StandardScaler().fit(X)
            X = self.scaler.transform(X)

            self.model = LogisticRegression(C=100, penalty='l2', fit_intercept=False)
            self.model.fit(X, y)

            print self.model.intercept_
            print self.model.coef_
            print self.model.classes_

    def win_prob(self, team1, team2):
        X = np.array(self.features[team1] + self.features[team2])[np.newaxis]
        X = self.scaler.transform(X) # standardize features
        return self.model.predict_proba(X)[0][1] # get probability of class 1 (team1 wins)

class RandomForestModel(Model):
    def __init__(self, teams, year):
        super(RandomForestModel, self).__init__(teams, year)

    def train(self):
        with open('data/train.csv') as f:
            reader = csv.reader(f)
            data = np.array([map(float,row) for row in reader])
            y = data[:,0]
            X = data[:,1:]

            self.model = RandomForestClassifier(n_estimators=20)
            self.model.fit(X,y)

            print self.model.classes_

    def win_prob(self, team1, team2):
        X = np.array(self.features[team1] + self.features[team2])[np.newaxis]
        prob = self.model.predict_proba(X)[0] # get probability of class 1 (team1 wins)
        # print prob
        return prob[1]
