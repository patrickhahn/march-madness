from __future__ import division
import csv

# Load id numbers for each team
team_ids = dict()
with open('data/Teams.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        team_ids[row['Team_Name']] = row['Team_Id']

# Get list of seasons
seasons = ['2003','2004','2005','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015','2016']

# Compute statistics for each team in each season to use as model features
with open('data/TeamFeatures.csv', 'w') as fout:
    fieldnames = ['Season','Team','Id','WinPct','PPG','OppPPG','3PAPG','3PPct','FTPG','FTPct','OffReboundPct','DefReboundPct','AstPG','ToPG','StPG','BlkPG','FoulPG']
    writer = csv.DictWriter(fout, fieldnames=fieldnames)
    writer.writeheader()

    for year in seasons:
        with open('data/RegularSeasonDetailedResults.csv') as fin:
            reader = csv.DictReader(fin)
            season = [row for row in reader if row['Season'] == year]
            for team, tid in team_ids.iteritems():
                features = {'Season':year,'Team':team,'Id':tid}

                won_games = [row for row in season if row['Wteam'] == tid]
                lost_games = [row for row in season if row['Lteam'] == tid]
                games_played = len(won_games) + len(lost_games)
                if games_played == 0:
                    continue
                features['WinPct'] = len(won_games) / games_played

                team_points = 0
                opp_points = 0
                three_pt_att = 0
                three_pt_made = 0
                free_throw_att = 0
                free_throw_made = 0
                team_off_rebounds = 0
                opp_off_rebounds = 0
                team_def_rebounds = 0
                opp_def_rebounds = 0
                assists = 0
                turnovers = 0
                steals = 0
                blocks = 0
                fouls = 0
                for game in won_games:
                    team_points += int(game['Wscore'])
                    opp_points += int(game['Lscore'])
                    three_pt_att += int(game['Wfga3'])
                    three_pt_made += int(game['Wfgm3'])
                    free_throw_att += int(game['Wfta'])
                    free_throw_made += int(game['Wftm'])
                    team_off_rebounds += int(game['Wor'])
                    team_def_rebounds += int(game['Wdr'])
                    assists += int(game['Wast'])
                    turnovers += int(game['Wto'])
                    steals += int(game['Wstl'])
                    blocks += int(game['Wblk'])
                    fouls += int(game['Wpf'])
                    opp_off_rebounds += int(game['Lor'])
                    opp_def_rebounds += int(game['Ldr'])
                for game in lost_games:
                    team_points += int(game['Lscore'])
                    opp_points += int(game['Wscore'])
                    three_pt_att += int(game['Lfga3'])
                    three_pt_made += int(game['Lfgm3'])
                    free_throw_att += int(game['Lfta'])
                    free_throw_made += int(game['Lftm'])
                    team_off_rebounds += int(game['Lor'])
                    team_def_rebounds += int(game['Ldr'])
                    assists += int(game['Last'])
                    turnovers += int(game['Lto'])
                    steals += int(game['Lstl'])
                    blocks += int(game['Lblk'])
                    fouls += int(game['Lpf'])
                    opp_off_rebounds += int(game['Wor'])
                    opp_def_rebounds += int(game['Wdr'])
                features['PPG'] = team_points / games_played
                features['OppPPG'] = opp_points / games_played
                features['3PAPG'] = three_pt_att / games_played
                features['3PPct'] = three_pt_made / three_pt_att
                features['FTPG'] = free_throw_att / games_played
                features['FTPct'] = free_throw_made / free_throw_att
                features['OffReboundPct'] = team_off_rebounds / (team_off_rebounds + opp_def_rebounds)
                features['DefReboundPct'] = team_def_rebounds / (team_def_rebounds + opp_off_rebounds)
                features['AstPG'] = assists / games_played
                features['ToPG'] = turnovers / games_played
                features['StPG'] = steals / games_played
                features['BlkPG'] = blocks / games_played
                features['FoulPG'] = fouls / games_played
                writer.writerow(features)

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
