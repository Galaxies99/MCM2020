import csvreader, csv
import math
import numpy as np
import matplotlib.pyplot as plt


def add_coordinates(loc, s, x, y):
    if loc.get(s) is None:
        loc[s] = [x, y, 1]
    else:
        lst = loc[s]
        loc[s] = [lst[0] + x, lst[1] + y, lst[2] + 1]
    return None


def add_counts(dicts, s, add):
    if dicts.get(s) is None:
        dicts[s] = [add, 1]
    else:
        dicts[s] = [dicts[s][0] + add, dicts[s][1] + 1]
    return None


def get_counts(dicts, s):
    if dicts.get(s) is None:
        return 0
    else:
        return dicts[s][0] / dicts[s][1]


def euclid_distance(x, y, xx, yy):
    return math.sqrt((x - xx) ** 2 + (y - yy) ** 2)


def euclid_distance_loc(a, b):
    return euclid_distance(a[0], a[1], b[0], b[1])


def main(write_match, left_time, right_time):
    full_events = csvreader.csv_reader_without_headers('../data/fullevents.csv')
    passing_events = csvreader.csv_reader_without_headers('../data/passingevents.csv')

    write_team = 'Huskies'
    location = {}
    name_list = []

    # Count and average coordinates.
    for item in full_events:
        if int(item[0]) is not write_match:
            continue
        if item[1].find(write_team) is -1:
            continue

        tm = float(item[5])
        if item[4].find('2') != -1:
            tm += 3600

        if left_time > tm or tm > right_time:
            continue

        name = (item[2].split('_'))[1]
        if name not in name_list:
            name_list.append(name)
        if item[3] != '':
            nm = (item[3].split('_'))[1]
            if nm not in name_list:
                name_list.append(nm)

        if item[6].find('Pass') is not -1:
            add_coordinates(location, name, float(item[8]), float(item[9]))
            if item[3] != '' and item[3] != item[2]:
                add_coordinates(location, (item[3].split('_'))[1], float(item[10]), float(item[11]))
        elif item[6].find('Save') is not -1 or item[6].find('Goalkeeper') is not -1:
            add_coordinates(location, name, 0, 50)
        elif item[6].find('Duel') is not -1 or item[6].find('Others') is not -1 or \
                item[6].find('Foul') is not -1 or item[6].find('Offside') is not -1 or item[6].find('Shot') is not -1:
            add_coordinates(location, name, float(item[8]), float(item[9]))

    # Compute the player's average location.
    for key in location:
        loc = location[key]
        assert loc[2] is not 0
        location[key] = [loc[0] / loc[2], loc[1] / loc[2]]

    # Compute the average coordinate distance between players.
    dC = {}
    for name1 in name_list:
        for name2 in name_list:
            if name1 == name2:
                continue
            key = name1 + '.' + name2
            if location.get(name1) is None:
                if name1.find('G') != -1:
                    location[name1] = [0, 50]
                else:
                    continue
            if location.get(name2) is None:
                if name2.find('G') != -1:
                    location[name2] = [0, 50]
                else:
                    continue
            dC[key] = euclid_distance_loc(location[name1], location[name2])

    # Count the times of each pass and passing times distance
    head_pass = {}
    hand_pass = {}
    high_pass = {}
    simple_pass = {}
    launch = {}
    cross = {}
    smart_pass = {}
    dT = {}
    for name1 in name_list:
        for name2 in name_list:
            if name1 == name2:
                continue
            key = name1 + '.' + name2
            dT[key] = 0

    for item in passing_events:
        if int(item[0]) is not write_match:
            continue
        if item[1].find(write_team) is -1:
            continue

        tm = float(item[5])
        if item[4].find('2') != -1:
            tm += 3600

        if left_time > tm or tm > right_time:
            continue
        name1 = (item[2].split('_'))[1]
        name2 = (item[3].split('_'))[1]
        if name1 == name2:
            continue
        key = name1 + '.' + name2
        dT[key] += 1
        dis = euclid_distance(float(item[7]), float(item[8]), float(item[9]), float(item[10]))
        if item[6].find('Head') != -1:  # Head pass
            add_counts(head_pass, key, dis)
        elif item[6].find('Hand') != -1:  # Hand pass
            add_counts(hand_pass, key, dis)
        elif item[6].find('High') != -1:  # High pass
            add_counts(high_pass, key, dis)
        elif item[6].find('Simple') != -1:  # Simple pass
            add_counts(simple_pass, key, dis)
        elif item[6].find('Launch') != -1:  # Launch
            add_counts(launch, key, dis)
        elif item[6].find('Cross') != -1:  # Cross
            add_counts(cross, key, dis)
        elif item[6].find('Smart') != -1:  # Smart pass
            add_counts(smart_pass, key, dis)

    # Compute the average passing distance.
    dP = {}
    kdP = {'Head pass': 0.8, 'Hand pass': 0.6, 'High pass': 1.3, 'Simple pass': 1.0, 'Launch': 0.7,
           'Cross': 1.2, 'Smart pass': 1.1}
    kdP_total = kdP['Head pass'] + kdP['Hand pass'] + kdP['High pass'] + kdP['Simple pass'] + \
                kdP['Cross'] + kdP['Smart pass'] + kdP['Launch']
    for name1 in name_list:
        for name2 in name_list:
            if name1 == name2:
                continue
            key = name1 + '.' + name2
            score = get_counts(head_pass, key) * kdP['Head pass'] \
                    + get_counts(hand_pass, key) * kdP['Hand pass'] \
                    + get_counts(high_pass, key) * kdP['High pass'] \
                    + get_counts(simple_pass, key) * kdP['Simple pass'] \
                    + get_counts(launch, key) * kdP['Launch'] \
                    + get_counts(cross, key) * kdP['Cross'] \
                    + get_counts(smart_pass, key) * kdP['Smart pass']
            score = score / kdP_total
            dP[key] = score

    # Compute dT and ready for standardize
    maxdC = 0
    maxdP = 0
    for name1 in name_list:
        for name2 in name_list:
            if name1 == name2:
                continue
            key = name1 + '.' + name2
            if dT[key] == 0:
                continue
            dT[key] = 1 / dT[key]
            maxdC = max(maxdC, dC[key])
            maxdP = max(maxdP, dP[key])

    # Standardize & Compute w
    w = {}
    for name1 in name_list:
        for name2 in name_list:
            if name1 == name2:
                continue
            key = name1 + '.' + name2
            if dT[key] == 0:
                continue
            dC[key] = dC[key] / maxdC
            dP[key] = dP[key] / maxdP
            w[key] = 1 / (0.7 * dT[key] + 0.2 * dC[key] + 0.1 * dP[key])
            w[key] = math.exp(w[key])

    a = {}
    k = {}
    for name1 in name_list:
        count = 0
        for name2 in name_list:
            key = name1 + '.' + name2
            if w.get(key) is None:
                a[key] = 0
            else:
                a[key] = 1
                count += 1
        k[name1] = count

    c_count = 0
    c_num = 0
    c = {}
    for name in name_list:
        sum = 0
        for name2 in name_list:
            for name3 in name_list:
                key1 = name2 + '.' + name
                key2 = name + '.' + name3
                key3 = name2 + '.' + name3
                if a[key1] == 1 and a[key2] == 1 and a[key3] == 1:
                    sum = sum + (w[key1] + w[key2]) / 2
        if k[name] != 0 and k[name] != 1:
            c[name] = sum / k[name] / (k[name] - 1)
            c_count += c[name]
            c_num += 1
            # print(name, c[name])
        else:
            c[name] = 0

    return c


if __name__ == '__main__':
    lst = []
    out = {'D1': [], 'D2': [], 'D3': [], 'D4': [], 'D5': [], 'D6': [], 'D7': [], 'D8': [], 'D9': [], 'D10': [],
           'M1': [], 'M2': [], 'M3': [], 'M4': [], 'M5': [], 'M6': [], 'M7': [], 'M8': [], 'M9': [], 'M10': [],
           'M11': [], 'M12': [], 'M13': [], 'F1': [], 'F2': [], 'F3': [], 'F4': [], 'F5': [], 'F6': [], 'G1': []}
    tm = []
    tm.append('Name')
    for i in range(1, 115):
        if i > 50 and i < 60:
            continue
        print(i)
        tm.append(i)
        p = main(1, max(i * 60 - 600, 0), i * 60)
        for key in out:
            if p.get(key) is not None:
                out[key].append(p[key])
            else:
                out[key].append(0)

    with open('../data/networkdata/data_figure.csv', 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, dialect='excel')
        csv_writer.writerow(tm)
        for key in out:
            opt = out[key]
            opt.insert(0, key)
            csv_writer.writerow(opt)
