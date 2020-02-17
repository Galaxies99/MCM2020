# KMeans Classification
# Note: csvreader is our custom library to read csv file.
import csvreader
import random


def kmeans_step(K, c, bel, center):
    loss = 0
    # Calculate current total loss.
    for i, item in enumerate(c):
        # Choose the nearest center.
        min_loss, pos = 1e9, 0
        for j in range(0, K):
            dis = (center[j] - item[1]) ** 2
            if dis < min_loss:
                min_loss, pos = dis, j
        bel[i] = pos
        loss += min_loss
    num = []
    for i in range(0, K):
        center[i] = 0
        num.append(0)
    # Calculate new center.
    for i in range(0, len(c)):
        center[bel[i]] += c[i][1]
        num[bel[i]] += 1
    for i in range(0, K):
        center[i] /= num[i]
    return loss


def kmeans(c, write_match, K):
    # Randomly choose K centers.
    rd_list = []
    for i in range(0, K):
        x = random.randint(0, len(c) - 1)
        while x in rd_list:
            x = random.randint(0, len(c) - 1)
        rd_list.append(x)
    bel = []
    for item in c:
        bel.append(0)
    center = []
    for i in rd_list:
        center.append(c[i][1])
    ori_loss = kmeans_step(K, c, bel, center)
    while True:
        loss = kmeans_step(K, c, bel, center)
        # if loss is stable, then classification is finished.
        if abs(loss - ori_loss) < 1e-3:
            break
        ori_loss = loss
    return center, bel


def main(write_match):
    c_data = csvreader.csv_reader_without_headers('../data/networkdata/match'
                                                  + str(write_match) + '_c.csv')
    # c means clustering coefficient data.
    # c[0] is player name, c[1] is the clustering coefficient value.
    c = []
    for item in c_data:
        c.append([item[0], float(item[1])])
    # First divide into 2 groups: Group A and others.
    center, bel = kmeans(c, write_match, 2)
    # Make center[1] group A.
    if center[0] > center[1]:
        center[0], center[1] = center[1], center[0]
        for i, item in enumerate(bel):
            if item == 1:
                bel[i] = 0
            else:
                bel[i] = 1
    # Copy other item to d[].
    d = []
    for i, item in enumerate(c):
        if bel[i] == 0:
            d.append(item)
    # Divide others into 2 groups: Group B and Group C.
    center2, bel2 = kmeans(d, write_match, 2)
    # Make center2[0] Group C and center2[1] Group B.
    if center2[0] > center2[1]:
        center2[0], center2[1] = center2[1], center2[0]
    # Return every group's center.
    return [center2[0], center2[1], center[1]]


if __name__ == '__main__':
    # Analyze the data of match 1.
    print(main(1))