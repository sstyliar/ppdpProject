from utils import aux_utils
from bigtree import Node


def generaliseStrColumn(values, nodeName):
    node = Node(nodeName)
    sortedRacesByBlanket = {}
    for val in values:
        parts = val.split(':', 2)
        if parts[0] in sortedRacesByBlanket:
            sortedRacesByBlanket[parts[0]].append(parts[1])
        else:
            sortedRacesByBlanket[parts[0]] = [parts[1]]

    # Create nodes from sorted races, eg {"white": [Irish, Chinese, ...]}
    for key in sortedRacesByBlanket:
        childNode = Node(key)
        for race in sortedRacesByBlanket[key]:
            childNode.append(Node(race))
        node.append(childNode)

    return node


# Splits the integers list to n parts of ranges
def partition(lst, n):
    division = len(lst) / n
    tmp = []
    for i in range(n):
        start = round(division * i)
        end = round(division * (i + 1))
        tmp.append(lst[start:end])
    return tmp


# Generalise int data types
def generaliseIntColumn(values, levels, nodeName):
    if levels == 0:
        return None
    node = Node(nodeName)
    parts = partition(values, 2)
    for i in range(0, 2):  # two children for each node
        childValue = parts[i]
        childNode = generaliseIntColumn(childValue, levels - 1, aux_utils.rangeToHumanReadable(childValue))
        if childNode:
            node.append(childNode)
    return node


# Split logic based on column data type
def generaliseValues(values, nodeName, dataType):
    if dataType == 'int':
        node = generaliseIntColumn(values, 3, nodeName)
    elif dataType == 'str':
        node = generaliseStrColumn(values, nodeName)
    else:
        raise Exception("Unimplemented data type for generalization")
    return node
