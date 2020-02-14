import csv

scores = {}

headers = ["Name", "Air Duel Score", "Ground Attacking Duel Score", "Ground Loose Ball Duel Score", "Acceleration Score", "Body Score",
           "Ground Defending Duel Score (Total Counts)", "Ground Defending Duel Score (Successful Rate)", "Block Shot Score", "Clearance Score", "Defending Score",
           "Pass Accuracy Score", "Total Pass Score", "Smart Pass Rate Score", "Pass Score",
           "Total Shot Score", "Shot Accuracy Score", "Free Kick Accuracy Score", "Shot Score"]

with open('../data/Player_body_data.csv') as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)
    for row in csv_reader:
        scores[row[0]] = [float(row[1]), float(row[2]), float(row[3]), float(row[4]), float(row[5])]

with open('../data/Player_defending_data.csv') as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)
    for row in csv_reader:
        scores[row[0]].append(float(row[2]))
        scores[row[0]].append(float(row[4]))
        scores[row[0]].append(float(row[6]))
        scores[row[0]].append(float(row[8]))
        scores[row[0]].append(float(row[9]))

with open('../data/Player_passing_data.csv') as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)
    for row in csv_reader:
        scores[row[0]].append(float(row[6]))
        scores[row[0]].append(float(row[7]))
        scores[row[0]].append(float(row[8]))
        scores[row[0]].append(float(row[9]))

with open('../data/Player_shot_data.csv') as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)
    for row in csv_reader:
        scores[row[0]].append(float(row[8]))
        scores[row[0]].append(float(row[9]))
        scores[row[0]].append(float(row[10]))
        scores[row[0]].append(float(row[11]))

with open('../data/Player_full_data.csv', 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file, dialect='excel')
    csv_writer.writerow(headers)
    for key in scores:
        row = scores[key]
        row.insert(0, key)
        csv_writer.writerow(row)