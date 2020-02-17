import csv

count = 0
sum = 0
dict = {}

with open('../../data/fullevents.csv') as f:
    f_csv = csv.reader(f)
    for row in f_csv:
        if 'Huskies' in row[2] and dict.get(row[2])==None:
            onedict = {}
            onedict['Player'] = row[2]
            onedict['DeDuelTotal'] = 0
            onedict['Clearance'] = 0
            onedict['Touch'] = 0
            onedict['DeDuelSuccess'] = 0
            dict[row[2]] = onedict


with open('../data/fullevents.csv') as f:
    f_csv = csv.reader(f)
    for row in f_csv:
        if row[7] == 'Clearance' and 'Huskies' in row[2]:
            name = row[2]
            onedict = dict.get(name)
            onedict['Clearance'] += 1
            dict[name] = onedict

with open('../data/fullevents.csv') as f:
    f_csv = csv.reader(f)
    try_to_steal = False
    name = ''
    for row in f_csv:
        if 'Ground defend' in row[7] and 'Huskies' in row[2]:
            try_to_steal = True
            name = row[2]
            onedict = dict.get(name)
            onedict['DeDuelTotal'] += 1
            dict[name] = onedict
            continue
        if try_to_steal:
            if 'Ground attack' in row[7]:
                continue
            else:
                if row[1] == 'Huskies':
                    onedict = dict.get(name)
                    onedict['DeDuelSuccess'] += 1
                    dict[name] = onedict
                try_to_steal = False
                name = ''

with open('../data/fullevents.csv') as f:
    f_csv = csv.reader(f)
    enemy_shot = False
    for row in f_csv:
        if row[7] == 'Shot' and 'Opponent' in row[1]:
            enemy_shot = True
            continue
        if enemy_shot:
            if row[7] =='Touch' and row[1]=='Huskies':
                name = row[2]
                onedict = dict.get(name)
                onedict['Touch'] += 1
                dict[name] = onedict
            enemy_shot = False

for name in dict.keys():
    onedict = dict.get(name)
    rate = onedict['DeDuelSuccess']/onedict['DeDuelTotal']
    if rate >= 0.6:
        rate -= 0.4
    onedict['DefendRate'] = rate
    onedict.pop('DeDuelSuccess')
    dict[name] = onedict

rate_min = 1
rate_max = 0
touch_min = 10000
touch_max = 0
clearance_max = 0
clearance_min = 10000
total_max = 0
total_min = 10000

for name in dict.keys():
    onedict = dict.get(name)
    rate = onedict['DefendRate']
    touch = onedict['Touch']
    clearance = onedict['Clearance']
    total = onedict['DeDuelTotal']
    rate_max = max(rate_max, rate)
    rate_min = min(rate_min, rate)
    touch_max = max(touch_max, touch)
    touch_min = min(touch_min, touch)
    clearance_max = max(clearance_max, clearance)
    clearance_min = min(clearance_min, clearance)
    total_max = max(total_max, total)
    total_min = min(total_min, total)

for name in dict.keys():
    onedict = dict.get(name)
    rate = onedict['DefendRate']
    touch = onedict['Touch']
    clearance = onedict['Clearance']
    total = onedict['DeDuelTotal']
    onedict['Clearance_Score'] = (clearance - clearance_min) / (clearance_max - clearance_min) * 60 + 40
    onedict['Duel_Score'] = (rate - rate_min) / (rate_max - rate_min) * 60 + 40
    onedict['Touch_Score'] = (touch - touch_min) / (touch_max - touch_min) * 60 + 40
    onedict['DeDuelTotal_Score'] = (total - total_min) / (total_max - total_min) * 60 + 40
    onedict['Defend_Score'] = int(0.25 * onedict['DeDuelTotal_Score'] + 0.45 * onedict['Duel_Score'] +
                                  0.2 * onedict['Clearance_Score'] + 0.1 * onedict['Touch_Score'])
    dict[name] = onedict

list = []
headers = ["Name", "Ground Defending Duel (Total Counts)",
           "Ground Defending Duel Score (Total Counts)",
           "Ground Defending Duel (Successful Rate)",
           "Ground Defending Duel Score (Successful Rate)",
           "Block Shot Counts", "Block Shot Score",
           "Clearance Counts", "Clearance Score", "Defense Score"]

with open('../../data/Player_defense_data.csv', 'w', newline='') as csv_file:
    writer = csv.writer(csv_file, dialect='excel')
    writer.writerow(headers)
    for key in dict:
        onedict = dict[key]
        row = [key, onedict['DeDuelTotal'], onedict['DeDuelTotal_Score'], onedict['DefendRate'],
               onedict['Duel_Score'], onedict['Touch'], onedict['Touch_Score'],
               onedict['Clearance'], onedict['Clearance_Score'], onedict['Defend_Score']]
        writer.writerow(row)