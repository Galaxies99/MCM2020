import csv
import random

full_events = []

with open('../../data/fullevents.csv') as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)
    for row in csv_reader:
        full_events.append(row)

pass_score = {}

for item in full_events:
    if item[2].find('Huskies') is -1:
        continue
    if item[6] == 'Pass':
        smart_pass_add = 0
        success_pass_add = 0
        total_pass_add = 1
        if item[7] == 'Smart pass':
            smart_pass_add = 1
        if item[3] is not '':
            success_pass_add = 1
        if pass_score.get(item[2]) is None:
            pass_score[item[2]] = [success_pass_add, total_pass_add, success_pass_add / total_pass_add,
                                   smart_pass_add, smart_pass_add / total_pass_add]
        else:
            cur = pass_score[item[2]]
            pass_score[item[2]] = [cur[0] + success_pass_add, cur[1] + total_pass_add,
                                   (cur[0] + success_pass_add) / (cur[1] + total_pass_add),
                                   cur[3] + smart_pass_add,
                                   (cur[3] + smart_pass_add) / (cur[1] + total_pass_add)]

min_accuracy = 1
max_accuracy = 0
total_min_passes = 10000
total_max_passes = 0
min_smart_rate = 1
max_smart_rate = 0

for key in pass_score:
    score = pass_score[key]
    # Only counts total pass > 100
    if score[1] >= 100:
        min_accuracy = min(min_accuracy, score[2])
        max_accuracy = max(max_accuracy, score[2])
        total_min_passes = min(total_min_passes, score[1])
        total_max_passes = max(total_max_passes, score[1])
        min_smart_rate = min(min_smart_rate, score[4])
        max_smart_rate = max(max_smart_rate, score[4])

for key in pass_score:
    score = pass_score[key]
    if score[1] >= 100:
        pass_score[key].append((score[2] - min_accuracy) / (max_accuracy - min_accuracy) * 60 + 40)
        pass_score[key].append((score[1] - total_min_passes) / (total_max_passes - total_min_passes) * 60 + 40)
        pass_score[key].append((score[4] - min_smart_rate) / (max_smart_rate - min_smart_rate) * 60 + 40)
    else:
        pass_score[key].append((score[2] - 0.6) / 0.4 * 20 + 40)
        pass_score[key].append(score[1] / 100 * 10 + 40)
        pass_score[key].append(max(score[4] / 0.03 * 5, random.randint(40, 50)))

    if key.find('G') is not -1:
        pass_score[key].append(0.6 * pass_score[key][5] + 0.4 * pass_score[key][6])
    elif key.find('D') is not -1:
        pass_score[key].append(0.5 * pass_score[key][5] + 0.4 * pass_score[key][6] + 0.1 * pass_score[key][7])
    elif key.find('M') is not -1:
        pass_score[key].append(0.4 * pass_score[key][5] + 0.4 * pass_score[key][6] + 0.2 * pass_score[key][7])
    elif key.find('F') is not -1:
        pass_score[key].append(0.4 * pass_score[key][5] + 0.2 * pass_score[key][6] + 0.4 * pass_score[key][7])

headers = ['Name', 'Successful Pass', 'Total Pass', 'Accuracy', 'Total Smart Pass', 'Smart Pass Rate', 'Accuracy score', 'Total Pass Score', 'Smart Pass Rate Score', 'Pass score']

with open('../../data/Player_passing_data.csv', 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file, dialect='excel')
    csv_writer.writerow(headers)
    for key in pass_score:
        row = pass_score[key]
        row.insert(0, key)
        csv_writer.writerow(row)

