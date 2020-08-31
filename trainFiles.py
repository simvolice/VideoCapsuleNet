import csv
import json

smokeClassID = '54'
fightClassID = '64'

smokeClassLists = []
fightClassLists = []

with open('ava_train_v2.2.csv') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    for row in spamreader:
        if smokeClassID == row[6]:
            resultStr = "{}:{}:{}:{}:{}:{}:{}".format(row[0], int(row[1]) - 1, int(row[1]) + 1,
                                                       row[2], row[3], row[4], row[5])

            smokeClassLists.append(resultStr)
        elif fightClassID == row[6]:
            resultStr = "{}:{}:{}:{}:{}:{}:{}".format(row[0], int(row[1]) - 1, int(row[1]) + 1,
                                                      row[2], row[3], row[4], row[5])

            fightClassLists.append(resultStr)

    with open('smokeData.txt', "w") as smokeDatafile:
        json.dump(smokeClassLists, smokeDatafile)
    with open('fightData.txt', "w") as fightDatafile:
        json.dump(fightClassLists, fightDatafile)

