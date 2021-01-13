from formats.Dragon_Tokens import DragonToken
from formats.Utility import invert_dictionary

MAXIMUM_DOS_KEYWORD = 0xe7
MAXIMUM_DOS_FUNCTION = 0xa8


class DragonDosToken(DragonToken):
    dos_keyword_token_dictionary = {
        0xce: "AUTO",
        0xcf: "BACKUP",
        0xd0: "BEEP",
        0xd1: "BOOT",
        0xd2: "CHAIN",
        0xd3: "COPY",
        0xd4: "CREATE",
        0xd5: "DIR",
        0xd6: "DRIVE",
        0xd7: "DSKINIT",
        0xd8: "FREAD",
        0xd9: "FWRITE",
        0xda: "ERROR",
        0xdb: "KILL",
        0xdc: "LOAD",
        0xdd: "MERGE",
        0xde: "PROTECT",
        0xdf: "WAIT",
        0xe0: "RENAME",
        0xe1: "SAVE",
        0xe2: "SREAD",
        0xe3: "SWRITE",
        0xe4: "VERIFY",
        0xe5: "FROM",
        0xe6: "FLREAD",
        0xe7: "SWAP"
    }

    dos_function_token_dictionary = {
        0xa2: "LOF",
        0xa3: "FREE",
        0xa4: "ERL",
        0xa5: "ERR",
        0xa6: "HIMEM",
        0xa7: "LOC",
        0xa8: "FRE$"
    }

    def __init__(self):
        super().__init__()
        self.keyword_token_dictionary = {**self.keyword_token_dictionary,
                                         **self.dos_keyword_token_dictionary}
        self.function_token_dictionary = {**self.function_token_dictionary,
                                          **self.dos_function_token_dictionary}
        self.max_keyword = MAXIMUM_DOS_KEYWORD
        self.max_function = MAXIMUM_DOS_FUNCTION
        self.name = "DragonDos extended tokens"
        self.keyword_dictionary = invert_dictionary(
            self.keyword_token_dictionary)
        self.function_dictionary = invert_dictionary(
            self.function_token_dictionary)
