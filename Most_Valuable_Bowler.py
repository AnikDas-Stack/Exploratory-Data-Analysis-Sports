# Importing Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Importing Dataset
deliveries = pd.read_csv("deliveries.csv")

# Creating DataFrame for temporary works
allBowler = pd.DataFrame(deliveries["bowler"].unique(), columns = ['bowler'])
info = pd.DataFrame(np.full((len(allBowler.bowler), 9), 0), columns = ["Innings", "Wickets", "Balls",
                  "Runs_Given", "Economy", "Best_Figure","Average", "Three_Wickets", "Five_Wickets"])

# Making List of DataFrames for Each Player
players = []
grouped = deliveries.groupby('bowler')
for x in allBowler.bowler:
    temp = (grouped.get_group(x)).reset_index(drop = True)
    players.append(temp)


# Operation
for i in range(0, len(players), +1):
    info.Innings[i] = len(players[i].match_id.unique())
    
    for p, q, r in zip(players[i].player_dismissed, players[i].is_super_over, players[i].dismissal_kind):
        if pd.isnull(p) == False and q == 0:
            if  r != 'run out' and r != 'retired hurt' and r != 'obstructing the field':
                info.Wickets[i] += 1 

    for j, k, l in zip(players[i].wide_runs, players[i].noball_runs, players[i].is_super_over):
        if (j == 0 and k == 0) and l == 0:
            info.Balls[i] = info.Balls[i] + 1
    
    for p, q, r, s, t in zip(players[i].is_super_over, players[i].wide_runs, players[i].noball_runs,\
    players[i].batsman_runs, players[i].penalty_runs):
        #info.Runs_Given[i] = info.Runs_Given[i] + t
        if p == 0 and q != 0:
            info.Runs_Given[i] = info.Runs_Given[i] + q
        if p == 0 and r != 0:
            info.Runs_Given[i] = info.Runs_Given[i] + r
        if p == 0 and s != 0 and q == 0:
            info.Runs_Given[i] = info.Runs_Given[i] + s
        
    
    info['Economy'] = info['Economy'].astype(float)
    info.Economy[i] = float(info.Runs_Given[i] / (info.Balls[i] / 6.00))
    info = info.round({'Economy': 2})
    
    match = []
    uniqMatch = pd.DataFrame(players[i].match_id.unique(), columns = ['m_id'])
    
    grouped_2 = players[i].groupby('match_id')
    for x in uniqMatch.m_id:
        temp_2 = grouped_2.get_group(x)
        match.append(temp_2)
    
    wic = 0
    run = 0
    wicket_3 = 0
    wicket_5 = 0
    
    for u in match:
        temp_wic = 0
        temp_run = 0
        
        for p, q, r, s in zip(u.player_dismissed, u.is_super_over, u.dismissal_kind, u.noball_runs):
            if pd.isnull(p) == False and q == 0 and s == 0:
                if  r != 'run out' and r != 'retired hurt' and r != 'obstructing the field':
                    temp_wic += 1

        for p, q, r, s in zip(u.is_super_over, u.wide_runs, u.noball_runs, u.batsman_runs):
            if p == 0 and (q != 0 or r != 0):
                temp_run = temp_run + 1
            elif p == 0 and s != 0:
                temp_run = temp_run + s
                
        if temp_wic > wic:
            wic = temp_wic
            run = temp_run
        elif temp_wic == wic:
            if temp_run <= run:
                run = temp_run
                
        if temp_wic >= 3 and temp_wic < 5:
            wicket_3 += 1
        elif temp_wic >= 5:
            wicket_5 += 1
                
    info.Best_Figure[i] = str(wic) + "/" + str(run) 
    info['Average'] = info['Average'].astype(float)
    info.Average[i] = round(info.Runs_Given[i] / info.Wickets[i], 2)
    info.Three_Wickets[i] = wicket_3
    info.Five_Wickets[i] = wicket_5     
        
# Making Final DataFrame
Bowler_Stat = pd.concat([allBowler, info], axis = 1, ignore_index = False)   
Bowler_Stat = Bowler_Stat.sort_values('Wickets', ascending = False)
#Bowler_Stat = Bowler_Stat.sort_values('bowler', ascending = True)

Bowler_Stat.to_csv("Bowler_Ranking.csv")