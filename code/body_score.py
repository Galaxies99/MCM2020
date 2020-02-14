from math import sqrt
import csv

events = []
name = {}
player = [[0, 0, 0, 0, 0, 0, [], [], [], 0] for i in range(35)]
speed = [0]*35
speedscore = [0]*35
airscore = [0]*35
attscore = [0]*35
looscore = [0]*35
air = [0]*35
attack = [0]*35
loose = [0]*35
score = [0]*35
length = 105
width = 68
u = 0

with open('../data/fullevents.csv') as csv_file:
    csv_reader = csv.reader(csv_file)
    for row in csv_reader:
        events.append(row)

k = len(events)
for i in range(1, k):
    if events[i][2][0] == 'O':
        continue
    if events[i][7] == 'Air duel':
        if events[i][2] not in name.keys():
            name[events[i][2]] = u
            u = u + 1
        no = name[events[i][2]]
        player[no][1] = player[no][1]+1
        v = i+1
        while v < k + 1:
            if events[v][6] == 'Duel':
                v = v + 1
                continue
            if events[v][2][0] == 'H':
                player[no][0] = player[no][0] + 1
            break
    elif events[i][7] == 'Ground attacking duel':
        if events[i][2] not in name.keys():
            name[events[i][2]] = u
            u = u + 1
        no = name[events[i][2]]
        player[no][3] = player[no][3]+1
        v = i + 1
        while v < k + 1:
            if events[v][6] == 'Duel':
                v = v + 1
                continue
            if events[v][2][0] == 'H':
                player[no][2] = player[no][2] + 1
            break
    elif events[i][7] == 'Ground loose ball duel':
        if events[i][2] not in name.keys():
            name[events[i][2]] = u
            u = u + 1
        no = name[events[i][2]]
        player[no][5] = player[no][5]+1
        v = i + 1
        while v < k + 1:
            if events[v][6] == 'Duel':
                v = v + 1
                continue
            if events[v][2][0] == 'H':
                player[no][4] = player[no][4]+1
            break
    elif events[i][7] == 'Acceleration':
        if events[i][2] not in name.keys():
            name[events[i][2]] = u
            u = u + 1
        no = name[events[i][2]]
        player[no][9] = player[no][9]+1
        player[no][6].append(int(float(events[i][8]))-int(float(events[i][10])))
        player[no][7].append(int(float(events[i][9]))-int(float(events[i][11])))
        player[no][8].append(int(float(events[i+1][5]))-int(float(events[i][5])))

for i in range(0, 30):
    sum = 0
    if player[i][9] > 0:
        q = player[i][9]
        for j in range(0,player[i][9]):
            if player[i][8][j] == 0:
                q = q - 1
                continue
            dist = sqrt((player[i][6][j] / 100 * length) ** 2 + (player[i][7][j] / 100 * width) ** 2)
            sum = sum + dist / player[i][8][j]
            speed[i] = sum / player[i][9]
    if player[i][1] > 0:
        air[i] = player[i][0] / player[i][1]
    if player[i][3] > 0:
        attack[i] = player[i][2] / player[i][3]
    if player[i][5] > 0:
        loose[i] = player[i][4] / player[i][5]

maxspeed = max(speed)
minspeed = min(speed)
maxair = max(air)
minair = min(air)
maxatt = max(attack)
minatt = min(attack)
maxloo = max(loose)
minloo = min(loose)

for i in range(0, 30):
    speedscore[i] = (speed[i] - minspeed) / (maxspeed - minspeed) * 60 + 40
    airscore[i] = (air[i] - minair) / (maxair - minair) * 60 + 40
    attscore[i] = (attack[i] - minatt) / (maxatt - minatt) * 60 + 40
    looscore[i] = (loose[i] - minloo) / (maxloo - minloo) * 60 + 40

for i in range(0, 30):
    score[i] = 0.4 * speedscore[i] + 0.2 * (airscore[i] + attscore[i] + looscore[i])

with open('../data/Player_body_data.csv', 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["Name", "Air Duel Score", "Ground Attacking Duel Score",
                     "Ground Loose Ball Duel Score", "Accelaration Score", "Body Score"])
    for i in name.keys():
        id = name[i]
        writer.writerow([i, airscore[id], attscore[id], looscore[id], speedscore[id], score[id]])
