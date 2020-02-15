import networkx as nx
import matplotlib.pyplot as plt
import csvreader
import numpy as np
import passing_network_match as pnm


def add_passing_data(ps, s, sp, tp):
    if ps.get(s) is None:
        ps[s] = [sp, tp]
    else:
        lst = ps[s]
        ps[s] = [lst[0] + sp, lst[1] + tp]


def set_pts(graph, nodes, nloc, node_color, size, alpha):
    if nodes is not []:
        vnode = np.array(nloc)
        npos = dict(zip(nodes, vnode))
        nlabels = dict(zip(nodes, nodes))
        nx.draw_networkx_nodes(G, npos, nodes, alpha=alpha, node_size=size, node_color=node_color)
        nx.draw_networkx_labels(G, npos, nlabels)


def set_points(graph, nodes, nloc, ps_data, node_color):
    for i, key in enumerate(nodes):
        tnodes = [key]
        tnlocs = [nloc[i]]
        dat = ps_data[key]
        size = dat[1] * 20
        alpha = dat[1] / 160 + 0.15
        set_pts(graph, tnodes, tnlocs, node_color=node_color, size=size, alpha=alpha)


length_factor = 1.05
width_factor = 0.68

full_events = csvreader.csv_reader_without_headers('../data/fullevents.csv')
passing_events = csvreader.csv_reader_without_headers('../data/passingevents.csv')

write_team = 'Huskies'

for write_match in range(1, 39):
    location = {}
    passing_data = {}
    pair_passing_data = {}
    substitution_list = []

    for item in full_events:
        if int(item[0]) is not write_match:
            continue
        if item[1].find(write_team) is -1:
            continue

        name = (item[2].split('_'))[1]

        if item[6].find('Pass') is not -1:
            pnm.add_coordinates(location, name, float(item[8]), float(item[9]))
            add_passing_data(passing_data, name, 0, 1)
            if item[3] is not '' and item[3] is not item[2]:
                pnm.add_coordinates(location, (item[3].split('_'))[1], float(item[10]), float(item[11]))
                add_passing_data(passing_data, name, 1, 0)
        elif item[6].find('Save') is not -1 or item[6].find('Goalkeeper') is not -1:
            pnm.add_coordinates(location, name, 0, 50)
        elif item[6].find('Substitution') is not -1:
            substitution_list.append((item[3].split('_'))[1])
        elif item[6].find('Duel') is not -1 or item[6].find('Others') is not -1 or item[6].find('Foul') is not -1 or \
                item[6].find('Offside') is not -1 or item[6].find('Shot') is not -1:
            pnm.add_coordinates(location, name, float(item[8]), float(item[9]))

    for item in passing_events:
        if int(item[0]) is not write_match:
            continue
        if item[1].find(write_team) is -1:
            continue

        name1 = (item[2].split('_'))[1]
        name2 = (item[3].split('_'))[1]
        if name1 > name2:
            name1, name2 = name2, name1
        key = name1 + '.' + name2

        if pair_passing_data.get(key) is None:
            pair_passing_data[key] = 1
        else:
            pair_passing_data[key] += 1

    for key in passing_data:
        passing_data[key].append(passing_data[key][0] / passing_data[key][1])

    for key in location:
        loc = location[key]
        assert loc[2] is not 0
        location[key] = [loc[0] / loc[2] * length_factor, 68 - loc[1] / loc[2] * width_factor]

    G = []
    Gloc = []
    M = []
    Mloc = []
    F = []
    Floc = []
    D = []
    Dloc = []

    for key in location:
        if key in substitution_list:
            continue
        if key.find('G') is not -1:
            G.append(key)
            Gloc.append([location[key][0], location[key][1]])
        elif key.find('M') is not -1:
            M.append(key)
            Mloc.append([location[key][0], location[key][1]])
        elif key.find('D') is not -1:
            D.append(key)
            Dloc.append([location[key][0], location[key][1]])
        elif key.find('F') is not -1:
            F.append(key)
            Floc.append([location[key][0], location[key][1]])

    Gr = nx.Graph()

    set_points(Gr, G, Gloc, passing_data, node_color='y')
    set_points(Gr, D, Dloc, passing_data, node_color='b')
    set_points(Gr, M, Mloc, passing_data, node_color='g')
    set_points(Gr, F, Floc, passing_data, node_color='r')

    for key in pair_passing_data:
        A = (key.split('.'))[0]
        B = (key.split('.'))[1]
        if A not in substitution_list and B not in substitution_list:
            num = pair_passing_data[key]
            alpha = min(num / 15, 1)
            width = num / 25 * 4
            nx.draw_networkx_edges(Gr, location, [[A, B]], alpha=alpha, width=width)


    plt.xlim(0, 105)
    plt.ylim(0, 68)
    plt.savefig('../pics/match' + str(write_match) + '.png')
    plt.show()
