import csv
import operator

import model

class Game:
    def __init__(self, teams, h2h_model):
        self.h2h_model = h2h_model
        self.teams = teams
        self.size = len(teams)
        self.half1 = teams[:(self.size/2)]
        self.half2 = teams[(self.size/2):]
        if self.size > 1:
            # Game objects for preceding tournament rounds
            self.semi1 = Game(self.half1, h2h_model)
            self.semi2 = Game(self.half2, h2h_model)

    def calculate_probs(self):
        if self.size == 1:
            self.advance_probs = {self.teams[0]: 1.0}
            return self.advance_probs
        else:
            # Get probability for each team to make it to this game
            half1_arrive = self.semi1.calculate_probs()
            half2_arrive = self.semi2.calculate_probs()

            # For each team, calculate probability of winning this game, then
            # multiply by probability of getting to this game to get probability
            # of advancing
            advance_probs = dict()
            for team in self.half1:
                advance_probs[team] = half1_arrive[team] * self.win_prob(team, half2_arrive)
            for team in self.half2:
                advance_probs[team] = half2_arrive[team] * self.win_prob(team, half1_arrive)
            # assert abs(sum(advance_probs.values()) - 1) < 0.01, "Distribution must sum to 1! %f" % sum(advance_probs.values())
            self.advance_probs = advance_probs
            return advance_probs

    def win_prob(self, team, opponents_arrive):
        # Probability of winning is the sum of win probabilities against each
        # possible opponent, weighted by the probability of each opponent making
        # it to this game
        win_prob = 0
        for opponent, arrival_prob in opponents_arrive.iteritems():
            win_prob += arrival_prob * self.h2h_model.win_prob(team, opponent)
        return win_prob

    def predict_winners(self, parent_winner):
        if parent_winner in self.teams:
            self.winner = parent_winner
        else:
            self.winner = max(self.advance_probs.iteritems(), key=operator.itemgetter(1))[0]
        if self.size > 1:
            self.semi1.predict_winners(self.winner)
            self.semi2.predict_winners(self.winner)

    def print_advance_probs(self):
        print "--------GAME--------"
        for team in self.teams:
            print "%s:\t\t%f" % (team, self.advance_probs[team])
        if self.size > 1:
            self.semi1.print_advance_probs()
            self.semi2.print_advance_probs()

def print_winners(final):
    queue = [(final, 0)]
    prev_round = 0
    while queue:
        tup = queue.pop(0)
        game = tup[0]
        cur_round = tup[1]

        if cur_round > prev_round:
            print "--------------------"
        prev_round = cur_round

        print game.winner
        if game.size > 1:
            queue.append((game.semi1, cur_round+1))
            queue.append((game.semi2, cur_round+1))

def main():
    with open('data/bracket2017.csv') as f:
        teams = []
        team_seeds = dict()
        reader = csv.reader(f)
        for row in reader:
            teams.append(row[0])
            team_seeds[row[0]] = float(row[1])

    h2h_model = model.LogRegModel(teams, '2016')
    h2h_model.train()

    bracket = Game(teams, h2h_model)
    bracket.calculate_probs()
    bracket.predict_winners("")
    print_winners(bracket)

if __name__ == "__main__": main()
