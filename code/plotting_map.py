import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse
import csv
import math

average_position_data = []
passing_accuracy_data = []
passing_data = []

with open('../data/plotting_data.csv') as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)
    for row in csv_reader:
        average_position_data.append(row)

with open('../data/passing_accuracy.csv') as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)
    for row in csv_reader:
        passing_accuracy_data.append(row)

with open('../data/passingevents.csv') as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)
    for row in csv_reader:
        passing_data.append(row)

width_height = 0.64762

for write_match in range(1, 39):
    write_team = 'Huskies'
    # write_team = 'Opponent'

    fig = plt.figure()
    sp = fig.add_subplot(111)
    sp.set_xlim(0, 100)
    sp.set_ylim(0, 100)
    sp.set_aspect(width_height)

    location_dict = {}
    radius = {}

    for item in average_position_data:
        if int(item[0]) != write_match:
            continue
        if item[1].find(write_team) == -1:
            continue
        if int(item[5]) == 1:
            continue

        total_pass = 0
        successful_pass = 0
        location_dict[item[1]] = [float(item[2]), float(item[3])]

        for _item in passing_accuracy_data:
            if int(item[0]) == int(_item[0]) and item[1] == _item[1]:
                total_pass = int(_item[3])
                successful_pass = int(_item[2])
                break

        radius[item[1]] = (total_pass * 0.15 + 1)
        if radius[item[1]] < 5:
            alpha = 0.3
        elif radius[item[1]] < 10:
            alpha = 0.5
        elif radius[item[1]] < 20:
            alpha = 0.7
        else:
            alpha = 0.9

        sp.add_patch(Ellipse(xy=(float(item[2]), float(item[3])),
                             width=radius[item[1]] * width_height, height=radius[item[1]],
                             alpha=alpha, color='r'))

    passing_network = {}

    for item in passing_data:
        if int(item[0]) != write_match:
            continue
        if item[2].find(write_team) == -1:
            continue

        key = item[2] + '.' + item[3]

        if passing_network.get(key) is None:
            passing_network[key] = 1
        else:
            passing_network[key] = passing_network[key] + 1

    for key in passing_network:
        assert key.find('.') is not None
        pos = key.find('.')
        a = key[0:pos]
        b = key[pos + 1:]
        times = passing_network[key]

        if location_dict.get(a) is None or location_dict.get(b) is None:
            continue

        sx = location_dict[a][0]
        sy = location_dict[a][1]
        ex = location_dict[b][0]
        ey = location_dict[b][1]

        if abs(ex - sx) > 1e-3:
            k = (ey - sy) / (ex - sx)

            aa = radius[a] * width_height / 2
            ab = radius[a] / 2
            ra = aa * ab / math.sqrt(ab ** 2 + (aa * k) ** 2) * math.sqrt(1 + k ** 2)

            ba = radius[b] * width_height / 2
            bb = radius[b] / 2
            rb = ba * bb / math.sqrt(bb ** 2 + (ba * k) ** 2) * math.sqrt(1 + k ** 2)

            dis = math.sqrt((sx - ex) ** 2 + (sy - ey) ** 2)
            dis = dis - radius[a] - radius[b]
        else:
            aa = radius[a] * width_height / 2
            ab = radius[a] / 2
            ra = ab

            ba = radius[b] * width_height / 2
            bb = radius[b] / 2
            rb = bb

            dis = math.sqrt((sx - ex) ** 2 + (sy - ey) ** 2)
            dis = dis - radius[a] - radius[b]

        if dis > 0:
            if times <= 2:
                alpha = 0.15
                width = 0.3
            elif times <= 3:
                alpha = 0.25
                width = 0.7
            elif times <= 5:
                alpha = 0.45
                width = 1.5
            elif times <= 10:
                alpha = 0.65
                width = 3.5
            elif times <= 20:
                alpha = 0.85
                width = 6.0
            else:
                alpha = 0.95
                width = 9.0

            theta = math.atan2(ey - sy, ex - sx)
            new_sx = sx + math.cos(theta) * (aa + width * 0.15)
            new_sy = sy + math.sin(theta) * (ab + width * 0.15)
            new_ex = ex - math.cos(theta) * (ba + width * 0.15)
            new_ey = ey - math.sin(theta) * (bb + width * 0.15)

            sp.arrow(new_sx, new_sy, new_ex - new_sx, new_ey - new_sy,
                     length_includes_head=True, head_width=1, head_length=2, fc='black', ec='black', alpha=alpha,
                     linewidth=width)

    plt.savefig('../pics/pic' + str(write_match) + '_Huskies.png');
    plt.show()
