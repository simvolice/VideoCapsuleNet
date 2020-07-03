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
            resultStr = "{}:{}:{}:{}:{}:{}:{}".format(row[0], row[1], row[1],
                                                       row[2], row[3], row[4], row[5])

            smokeClassLists.append(resultStr)
        elif fightClassID == row[6]:
            resultStr = "{}:{}:{}:{}:{}:{}:{}".format(row[0], row[1], row[1],
                                                      row[2], row[3], row[4], row[5])

            fightClassLists.append(resultStr)
    print(len(smokeClassLists))
    print(len(fightClassLists))
    with open('smokeData.txt', "r") as smokeDatafile:
        print(len(json.load(smokeDatafile)))
    with open('fightData.txt', "r") as fightDatafile:
        print(len(json.load(fightDatafile)))

