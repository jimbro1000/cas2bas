def invert_dictionary(source):
    result = {}
    for item in source.items():
        result[item[1]] = item[0]
    return result


def find_verbosity(options):
    result = 1
    if len(options) > 0:
        if any([op in ["-s", "--silent"] for op in options]):
            result = 3
        if any([op in ["-q", "--quiet"] for op in options]):
            result = 2
        if any([op in ["-v", "--verbose"] for op in options]):
            result = 0
    return result
