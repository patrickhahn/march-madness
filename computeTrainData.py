import csv

# Load map of team+year to features
team_features = dict()
with open('data/TeamFeatures.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        team_features[row[2]+row[0]] = row[3:] # concatenate team id and year for keys

# Write out logistic regression training data from tournament games
with open('data/TourneyDetailedResults.csv') as fin:
    tourney_reader = csv.DictReader(fin)
    with open('data/train.csv', 'w') as fout:
        writer = csv.writer(fout)
        team1win = True
        for row in tourney_reader:
            team1win = not team1win # alternate order of winning team to balance data
            if team1win:
                out_row = [1]
                out_row.extend(team_features[row['Wteam']+row['Season']])
                out_row.extend(team_features[row['Lteam']+row['Season']])
            else:
                out_row = [0]
                out_row.extend(team_features[row['Lteam']+row['Season']])
                out_row.extend(team_features[row['Wteam']+row['Season']])
            writer.writerow(out_row)
