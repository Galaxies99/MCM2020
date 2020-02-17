import csvreader
import numpy as np
import matplotlib.pyplot as plt

header, player_data = csvreader.csv_reader_with_headers('../data/Player_full_data.csv')

for player in player_data:
    plt.style.use('ggplot')
    values = [float(player[5]), float(player[10]), float(player[14]), float(player[18])]
    feature = ['Body', 'Defense', 'Pass', 'Shot']
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


    name = player[0].split('_')[1]
    plt.title(name + ' Score')

    ax.grid(True)
    plt.savefig('../pics/' + player[0] + '_score.png')
    plt.show()
