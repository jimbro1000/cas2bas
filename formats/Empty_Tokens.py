from formats.Utility import invert_dictionary

KEYWORD = 0
FUNCTION = 1
MAXIMUM_KEYWORD = 0x80
MAXIMUM_FUNCTION = 0x80
MAXIMUM_TOKEN_LENGTH = 7
FUNCTION_OFFSET = 0xff00
EXPECTING_LINE_NUMBER = 1
EXPECTING_INITIAL_WHITE_SPACE = 2
EXPECTING_TOKEN = 3
EXPECTING_LITERAL_OR_WHITE_SPACE = 4
EXPECTING_STRING_LITERAL = 5
EXPECTING_LITERAL_TO_EOL = 6
CLOSE_LINE = 7
TAB = "\t"
EOL = "\n"
CR = "\r"
SPACE = " "
STRING_DELIMITER = '"'
COLON = ":"
SEMICOLON = ";"
COMMA = ","
STRING_IDENTIFIER = "$"


class EmptyToken(object):
    keyword_token_dictionary = {}

    function_token_dictionary = {}

    reserved_literals = [
        SPACE,
        STRING_DELIMITER,
        COLON,
        CR,
        EOL,
        SEMICOLON,
        COMMA
    ]

    def __init__(self):
        self.state = KEYWORD
        self.max_keyword = MAXIMUM_KEYWORD
        self.max_function = MAXIMUM_FUNCTION
        self.name = "Empty tokens"
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
            if self.max_function > 0:
                self.state = FUNCTION
                return ""
            else:
                return "invalid extension token"
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

    @staticmethod
    def is_numeric(sample):
        return "0" <= sample <= "9"

    @staticmethod
    def word_to_bytes(word):
        msb = (word & 0xff00) >> 8
        lsb = word & 0xff
        return msb, lsb

    def parse_line(self, plain):
        """ parse_line "assumes" that the plain input is a correctly
        constructed basic program statement """

        def process_line(char, line_number):
            if self.is_numeric(char):
                line_number += char
                return 1, line_number
            return 0, line_number

        def process_white_space(char):
            if char == SPACE or char == TAB:
                return 1
            else:
                return 0

        def append_to_stream(value, stream):
            if type(value) == str:
                value = ord(value)
            if value > 0xff:
                msb, lsb = self.word_to_bytes(value)
                stream.append(msb)
                stream.append(lsb)
            else:
                stream.append(value)
            return stream

        def build_token(char, sample):
            """ on valid token for next single character return 5
                on numeric character return 4
                on reserved character return 3
                on valid token match return 2
                on no-match return 1"""
            is_reserved = False
            numeric = self.is_numeric(char)
            any_reserved, not_used = self.is_reserved(char)
            sample += char
            if sample == char:
                is_reserved = any_reserved
            valid, test_key = self.match(sample)
            single_valid, single_key = self.match(char)
            if numeric:
                return 4, sample, None
            if is_reserved:
                return 3, sample, None
            elif valid:
                return 2, sample, test_key
            elif single_valid:
                return 5, sample[:-1], single_key
            elif any_reserved:
                return 5, sample[:-1], char
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
                if outcome == 5:
                    while len(token) > 0:
                        statement = append_to_stream(
                            token[0], statement
                        )
                        token = token[1:]
                    if key == EOL or key == CR:
                        state = CLOSE_LINE
                    elif key == COLON:
                        statement = append_to_stream(key, statement)
                        token = ""
                        next_char = plain_array.pop(0)
                    elif key == STRING_DELIMITER:
                        state = EXPECTING_STRING_LITERAL
                        statement = append_to_stream(key, statement)
                        token = ""
                        next_char = plain_array.pop(0)
                    elif key == SEMICOLON or key == COMMA:
                        statement = append_to_stream(key, statement)
                        token = ""
                        next_char = plain_array.pop(0)
                    else:
                        statement = append_to_stream(key, statement)
                        token = ""
                        next_char = plain_array.pop(0)
                elif outcome == 4:
                    while len(token) > 0:
                        statement = append_to_stream(
                            token[0], statement
                        )
                        token = token[1:]
                    token = ""
                    next_char = plain_array.pop(0)
                elif outcome == 3:
                    if token == COLON \
                            or token == SEMICOLON \
                            or token == COMMA:
                        statement = append_to_stream(token, statement)
                        token = ""
                        next_char = plain_array.pop(0)
                    elif token == EOL or token == CR:
                        state = CLOSE_LINE
                    elif token == SPACE:
                        statement = append_to_stream(token, statement)
                        next_char = plain_array.pop(0)
                        token = ""
                    elif token == STRING_DELIMITER:
                        statement = append_to_stream(token, statement)
                        next_char = plain_array.pop(0)
                        token = ""
                        state = EXPECTING_STRING_LITERAL
                elif outcome == 2:
                    state = EXPECTING_TOKEN
                    if token == "ELSE":
                        if statement[-1:][0] != ord(COLON):
                            statement = append_to_stream(COLON, statement)
                    elif token == "REM":
                        state = EXPECTING_LITERAL_TO_EOL
                    elif token == "'":
                        state = EXPECTING_LITERAL_TO_EOL
                    elif token == "DATA":
                        state = EXPECTING_LITERAL_TO_EOL
                    token = ""
                    statement = append_to_stream(key, statement)
                    next_char = plain_array.pop(0)
                elif outcome == 1:
                    if next_char == STRING_IDENTIFIER:
                        while len(token) > 0:
                            statement = append_to_stream(
                                token[0], statement
                            )
                            token = token[1:]
                        token = ""
                    next_char = plain_array.pop(0)
            elif state == EXPECTING_LITERAL_OR_WHITE_SPACE:
                reserved, token = self.is_reserved(next_char)
                if reserved:
                    if token == EOL:
                        state = CLOSE_LINE
                    elif token == CR:
                        next_char = plain_array.pop(0)
                    elif token == ":":
                        statement = append_to_stream(token, statement)
                        state = EXPECTING_TOKEN
                        next_char = plain_array.pop(0)
                        token = ""
                    elif token == '"':
                        statement = append_to_stream(token, statement)
                        state = EXPECTING_STRING_LITERAL
                        next_char = plain_array.pop(0)
                else:
                    statement = append_to_stream(next_char, statement)
                    next_char = plain_array.pop(0)
            elif state == EXPECTING_STRING_LITERAL:
                reserved, token = self.is_reserved(next_char)
                if token == EOL or token == CR:
                    statement = append_to_stream(0, statement)
                    loop = False
                    result = -1
                elif token == STRING_DELIMITER:
                    statement = append_to_stream(token, statement)
                    state = EXPECTING_TOKEN
                    token = ""
                    next_char = plain_array.pop(0)
                else:
                    statement = append_to_stream(next_char, statement)
                    next_char = plain_array.pop(0)
            elif state == EXPECTING_LITERAL_TO_EOL:
                if next_char == EOL:
                    state = CLOSE_LINE
                elif next_char == CR:
                    next_char = plain_array.pop(0)
                else:
                    statement = append_to_stream(next_char, statement)
                    next_char = plain_array.pop(0)
            elif state == CLOSE_LINE:
                statement = append_to_stream(0, statement)
                loop = False
                result = 0
        return result, line, statement

    def parse_program(self, program, load_address):

        def extract_line(plain_text):
            next_eol = plain_text.find(EOL)
            if next_eol == -1:
                if len(plain_text) > 0:
                    next_line = plain_text + EOL
                else:
                    next_line = ""
                remaining = ""
            else:
                next_line = plain_text[:next_eol + 1]
                remaining = plain_text[next_eol + 1:]
            return next_line, remaining

        result = 0
        loop = len(program) > 0
        stream = []
        load_address += 1
        while loop:
            sample, program = extract_line(program)
            if len(sample) > 0:
                result, line_number, line_bytes = self.parse_line(sample)
                if result == 0:
                    load_address += 4 + len(line_bytes)
                    msb, lsb = self.word_to_bytes(load_address)
                    stream += [msb, lsb]
                    msb, lsb = self.word_to_bytes(int(line_number))
                    stream += [msb, lsb]
                    stream += line_bytes
            loop = result == 0 and len(program) > 0
        return result, bytearray(stream)
