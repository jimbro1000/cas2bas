from formats.Coco_Tokens import CoCoToken
from formats.Utility import invert_dictionary

MAXIMUM_DOS_KEYWORD = 0xe0
MAXIMUM_DOS_FUNCTION = 0xa6


class RsDosToken(CoCoToken):
    dos_keyword_token_dictionary = {
        0xce: "DIR",
        0xcf: "DRIVE",
        0xd0: "FIELD",
        0xd1: "FILES",
        0xd2: "KILL",
        0xd3: "LOAD",
        0xd4: "LSET",
        0xd5: "MERGE",
        0xd6: "RENAME",
        0xd7: "RSET",
        0xd8: "SAVE",
        0xd9: "WRITE",
        0xda: "VERIFY",
        0xdb: "UNLOAD",
        0xdc: "DSKINI",
        0xdd: "BACKUP",
        0xde: "COPY",
        0xdf: "DSKI$",
        0xe0: "DSKO$"
    }

    dos_function_token_dictionary = {
        0xa2: "CVN",
        0xa3: "FREE",
        0xa4: "LOC",
        0xa5: "LOF",
        0xa6: "MKN$"
    }

    def __init__(self):
        super().__init__()
        self.keyword_token_dictionary = {**self.keyword_token_dictionary,
                                         **self.dos_keyword_token_dictionary}
        self.function_token_dictionary = {**self.function_token_dictionary,
                                          **self.dos_function_token_dictionary}
        self.max_keyword = MAXIMUM_DOS_KEYWORD
        self.max_function = MAXIMUM_DOS_FUNCTION
        self.name = "Coco Extended RSDOS tokens"
        self.keyword_dictionary = invert_dictionary(
            self.keyword_token_dictionary)
        self.function_dictionary = invert_dictionary(
            self.function_token_dictionary)
