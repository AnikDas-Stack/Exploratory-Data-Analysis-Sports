# Importing Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Importing Dataset
matches = pd.read_csv("matches.csv")
deliveries = pd.read_csv("deliveries.csv")

# Grouping Based on Season & Making List of all seasons(Dataframe)
grouped = matches.groupby(['season'])
season_list = []

for i in range(2008, 2020, +1):
    temp_season = grouped.get_group(i)
    season_list.append(temp_season)

pointTable_list = []


# Operation
for df in season_list:
    Table1= pd.DataFrame(columns = ['Team'])

    f = df.first_valid_index()
    l = df.last_valid_index()
    
    for i in range(f, l+1, +1):
        if df.team1[i] not in Table1.values:
            Table1 = Table1.append({'Team': df.team1[i]}, ignore_index = True) 
      
        if df.team2[i] not in Table1.values:
            Table1 = Table1.append({'Team': df.team2[i]}, ignore_index = True)
            
    Table2= pd.DataFrame(np.full((len(Table1.Team), 4), 0), columns = ['Played', 'Won', 'Lost', 'No_Result'])

            
    for i in range(f, l+1, +1):
        if df.winner[i] == df.team1[i]:
            for j in range(0, len(Table1.Team), +1):
                if Table1.Team[j] == df.winner[i]:
                    Table2.Played[j] = Table2.Played[j] + 1
                    Table2.Won[j] = Table2.Won[j] + 1

                if Table1.Team[j] == df.team2[i]:
                    Table2.Played[j] = Table2.Played[j] + 1
                    Table2.Lost[j] = Table2.Lost[j] + 1
                
        elif df.winner[i] == df.team2[i]:
            for j in range(0, len(Table1.Team), +1):
                if Table1.Team[j] == df.winner[i]:
                    Table2.Played[j] = Table2.Played[j] + 1
                    Table2.Won[j] = Table2.Won[j] + 1       

                if Table1.Team[j] == df.team1[i]:
                    Table2.Played[j] = Table2.Played[j] + 1
                    Table2.Lost[j] = Table2.Lost[j] + 1
                
        else:
            for j in range(0, len(Table1.Team), +1):
                if Table1.Team[j] == df.team1[i]:
                    Table2.Played[j] = Table2.Played[j] + 1
                    Table2.No_Result[j] = Table2.No_Result[j] + 1

                if Table1.Team[j] == df.team2[i]:
                    Table2.Played[j] = Table2.Played[j] + 1
                    Table2.No_Result[j] = Table2.No_Result[j] + 1
        
    newTable = pd.concat([Table1, Table2], axis = 1, ignore_index = False)
    pointTable_list.append(newTable)
    

IPL_Points_Table = {"Season_2008": pointTable_list[0], "Season_2009": pointTable_list[1],
                    "Season_2010": pointTable_list[2], "Season_2011": pointTable_list[3],
                    "Season_2012": pointTable_list[4], "Season_2013": pointTable_list[5],
                    "Season_2014": pointTable_list[6], "Season_2015": pointTable_list[7],
                    "Season_2016": pointTable_list[8], "Season_2017": pointTable_list[9],
                    "Season_2018": pointTable_list[10], "Season_2019": pointTable_list[11],}
                                                                                           

#################################################################################################################

# Win or Loss based on toss
toss = pd.DataFrame(np.full((1, 2), 0), columns = ['toss_winner_won', 'toss_winner_lost'])

for a, b, c in zip(matches.toss_winner, matches.winner, matches.result):
    if c != 'no result':
        if a == b:
            toss.toss_winner_won += 1
        else:
            toss.toss_winner_lost += 1
            
            
# Win or Loss based on toss winning and decision making
when_team_won = pd.DataFrame(np.full((1, 2), 0), columns = ['Win_toss_and_Chasing', 'Win_toss_and_Batting_First'])

for a, b, c, d in zip(matches.toss_winner, matches.winner, matches.result, matches.toss_decision):
    if c!= 'no result':
        if a == b and d == 'field':
            when_team_won.Win_toss_and_Chasing += 1
        if a == b and d == 'bat':
            when_team_won.Win_toss_and_Batting_First += 1
            
when_team_won.to_csv('when_team_won.csv')
            

# Win or Loss based on opening partnership
win_loss_on_partnership = pd.DataFrame(np.full((1, 2), 0), columns = ['Fifty_or_Fifty_Plus_and_Won',\
                                                                      'Fifty_or_Fifty_Plus_but_Lost']) 
    
for a, b in zip(matches.id, matches.winner):
    grouped = deliveries[deliveries['match_id'] == a]
    team1_opening = 0
    team2_opening = 0
    
    
    for i, j ,l, m in zip(grouped.inning, grouped.player_dismissed, grouped.batting_team, grouped.total_runs):
        if i == 1 and pd.isnull(j) == True:
            team1 = l
            team1_opening += m
        if pd.isnull(j) == False:
            break
        
    for i, j, l, m in zip(grouped.inning, grouped.player_dismissed, grouped.batting_team, grouped.total_runs):
        if i == 2 and pd.isnull(j) == False:
            break
        if i == 2 and pd.isnull(j) == True:
            team2 = l
            team2_opening += m
    
    if team1_opening >= 50:
        if b == team1:
            win_loss_on_partnership.Fifty_or_Fifty_Plus_and_Won += 1
        if b != team1 and pd.isnull(b) == False:
            win_loss_on_partnership.Fifty_or_Fifty_Plus_but_Lost += 1
            
    if team2_opening >= 50:
        if b == team2:
            win_loss_on_partnership.Fifty_or_Fifty_Plus_and_Won += 1
        if b != team2 and pd.isnull(b) == False:
            win_loss_on_partnership.Fifty_or_Fifty_Plus_but_Lost += 1

win_loss_on_partnership.to_csv('win_loss_on_opening_partnership.csv')            

# Most successful team who played at least 70 matches
temp_table = pd.concat(pointTable_list, axis = 0, ignore_index = True) 
unique_team = pd.DataFrame(temp_table['Team'].unique(), columns = ['Team'])
team_result = pd.DataFrame(np.full((len(unique_team), 5), 0), columns = ['Played', 'Won', 'Lost', 'No_Result', 'Winning_Percentage'])
unique_team = pd.concat([unique_team, team_result], axis = 1, ignore_index = False) 

temp_group = temp_table.groupby('Team')
for i in range(0, len(unique_team), +1):
    var = temp_group.get_group(unique_team.Team[i]).reset_index(drop = True)
    unique_team.Played[i] = var.Played.sum()
    unique_team.Won[i] = var.Won.sum()
    unique_team.Lost[i] = var.Lost.sum()
    unique_team.No_Result[i] = var.No_Result.sum()
    
    unique_team['Winning_Percentage'] = unique_team['Winning_Percentage'].astype(float)
    unique_team.Winning_Percentage[i] = round((unique_team.Won[i] / unique_team.Played[i]) * 100.00, 2)

final_ranking = unique_team[unique_team['Played'] >= 70]
final_ranking = final_ranking.sort_values(['Winning_Percentage'], ascending = False)

final_ranking.to_csv('Ranking.csv')