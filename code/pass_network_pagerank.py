import csvreader, csv
import math
import numpy as np
import matplotlib.pyplot as plt
import pagerank as pr

def main(write_match):
    full_events = csvreader.csv_reader_without_headers('../data/fullevents.csv')
    passing_events = csvreader.csv_reader_without_headers('../data/passingevents.csv')

    write_team = 'Huskies'
    location = {}
    substitution_list = []
    name_list = []
    dT = {}

    for item in full_events:
        if int(item[0]) is not write_match:
            continue
        if item[1].find(write_team) is -1:
            continue
        name = (item[2].split('_'))[1]
        if name not in name_list:
            name_list.append(name)

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
        name1 = (item[2].split('_'))[1]
        name2 = (item[3].split('_'))[1]
        if name1 == name2:
            continue
        key = name1 + '.' + name2
        dT[key] += 1

    graph = pr.Graph()

    for name in name_list:
        sum = 0
        for name2 in name_list:
            if name == name2:
                continue
            key = name + '.' + name2
            sum += dT[key]
        for name2 in name_list:
            if name == name2:
                continue
            key = name + '.' + name2
            c = dT[key] / sum
            graph.add_link(name, name2, c)

    pr_map = graph.get_PR()
    with open('../data/networkdata/match' + str(write_match) + '_pr.csv', 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, dialect='excel')
        for key in pr_map:
            csv_writer.writerow([key, pr_map[key]])

if __name__ == '__main__':
    main(15)