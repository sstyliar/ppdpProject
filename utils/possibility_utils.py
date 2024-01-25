import numpy as np
from utils import aux_utils


def getDiseasePossibilitiesForFields(hospitalRows, knownFields):
    matchingRows = aux_utils.queryDataFrame(hospitalRows, knownFields)
    totalDiseases = np.unique(matchingRows["disease"])

    # Get the count of occurrences in the matched set
    occurrences = {}
    for value in matchingRows['disease']:
        occurrences[value] = occurrences.get(value, 0) + 1

    # Calculate the possibilities for each disease
    possibilities = []
    for disease in totalDiseases:
        if disease in occurrences:
            possibility = occurrences[disease] / len(matchingRows) * 100
        else:
            possibility = 0
        possibilities.append((disease.replace("'", ""), possibility))

    # Sort them in descending order based on possibility
    return sorted(possibilities, key=lambda tup: tup[1], reverse=True)


def getCertainDiseaseForCitizens(hospitalRows, citizensRows):
    ret = []
    # For each citizen query the hospital data
    for index, row in citizensRows.iterrows():
        select = {"sex": row["sex"], "race": row["race"], "age": row["age"]}
        matchingRows = aux_utils.queryDataFrame(hospitalRows, select)
        # If it returns only one result then we can be sure that the patient has a specific disease
        if len(matchingRows) == 1:
            ret.append((row["name"], matchingRows["disease"].item().replace("'", "")))
    return ret


def getPossibilitiesResults(data):
    hospitalRows = data["hospital_data"]["rows"]
    citizensRows = data["citizens_data"]["rows"]

    # a. calculate the possibility that given specific known fields
    # someone could deduce the illness of an individual from the list
    knownFields = {"sex": "male", "race": "White: British", "age": 70}
    diseasePossibilities = getDiseasePossibilitiesForFields(hospitalRows, knownFields)

    # b. is there a direct correlation between the hospital and the citizens table?
    certainDiseases = getCertainDiseaseForCitizens(hospitalRows, citizensRows)

    return {
        "known_fields": knownFields,
        "disease_possibilities": diseasePossibilities,
        "certain_diseases": certainDiseases
    }
