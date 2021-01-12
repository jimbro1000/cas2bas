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
TAB = "\t"
EOL = "\n"
CR = "\r"


class EmptyToken(object):
    keyword_token_dictionary = {}

    function_token_dictionary = {}

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
                if token == EOL:
                    statement.append(0)
                    loop = False
                    result = -1
                    next_char = plain_array.pop(0)
                elif token == CR:
                    pass
                elif token == '"':
                    statement.append(ord(token))
                    state = EXPECTING_LITERAL_OR_WHITE_SPACE
                    next_char = plain_array.pop(0)
                if reserved:
                    pass
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
