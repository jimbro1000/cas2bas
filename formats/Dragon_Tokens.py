from formats.Utility import invert_dictionary

KEYWORD = 0
FUNCTION = 1
MAXIMUM_KEYWORD = 0xcd
MAXIMUM_FUNCTION = 0xa1
MAXIMUM_DOS_KEYWORD = 0xe7
MAXIMUM_DOS_FUNCTION = 0xa8
FUNCTION_OFFSET = 0xff00


class DragonToken(object):
    """Converts byte codes into tokens, or more accurately detokenises a byte stream one byte at a time."""
    keyword_token_dictionary = {
        0x80: "FOR",
        0x81: "GO",
        0x82: "REM",
        0x83: "'",
        0x84: "ELSE",
        0x85: "IF",
        0x86: "DATA",
        0x87: "PRINT",
        0x88: "ON",
        0x89: "INPUT",
        0x8a: "END",
        0x8b: "NEXT",
        0x8c: "DIM",
        0x8d: "READ",
        0x8e: "LET",
        0x8f: "RUN",
        0x90: "RESTORE",
        0x91: "RETURN",
        0x92: "STOP",
        0x93: "POKE",
        0x94: "CONT",
        0x95: "LIST",
        0x96: "CLEAR",
        0x97: "NEW",
        0x98: "DEF",
        0x99: "CLOAD",
        0x9a: "CSAVE",
        0x9b: "OPEN",
        0x9c: "CLOSE",
        0x9d: "LLIST",
        0x9e: "SET",
        0x9f: "RESET",
        0xa0: "CLS",
        0xa1: "MOTOR",
        0xa2: "SOUND",
        0xa3: "AUDIO",
        0xa4: "EXEC",
        0xa5: "SKIPF",
        0xa6: "DEL",
        0xa7: "EDIT",
        0xa8: "TRON",
        0xa9: "TROFF",
        0xaa: "LINE",
        0xab: "PCLS",
        0xac: "PSET",
        0xad: "PRESET",
        0xae: "SCREEN",
        0xaf: "PCLEAR",
        0xb0: "COLOR",
        0xb1: "CIRCLE",
        0xb2: "PAINT",
        0xb3: "GET",
        0xb4: "PUT",
        0xb5: "DRAW",
        0xb6: "PCOPY",
        0xb7: "PMODE",
        0xb8: "PLAY",
        0xb9: "DLOAD",
        0xba: "RENUM",
        0xbb: "TAB(",
        0xbc: "TO",
        0xbd: "SUB",
        0xbe: "FN",
        0xbf: "THEN",
        0xc0: "NOT",
        0xc1: "STEP",
        0xc2: "OFF",
        0xc3: "+",
        0xc4: "-",
        0xc5: "*",
        0xc6: "/",
        0xc7: "^",
        0xc8: "AND",
        0xc9: "OR",
        0xca: ">",
        0xcb: "=",
        0xcc: "<",
        0xcd: "USING"
    }

    function_token_dictionary = {
        0x80: "SGN",
        0x81: "INT",
        0x82: "ABS",
        0x83: "POS",
        0x84: "RND",
        0x85: "SQR",
        0x86: "LOG",
        0x87: "EXP",
        0x88: "SIN",
        0x89: "COS",
        0x8a: "TAN",
        0x8b: "ATN",
        0x8c: "PEEK",
        0x8d: "LEN",
        0x8e: "STR$",
        0x8f: "VAL",
        0x90: "ASC",
        0x91: "CHR$",
        0x92: "EOF",
        0x93: "JOYSTK",
        0x94: "FIX",
        0x95: "HEX$",
        0x96: "LEFT$",
        0x97: "RIGHT$",
        0x98: "MID$",
        0x99: "POINT",
        0x9a: "INKEY$",
        0x9b: "MEM",
        0x9c: "VARPTR",
        0x9d: "INSTR",
        0x9e: "TIMER",
        0x9f: "PPOINT",
        0xa0: "STRING$",
        0xa1: "USR"
    }

    def __init__(self):
        self.state = KEYWORD
        self.max_keyword = MAXIMUM_KEYWORD
        self.max_function = MAXIMUM_FUNCTION
        self.name = "Dragon tokens"
        self.keyword_dictionary = invert_dictionary(self.keyword_token_dictionary)
        self.function_dictionary = invert_dictionary(self.function_token_dictionary)

    def convert(self, byte):
        """Translates a byte to a string. Ascii characters are literal, values over 127 are tokens or token sequences.
        Not all token values are valid."""
        if byte < 128:
            return chr(byte)
        if self.state == FUNCTION:
            if byte <= self.max_function:
                function = self.function_token_dictionary.get(byte)
                self.state = KEYWORD
                return function
            else:
                return "invalid function token"
        if byte == 255:
            self.state = FUNCTION
            return ""
        if byte <= self.max_keyword:
            return self.keyword_token_dictionary.get(byte)
        else:
            return "invalid keyword token"

    def match(self, sample):
        valid = False
        token = sample
        if self.keyword_dictionary.get(sample) is not None:
            valid = True
            token = self.keyword_dictionary.get(sample)
        if not valid and self.function_dictionary.get(sample) is not None:
            valid = True
            token = FUNCTION_OFFSET + self.function_dictionary.get(sample)
        return valid, token


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
        self.keyword_dictionary = invert_dictionary(self.keyword_token_dictionary)
        self.function_dictionary = invert_dictionary(self.function_token_dictionary)
