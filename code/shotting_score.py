import csv
import random

full_events = []

with open('../data/fullevents.csv') as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)
    for row in csv_reader:
        full_events.append(row)

shot_score = {}

for i, item in enumerate(full_events):
    if item[1] != 'Huskies':
        continue
    name = item[2]
    if shot_score.get(name) is None:
        shot_score[name] = [0, 0, 0, 0, 0]
    if item[6] == 'Shot':
        shots_add = 1
        shots_on_add = 0
        shots_block_add = 0
        if full_events[i + 1][6] == 'Save attempt':
            shots_on_add = 1
        if full_events[i + 1][6] == 'Others on the ball' or \
                ((full_events[i + 1][6] == 'Pass' or full_events[i + 1][6] == 'Duel') and float(full_events[i + 1][5]) - float(item[5]) < 25):
            shots_block_add = 1
        cur = shot_score[name]
        shot_score[name] = [cur[0] + shots_on_add, cur[1] + shots_block_add, cur[2] + shots_add,
                            cur[3], cur[4]]
    if item[7] == 'Free kick shot':
        free_kick_shots_add = 1
        free_kick_shots_on_add = 0
        if full_events[i + 1][6] == 'Save attempt':
            free_kick_shots_on_add = 1
        cur = shot_score[name]
        shot_score[name] = [cur[0], cur[1], cur[2],
                            cur[3] + free_kick_shots_on_add, cur[4] + free_kick_shots_add]

for key in shot_score:
    score = shot_score[key]
    if score[2] - score[1] != 0:
        shot_score[key].append(score[0] / (score[2] - score[1]))
    else:
        shot_score[key].append(0)
    if score[4] != 0:
        shot_score[key].append(score[3] / score[4])
    else:
        shot_score[key].append(0)

    shot_score[key].append(shot_score[key][2] + 60)
    if shot_score[key][2] == 0:
        shot_score[key].append(random.randint(40, 50))
    elif shot_score[key][2] <= 10:
        shot_score[key].append(shot_score[key][5] * 25 + 45)
    else:
        shot_score[key].append(shot_score[key][5] * 60 + 40)
    if shot_score[key][4] == 0:
        shot_score[key].append(random.randint(40, 50))
    else:
        shot_score[key].append(shot_score[key][6] * 40 + 60)

    score = shot_score[key]

    if key.find('D') != -1:
        shot_score[key].append(score[7] * 0.2 + score[8] * 0.4 + score[9] * 0.4)
    elif key.find('M') != -1:
        shot_score[key].append(score[7] * 0.2 + score[8] * 0.4 + score[9] * 0.4)
    elif key.find('G') != -1:
        shot_score[key].append(random.randint(20, 40))
    elif key.find('F') != -1:
        shot_score[key].append(score[7] * 0.3 + score[8] * 0.4 + score[9] * 0.3)

headers = ['Player', 'Shots on', 'Shots blocked', 'Shots total', 'Free kick shots on', 'Free kick shots total', 'Shots on rate', 'Free kick shots on rate', 'Shots total Score', 'Shots accuracy Score', 'Free kick accuracy Score', 'Shot Score']
with open('../data/Player_shotting_data.csv', 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file, dialect='excel')
    csv_writer.writerow(headers)
    for key in shot_score:
        row = shot_score[key]
        row.insert(0, key)
        csv_writer.writerow(row)
