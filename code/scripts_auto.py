import pass_network_match as step1
import kmeans_classification as step2
import csv

if __name__ == '__main__':
    res = []
    for i in range(1, 39):
        print(i)
        step1.main(i)
        res.append(step2.main(i))

    with open('../data/networkdata/res.csv', 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, dialect='excel')
        for row in res:
            csv_writer.writerow(row)

