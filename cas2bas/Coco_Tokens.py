from cas2bas.Dragon_Tokens import DragonToken

KEYWORD = 0
FUNCTION = 1
MAXIMUM_KEYWORD = 0xcd
MAXIMUM_FUNCTION = 0xa1
MAXIMUM_DOS_KEYWORD = 0xe0
MAXIMUM_DOS_FUNCTION = 0xa6


class CoCoToken(DragonToken):
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
        0x8e: "RUN",
        0x8f: "RESTORE",
        0x90: "RETURN",
        0x91: "STOP",
        0x92: "POKE",
        0x93: "CONT",
        0x94: "LIST",
        0x95: "CLEAR",
        0x96: "NEW",
        0x97: "CLOAD",
        0x98: "CSAVE",
        0x99: "OPEN",
        0x9a: "CLOSE",
        0x9b: "LLIST",
        0x9c: "SET",
        0x9d: "RESET",
        0x9e: "CLS",
        0x9f: "MOTOR",
        0xa0: "SOUND",
        0xa1: "AUDIO",
        0xa2: "EXEC",
        0xa3: "SKIPF",
        0xa4: "TAB(",
        0xa5: "TO",
        0xa6: "SUB",
        0xa7: "THEN",
        0xa8: "NOT",
        0xa9: "STEP",
        0xaa: "OFF",
        0xab: "+",
        0xac: "-",
        0xad: "*",
        0xae: "/",
        0xaf: "^",
        0xb0: "AND",
        0xb1: "OR",
        0xb2: ">",
        0xb3: "=",
        0xb4: "<",
        0xb5: "DEL",
        0xb6: "EDIT",
        0xb7: "TRON",
        0xb8: "TROFF",
        0xb9: "DEF",
        0xbb: "LINE",
        0xbc: "PCLS",
        0xbd: "PSET",
        0xbe: "PRESET",
        0xbf: "SCREEN",
        0xc0: "PCLEAR",
        0xc1: "COLOR",
        0xc2: "CIRCLE",
        0xc3: "PAINT",
        0xc4: "GET",
        0xc5: "PUT",
        0xc6: "DRAW",
        0xc7: "PCOPY",
        0xc8: "PMODE",
        0xc9: "PLAY",
        0xca: "DLOAD",
        0xcb: "RENUM",
        0xcc: "FN",
        0xcd: "USING"
    }

    function_token_dictionary = {
        0x80: "SGN",
        0x81: "INT",
        0x82: "ABS",
        0x83: "USR",
        0x84: "RND",
        0x85: "SIN",
        0x86: "PEEK",
        0x87: "LEN",
        0x88: "STR$",
        0x89: "VAL",
        0x8a: "ASC",
        0x8b: "CHR$",
        0x8c: "EOF",
        0x8d: "JOYSTK",
        0x8e: "LEFT$",
        0x8f: "RIGHT$",
        0x90: "MID$",
        0x91: "POINT",
        0x92: "INKEY$",
        0x93: "MEM",
        0x94: "ATN",
        0x95: "COS",
        0x96: "TAN",
        0x97: "EXP",
        0x98: "FIX",
        0x99: "LOG",
        0x9a: "POS",
        0x9b: "SQR",
        0x9c: "HEX$",
        0x9d: "VARPTR",
        0x9e: "INSTR",
        0x9f: "TIMER",
        0xa0: "PPOINT",
        0xa1: "STRING$"
    }

    def __init__(self):
        super().__init__()
        self.max_keyword = MAXIMUM_KEYWORD
        self.max_function = MAXIMUM_FUNCTION
        self.name = "Coco Tokens"


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
