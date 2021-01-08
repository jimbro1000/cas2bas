from formats.Utility import invert_dictionary

KEYWORD = 0
FUNCTION = 1
MAXIMUM_KEYWORD = 0xcd
MAXIMUM_FUNCTION = 0xa1
MAXIMUM_DOS_KEYWORD = 0xe7
MAXIMUM_DOS_FUNCTION = 0xa8
MAXIMUM_TOKEN_LENGTH = 7
FUNCTION_OFFSET = 0xff00
EXPECTING_LINE_NUMBER = 1
EXPECTING_INITIAL_WHITE_SPACE = 2
EXPECTING_TOKEN = 3
EXPECTING_LITERAL_OR_WHITE_SPACE = 4
EXPECTING_STRING_LITERAL = 5
TAB = "\t"
EOL = "\n"
CR = "\r"


class DragonToken(object):
    """Converts byte codes into tokens, or more accurately de-tokenises
    a byte stream one byte at a time."""
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

    reserved_literals = [
        ":",
        '"',
        CR,
        EOL
    ]

    def __init__(self):
        self.state = KEYWORD
        self.max_keyword = MAXIMUM_KEYWORD
        self.max_function = MAXIMUM_FUNCTION
        self.name = "Dragon tokens"
        self.keyword_dictionary = invert_dictionary(
            self.keyword_token_dictionary)
        self.function_dictionary = invert_dictionary(
            self.function_token_dictionary)

    def convert(self, byte):
        """Translates a byte to a string. Ascii characters are literal,
        values over 127 are tokens or token sequences.
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

    def is_reserved(self, sample):
        result = False
        reserved = None
        for item in self.reserved_literals:
            if item == sample:
                result = True
                reserved = item
        return result, reserved

    def parse_line(self, plain):
        """ parse_line "assumes" that the plain input is a correctly
        constructed basic program statement """

        def process_line(char, line_number):
            if '0' <= char <= '9':
                line_number += char
                return 1, line_number
            return 0, line_number

        def process_white_space(char):
            if char == " " or char == TAB:
                return 1
            else:
                return 0

        def build_token(char, sample):
            sample += char
            valid, test_key = self.match(sample)
            if valid:
                return 2, sample, test_key
            elif len(sample) > MAXIMUM_TOKEN_LENGTH:
                return 0, sample, None
            else:
                return 1, sample, None

        plain_array = list(plain)
        state = EXPECTING_LINE_NUMBER
        line = ""
        statement = []
        token = ""

        result = 0
        loop = len(plain_array) > 0
        next_char = plain_array.pop(0)
        while loop:
            if state == EXPECTING_LINE_NUMBER:
                outcome, line = process_line(next_char, line)
                if outcome == 0:
                    state = EXPECTING_INITIAL_WHITE_SPACE
                else:
                    next_char = plain_array.pop(0)
            elif state == EXPECTING_INITIAL_WHITE_SPACE:
                outcome = process_white_space(next_char)
                if outcome == 0:
                    state = EXPECTING_TOKEN
                else:
                    next_char = plain_array.pop(0)
            elif state == EXPECTING_TOKEN:
                outcome, token, key = build_token(next_char, token)
                if outcome == 2:
                    token = ""
                    if key == 0x81:
                        state = EXPECTING_TOKEN
                    else:
                        state = EXPECTING_LITERAL_OR_WHITE_SPACE
                    statement.append(key)
                    next_char = plain_array.pop(0)
                elif outcome == 1:
                    next_char = plain_array.pop(0)
                else:
                    loop = False
                    result = -1
            elif state == EXPECTING_LITERAL_OR_WHITE_SPACE:
                reserved, token = self.is_reserved(next_char)
                if reserved:
                    if token == EOL:
                        statement.append(0)
                        loop = False
                        result = 0
                    elif token == CR:
                        next_char = plain_array.pop(0)
                    elif token == ":":
                        statement.append(ord(token))
                        state = EXPECTING_TOKEN
                        next_char = plain_array.pop(0)
                        token = ""
                    elif token == '"':
                        statement.append(ord(token))
                        state = EXPECTING_STRING_LITERAL
                        next_char = plain_array.pop(0)
                else:
                    statement.append(ord(next_char))
                    next_char = plain_array.pop(0)
            elif state == EXPECTING_STRING_LITERAL:
                reserved, token = self.is_reserved(next_char)
                if reserved:
                    if token == EOL:
                        statement.append(0)
                        loop = False
                        result = -1
                    elif token == CR:
                        next_char = plain_array.pop(0)
                    elif token == '"':
                        statement.append(ord(token))
                        state = EXPECTING_LITERAL_OR_WHITE_SPACE
                        next_char = plain_array.pop(0)
                else:
                    statement.append(ord(next_char))
                    next_char = plain_array.pop(0)
        return result, line, statement

    def parse_program(self, program, load_address):

        def extract_line(plain_text):
            next_eol = plain_text.find(EOL)
            if next_eol == -1:
                next_line = ""
                remaining = ""
            else:
                next_line = plain_text[:next_eol + 1]
                remaining = plain_text[next_eol + 1:]
            return next_line, remaining

        def word_to_bytes(word):
            high_byte = word // 256
            low_byte = word % 256
            return [high_byte, low_byte]

        result = 0
        loop = len(program) > 0
        stream = []
        while loop:
            sample, program = extract_line(program)
            print(sample)
            result, line_number, line_stream = self.parse_line(sample)
            if result == 0:
                load_address += 4 + len(line_stream)
                stream += word_to_bytes(load_address)
                stream += word_to_bytes(int(line_number))
                stream += line_stream
            loop = result == 0 and len(program) > 0
        return result, stream


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
