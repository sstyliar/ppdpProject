from utils import aux_utils
import numpy as np


def getIntILoss(generalizedRows, column, possibleValues):
    Da = max(possibleValues) - min(possibleValues) + 1  # + 1 Cause we are missing one due to python's range
    groups = generalizedRows.groupby(column)[column].apply(list)  # Group the values of the fields to individual lists
    ret = 0
    for group in groups:
        count = len(group)
        groupRange = aux_utils.humanReadableToRange(np.unique(group)[0])
        Vg = max(groupRange) - min(groupRange) + 1
        ret += ((Vg - 1) / Da) * count
    return ret


def getStrILoss(generalizedRows, column, possibleValues):
    Da = len(possibleValues)
    groups = generalizedRows.groupby(column)[column].apply(list)  # Group the values of the fields to individual lists
    ret = 0
    for group in groups:
        Vg = count = len(group)
        ret += ((Vg - 1) / Da) * count
    return ret


def getILoss(initialData, generalizedData, config):
    ret = 0
    initialRows = initialData["rows"]
    generalizedRows = generalizedData["rows"]

    for column in config["generalization"]["fields"]:
        possibleValues = np.unique(initialRows[column])  # Count how many possible values this field has
        if config["generalization"]["fields"][column] == "str":
            ret += getStrILoss(generalizedRows, column, possibleValues)
        elif config["generalization"]["fields"][column] == "int":
            ret += getIntILoss(generalizedRows, column, possibleValues)
    return ret
