import matplotlib.pyplot as plt
import csv

fig = plt.figure()

passing_data = []

with open('../data/passing_data.csv') as csvfile:
    csv_reader = csv.reader(csvfile)
    for row in csv_reader:
        passing_data.append(row)


sp = fig.add_subplot(111)
sp.set_xlim(0, 100)
sp.set_ylim(0, 100)
sp.set_aspect(0.64762)

for orec in passing_data:
    rec = [int(x) for x in orec]
    if rec[0] == 1 and rec[1] == 1:
        if rec[2] == 0:
            sp.arrow(rec[3], rec[4], rec[5] - rec[3], rec[6] - rec[4], length_includes_head=True, head_width=1,
                     head_length=2, fc='r', ec='r', alpha=0.4, linewidth=0.3)
        else:
            sp.arrow(rec[3], rec[4], rec[5] - rec[3], rec[6] - rec[4], length_includes_head=True, head_width=1,
                     head_length=2, fc='b', ec='b', alpha=0.6, linewidth=0.3)


plt.show()
plt.tight_layout()