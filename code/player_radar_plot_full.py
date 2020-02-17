import csvreader
import numpy as np
import matplotlib.pyplot as plt

header = []
player_data = []

header, player_data = csvreader.csv_reader_with_headers('../data/Player_full_data.csv')

for player in player_data:
    plt.style.use('ggplot')
#    values = [float(player[5]), float(player[10]), float(player[14]), float(player[18])]
#    feature = ['Body Score', 'Defending Score', 'Passing Score', 'Shot Score']
    list = [1, 2, 3, 4, 6, 7, 8, 9, 11, 12, 13, 15, 16, 17]
    values = []
    feature = []

    for j, i in enumerate(list):
        values.append(float(player[i]))
        feature.append('Feature ' + str(j+1))

    N = len(values)

    angles = np.linspace(0, 2*np.pi, N, endpoint=False)

    values = np.concatenate((values, [values[0]]))
    angles = np.concatenate((angles, [angles[0]]))

    fig = plt.figure()
    ax = fig.add_subplot(111, polar=True)
    ax.plot(angles, values, 'o-', linewidth=2)
    ax.fill(angles, values, 'r', alpha=0.5)

    ax.set_thetagrids(angles*180/np.pi, feature)

    ax.set_ylim(0, 100)

    plt.title(player[0] + ' Score')

    ax.grid(True)
    plt.savefig('../pics/' + player[0] + '_score_detail.png')
    plt.show()
