from formats.Coco_Tokens import CoCoToken, RsDosToken
from formats.Dragon_Tokens import DragonToken, DragonDosToken


def find_tokeniser(options):
    result = DragonToken()
    if len(options) > 0:
        if any([op in ["-dd", "--dragondos"] for op in options]):
            result = DragonDosToken()
        elif any([op in ["-cc", "--coco"] for op in options]):
            result = CoCoToken()
        elif any([op in ["-rd", "--rsdos"] for op in options]):
            result = RsDosToken()
    return result
