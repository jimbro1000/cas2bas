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


def find_header_length(options, default):
    result = default
    if len(options) > 0:
        index = 0
        loop = True
        while loop:
            switch = options[index]
            index += 1
            if switch == "-h" or switch == "--header":
                if index <= len(options):
                    value = options[index]
                    if value.isnumeric():
                        result = int(value)
                        if 0 < result <= 65535:
                            result = default
                loop = False
            loop = loop and index <= len(options)
    return result


def find_base_load_address(options, default):
    result = default
    if len(options) > 0:
        index = 0
        loop = True
        while loop:
            switch = options[index]
            index += 1
            if switch == "-b" or switch == "--base":
                if index <= len(options):
                    value = options[index]
                    safe, result = string_to_number(value)
                    if safe:
                        if result <= 0 or result >= 65535:
                            result = default
                    else:
                        result = default
                loop = False
            loop = loop and index <= len(options)
    return result


def string_to_number(string_value):
    if string_value.isnumeric():
        return True, int(string_value)
    else:
        if len(string_value) > 3:
            if string_value[:2] == "0x":
                return True, int(string_value, 0)
            else:
                return False, None
        else:
            return False, None
