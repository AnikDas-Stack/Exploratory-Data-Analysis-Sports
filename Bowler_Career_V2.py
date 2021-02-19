# Importing Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Importing Dataset
deliveries = pd.read_csv("deliveries.csv")

# Creating DataFrame for temporary works
allBowler = pd.DataFrame(deliveries["bowler"].unique(), columns = ['bowler'])
info = pd.DataFrame(np.full((len(allBowler.bowler), 6), 0), columns = ["Played", "Wickets", "Balls",
                                                            "Runs_Given", "Economy", "Best_Figure"])

# Making List of DataFrames for Each Player
players = []
grouped = deliveries.groupby('bowler')
for x in allBowler.bowler:
    temp = (grouped.get_group(x)).reset_index(drop = True)
    players.append(temp)

# Operation
for i in range(0, len(players), +1):
    info.Played[i] = len(players[i].match_id.unique())
    
    for j in range(0, len(players[i]), +1):
        if pd.isnull(players[i].player_dismissed[j]) == False and players[i].is_super_over[j] == 0:
            kind = players[i].dismissal_kind[j]
            if  kind != 'run out' and kind != 'retired hurt' and kind != 'obstructing the field':
                info.Wickets[i] += 1
            
        if players[i].wide_runs[j] == 0 and players[i].noball_runs[j] == 0 and players[i].is_super_over[j] == 0:
            info.Balls[i] += 1
            
        if players[i].is_super_over[j] == 0 and (players[i].wide_runs[j] != 0 or players[i].noball_runs[j] != 0):
            #info.Runs_Given[i] += players[i].wide_runs[j]+players[i].noball_runs[j]+players[i].batsman_runs[j]
            info.Runs_Given += 1
        elif players[i].is_super_over[j] == 0 and players[i].batsman_runs[j] != 0:
            info.Runs_Given += players[i].batsman_runs[j]


    info['Economy'] = info['Economy'].astype(float)
    info.Economy[i] = float(info.Runs_Given[i] / (info.Balls[i] / 6.00))
    info = info.round({'Economy': 2})
    
    match = []
    uniqMatch = pd.DataFrame(players[i].match_id.unique(), columns = ['m_id'])
    
    grouped_2 = players[i].groupby('match_id')
    for x in uniqMatch.m_id:
        temp_2 = (grouped_2.get_group(x)).reset_index(drop = True)
        match.append(temp_2)
    
    wic = 0
    run = 0
    for u in match:
        temp_wic = 0
        temp_run = 0
        
        for j in range(0, len(u), +1):
            if pd.isnull(u.player_dismissed[j]) == False and u.is_super_over[j] == 0:
                kind = u.dismissal_kind[j]
                if  kind != 'run out' and kind != 'retired hurt' and kind != 'obstructing the field':
                    temp_wic += 1
            if u.is_super_over[j] == 0 and (u.wide_runs[j] != 0 or u.noball_runs[j] != 0):
                #temp_run += u.wide_runs[j]+u.noball_runs[j]+u.batsman_runs[j]
                temp_run += 1
            elif u.is_super_over[j] == 0 and u.batsman_runs[j] != 0:
                temp_run += u.batsman_runs[j]

            
        if temp_wic > wic:
            wic = temp_wic
            run = temp_run
        elif temp_wic == wic:
            if temp_run <= run:
                run = temp_run
                 
    info.Best_Figure[i] = str(wic) + "/" + str(run)          
        
# Making Final DataFrame
Bowler_Stat = pd.concat([allBowler, info], axis = 1, ignore_index = False)   
Bowler_Stat = Bowler_Stat.sort_values('Wickets', ascending = False)

