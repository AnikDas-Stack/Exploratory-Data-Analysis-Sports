# Importing Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Importing Dataset
deliveries = pd.read_csv("deliveries.csv")
matches = pd.read_csv("matches.csv")

# Creating DataFrame for temporary works
allBatsman = pd.DataFrame(deliveries["batsman"].unique(), columns = ['batsman'])
info = pd.DataFrame(np.full((len(allBatsman.batsman), 11), 0), columns = ["Innings","Not_Out", 
"Total_Runs", "Ball_Faced","Average", "Fours", "Sixes", "Strike_Rate", "Highest_Run", "Fifties", "Hundreds"])


# Making List of DataFrames for Each Player
players = []
grouped = deliveries.groupby('batsman')
for x in allBatsman.batsman:
    temp = grouped.get_group(x).reset_index(drop = True)
    players.append(temp)

dismiss = []
cate = pd.DataFrame(deliveries['dismissal_kind'].unique(), columns=['kind'])
cate = cate.drop(cate.index[0])
filtered = deliveries[deliveries['is_super_over'] == 0]
grouped_2 = filtered.groupby('dismissal_kind')
for x in cate.kind:
    temp = grouped_2.get_group(x).reset_index(drop = True)
    dismiss.append(temp)
final_dismiss = pd.concat(dismiss, ignore_index = False)

   
# Operation
for i in range(0, len(players), +1):     
    info.Innings[i] = len(players[i].match_id.unique())
    
    for j, k, l in zip(players[i].is_super_over, players[i].batsman_runs, players[i].wide_runs):
        if j == 0 and k != 0 and l == 0:
            info.Total_Runs[i] += k
            
    for j, k in zip(players[i].is_super_over, players[i].wide_runs):
        if j == 0 and k == 0:
            info.Ball_Faced[i] = info.Ball_Faced[i] + 1
    
    for j, k, l in zip(players[i].is_super_over, players[i].batsman_runs, players[i].wide_runs):
        if j == 0 and k == 4 and l == 0:
            info.Fours[i] = info.Fours[i] + 1
        elif j == 0 and k == 6 and l == 0:
            info.Sixes[i] = info.Sixes[i] + 1
    
    info['Strike_Rate'] = info['Strike_Rate'].astype(float)
    info.Strike_Rate[i] = round((info.Total_Runs[i] / info.Ball_Faced[i]) * 100.00, 2)
    
    match_out = 0
    y = players[i].batsman[0]
    for j in final_dismiss.player_dismissed:
        if j == y:
            match_out += 1
    
    info.Not_Out[i] = info.Innings[i] - match_out
    
    info['Average'] = info['Average'].astype(float)
    info.Average[i] = round((info.Total_Runs[i] / match_out), 2)
     
    
    match = []
    uniqMatch = pd.DataFrame(players[i].match_id.unique(), columns = ['m_id'])
    
    grouped_2 = players[i].groupby('match_id')
    for x in uniqMatch.m_id:
        temp_2 = grouped_2.get_group(x).reset_index(drop = True)
        match.append(temp_2)
    
    match_f = 0
    match_h = 0
    highest_run = 0
    
    for u in match:
        match_run = 0
        
        for j, k, l in zip(u.is_super_over, u.batsman_runs, u.wide_runs):
            if j == 0 and k != 0 and l == 0:
                match_run += k
                
        if match_run >= 50 and match_run < 100:
            match_f += 1
        elif match_run >= 100:
            match_h += 1
        
        if match_run >= highest_run:
            highest_run = match_run
    
    info.Highest_Run[i] = highest_run
    info.Fifties[i] = match_f
    info.Hundreds[i] = match_h

# Making Final DataFrame
Batsman_Stat = pd.concat([allBatsman, info], axis = 1, ignore_index = False)   
Batsman_Stat = Batsman_Stat.sort_values(['Total_Runs', 'Strike_Rate'], ascending = False)
#Batsman_Stat = Batsman_Stat.sort_values('batsman', ascending = True)


