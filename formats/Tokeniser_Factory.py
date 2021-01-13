from formats.Coco_Rsdos_Tokens import RsDosToken
from formats.Coco_Tokens import CoCoToken
from formats.Dragon_Dos_Tokens import DragonDosToken
from formats.Dragon_Tokens import DragonToken
from formats.Trs80_Tokens import Trs80Token


def find_tokeniser(options):
    result = DragonToken()
    if len(options) > 0:
        if any([op in ["-dd", "--dragondos"] for op in options]):
            result = DragonDosToken()
        elif any([op in ["-cc", "--coco"] for op in options]):
            result = CoCoToken()
        elif any([op in ["-rd", "--rsdos"] for op in options]):
            result = RsDosToken()
        elif any([op in ["-b2", "--basic2"] for op in options]):
            result = Trs80Token()
    return result
