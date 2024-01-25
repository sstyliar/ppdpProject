import numpy as np


def getEntropyLDiversity(data):
    groups = data["rows"].groupby(data["qi_group"])[data["sa_group"]].apply(list)
    entropyLDivs = []
    for group in groups:
        uniqueValues = np.unique(group)
        groupLDiv = 1
        for uniqueVal in uniqueValues:
            tmp = group.count(uniqueVal) / len(group)
            groupLDiv *= pow(tmp, -tmp)
        entropyLDivs.append(groupLDiv)
    return min(entropyLDivs)


def getLDiversity(data):
    targetCol = data["sa_group"]
    uniqueGroups = data["rows"].groupby(data["qi_group"])[targetCol].apply(list)
    saUniqueValueCounts = []
    for group in uniqueGroups:
        uniqueValues = np.unique(group)
        saUniqueValueCounts.append(len(uniqueValues))
    return min(saUniqueValueCounts)
