# Returns the count of the identical rows sorted in ASC order
def getDuplicatesCounts(rows, qi_group):
    duplicatesCounts = rows.pivot_table(index=qi_group, aggfunc='size')
    return sorted(duplicatesCounts)


# Get the K Anonymity value for the dataframe
def getKAnonymity(data):
    duplicates = getDuplicatesCounts(data["rows"], data["qi_group"])
    return min(duplicates)
