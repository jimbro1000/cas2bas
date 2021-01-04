def invert_dictionary(source):
    result = {}
    for item in source.items():
        result[item[1]] = item[0]
    return result
