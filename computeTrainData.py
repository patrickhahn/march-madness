import csv

# Load map of team+year to features
team_features = dict()
with open('data/TeamFeatures') as f:
    reader = csv.reader(f)
    for row in reader:
        team_features[row[2]+row[0]] = row[3:] # concatenate team id and year for keys

# Write out logistic regression training data from tournament games
with open('data/TourneyDetailedResults.csv') as tourney:
    tourney_reader = csv.DictReader(fin)
    with open('data/train.csv', 'w') as fout:
        write = csv.writer(fout)
        for row in tourney_reader:
