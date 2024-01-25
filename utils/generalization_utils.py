from utils import aux_utils


def getGeneralizationValues(tree, level, config):
    ret = {}
    for column in config["generalization"]["fields"]:
        branch = tree.getBranch(column)
        tmp = tree.getTreeLevel(branch, level)
        if config["generalization"]["fields"][column] == 'int':
            tmp = aux_utils.humanReadableListToRange(tmp)
        ret[column] = tmp
    return ret


def getGeneralizedIntValue(value, possibleReplacements):
    for replacement in possibleReplacements:
        if value in replacement:
            return aux_utils.rangeToHumanReadable(replacement)
    return value


def getGeneralizedStrValue(value, level, possibleReplacements):
    parts = value.split(':', 2)
    part = parts[level - 2]  # Get on the first run the left part aka the blanket and then the right part
    return aux_utils.getMostSimilarStringFromArray(part, possibleReplacements)


def generalizeTable(data, tTree, level, config):
    if level <= 1:
        return data

    generalizationValues = getGeneralizationValues(tTree, level, config)
    rows = data["rows"]

    for column in config["generalization"]["fields"]:
        possibleReplacements = generalizationValues[column]
        for index, value in enumerate(rows[column]):
            if config["generalization"]["fields"][column] == "int":
                replace = getGeneralizedIntValue(value, possibleReplacements)
            elif config["generalization"]["fields"][column] == "str":
                replace = getGeneralizedStrValue(value, level, possibleReplacements)
            else:
                raise Exception("Unimplemented data type for generalization")
            rows.at[index, column] = replace

    return data
