import os
import pathlib
import pandas as pd
import Levenshtein


def readCsv(file_name, column_names, separator):
    if isinstance(file_name, str):
        file_name = pathlib.Path(file_name)

    file_extension = os.path.splitext(file_name)[1]

    if file_extension in [".csv", ".txt"]:
        data = pd.read_csv(file_name, on_bad_lines='skip', names=column_names, sep=separator)
    else:
        raise ValueError("Invalid file extension.")

    return data


def readCsvFromConfig(key, config):
    separator = config["csv_separator"]
    file_name = config["data"][key]["dir"]
    column_names = config["data"][key]["column_names"]
    return readCsv(file_name, column_names, separator)


# Returns a human readable form of a range object
def rangeToHumanReadable(val):
    return f'[{min(val)} - {max(val) + 1})'


# Reverts the above
def humanReadableToRange(val):
    parts = val.split('-')
    start = parts[0]
    end = parts[1]
    return range(int(start[1:]), int(end[:len(end) - 1]))


# Wrapper for a list
def humanReadableListToRange(lst):
    ret = []
    for val in lst:
        ret.append(humanReadableToRange(val))
    return ret


# Returns from a list the item that resembles the most the input string
def getMostSimilarStringFromArray(strng, arr):
    similarities = [Levenshtein.distance(strng, s) for s in arr]
    minDistance = min(similarities)
    mostSimilarIndices = [i for i, dist in enumerate(similarities) if dist == minDistance]
    return arr[mostSimilarIndices[0]]


def buildSelect(options):
    selects = []
    for option in options:
        if isinstance(options[option], str):
            selects.append(f"{option} == '{options[option]}'")
        else:
            selects.append(f"{option} == {options[option]}")
    return " and ".join(selects)


def queryDataFrame(df, options):
    select = buildSelect(options)
    return df.query(select)
