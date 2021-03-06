import pytest

from formats import Dragon_Dos_Tokens
from formats import Dragon_Tokens

tokeniser = Dragon_Tokens.DragonToken()
dos_tokeniser = Dragon_Dos_Tokens.DragonDosToken()
EOL = chr(10)


@pytest.fixture(autouse=True)
def before_each():
    tokeniser.state = Dragon_Tokens.KEYWORD
    dos_tokeniser.state = Dragon_Tokens.KEYWORD


@pytest.mark.parametrize("test_input,expected",
                         [(0x96, "CLEAR"), (0xa9, "TROFF"), (0x83, "'")])
def test_when_a_single_byte_token_is_supplied_return_the_token_keyword(
        test_input,
        expected):
    actual = tokeniser.convert(test_input)
    assert actual == expected


def test_given_a_255_byte_set_extended_mode_and_return_none():
    expected = ''
    token_value = 0xFF
    actual = tokeniser.convert(token_value)
    assert actual == expected
    assert tokeniser.state == Dragon_Tokens.FUNCTION


@pytest.mark.parametrize("test_input,expected",
                         [(0x93, "JOYSTK"), (0xA1, "USR"), (0x9C, "VARPTR")])
def test_when_a_two_byte_token_is_supplied_return_the_token_keyword(
        test_input,
        expected):
    tokeniser.convert(0xFF)
    actual = tokeniser.convert(test_input)
    assert actual == expected


@pytest.mark.parametrize("test_input,expected",
                         [(0x41, "A"), (0x42, "B"), (0x53, "S"), (0x28, "(")])
def test_when_an_ascii_value_byte_is_supplied_return_the_equivalent_character(
        test_input,
        expected):
    actual = tokeniser.convert(test_input)
    assert actual == expected


def test_when_an_illegal_single_byte_token_supplied_return_an_error_message():
    expected = "invalid keyword token"
    token_value = 0xFE
    actual = tokeniser.convert(token_value)
    assert actual == expected


def test_when_an_illegal_double_byte_token_supplied_return_an_error_message():
    expected = "invalid function token"
    token_value = 0xB0
    tokeniser.convert(0xFF)
    actual = tokeniser.convert(token_value)
    assert actual == expected


@pytest.mark.parametrize("test_input,expected",
                         [(0x96, "CLEAR"), (0xCE, "AUTO"),
                          (0xDD, "MERGE"), (0xE7, "SWAP")])
def test_when_a_dos_token_is_used_return_a_dos_keyword(test_input, expected):
    actual = dos_tokeniser.convert(test_input)
    assert actual == expected


@pytest.mark.parametrize("test_input,expected",
                         [(0x93, "JOYSTK"), (0xA2, "LOF"),
                          (0xA4, "ERL"), (0xA8, "FRE$")])
def test_when_a_two_byte_dos_token_is_supplied_return_the_token_function(
        test_input,
        expected):
    dos_tokeniser.convert(0xFF)
    actual = dos_tokeniser.convert(test_input)
    assert actual == expected


@pytest.mark.parametrize("test_input,expected",
                         [("invalid", (False, "invalid")),
                          ("bad", (False, "bad"))])
def test_when_invalid_string_is_supplied_to_match_return_a_false_string_tuple(
        test_input,
        expected):
    actual = tokeniser.match(test_input)
    assert actual == expected


@pytest.mark.parametrize("test_input,expected",
                         [("PRINT", (True, 0x87)),
                          ("USING", (True, 0xcd))])
def test_when_a_known_keyword_string_is_supplied_return_a_true_token_tuple(
        test_input,
        expected):
    actual = tokeniser.match(test_input)
    assert actual == expected


@pytest.mark.parametrize("test_input,expected",
                         [("SGN", (True, 0xff80)), ("VARPTR", (True, 0xff9c))])
def test_when_a_known_function_string_is_supplied_return_a_true_token_tuple(
        test_input,
        expected):
    actual = tokeniser.match(test_input)
    assert actual == expected


def test_given_a_valid_line_string_build_a_tokenised_string():
    sample = "10 STOP\n"
    result, line, actual = tokeniser.parse_line(sample)
    assert result == 0
    assert line == "10"
    assert actual == [0x92, 0]


def test_given_an_input_without_a_terminated_string_result_is_negative():
    sample = '10 PRINT"HELLO WORL\n'
    result, line, actual = tokeniser.parse_line(sample)
    assert result == -1


def test_given_a_goto_statement_result_is_correctly_two_tokens():
    sample = "10 GOTO 10\n"
    result, line, actual = tokeniser.parse_line(sample)
    assert result == 0
    assert line == "10"
    assert actual == [0x81, 0xbc, 0x20, 0x31, 0x30, 0]


def test_given_a_gosub_statment_result_is_correctly_two_tokens():
    sample = "10 GOSUB20\n"
    result, line, actual = tokeniser.parse_line(sample)
    assert result == 0
    assert line == "10"
    assert actual == [0x81, 0xbd, 0x32, 0x30, 0]


def test_given_a_valid_program_build_a_token_stream():
    load_address = 0x1E20
    sample = '10 PRINT"HELLO WORLD";\n20 GOTO 10\n'
    result, stream = tokeniser.parse_program(sample, load_address)
    assert result == 0
    assert len(stream) > 0


def test_given_a_variable_assignment_result_is_correctly_encoded():
    sample = "10 A=B+C\n"
    result, line, actual = tokeniser.parse_line(sample)
    assert result == 0
    assert line == "10"
    assert actual == [0x41, 0xcb, 0x42, 0xc3, 0x43, 0]


def test_given_multiple_sublines_encode_tokens_correctly():
    expected = [0x80, 0x49, 0xcb, 0x31, 0xbc, 0x31, 0x32, 0x3a,
                0x8d, 0x41, 0x24, 0x28, 0x49, 0x29, 0x3a,
                0x8b, 0x3a,
                0x80, 0x49, 0xcb, 0x31, 0xbc, 0x37, 0x3a,
                0x8d, 0x42, 0x24, 0x28, 0x49, 0x29, 0x2c, 0x42,
                0x4d, 0x28, 0x49, 0x29, 0x3a,
                0x8b, 0x3a,
                0x80, 0x49, 0xcb, 0x31, 0xbc, 0x37, 0x3a,
                0x8d, 0x43, 0x24, 0x28, 0x49, 0x29, 0x3a,
                0x8b, 0x3a,
                0x81, 0xbd, 0x32, 0x30, 0x32, 0x30, 0x00]
    sample = '20 FORI=1TO12:READA$(I):NEXT:FORI=1TO7:READB$(I),' \
             'BM(I):NEXT:FORI=1TO7:READC$(I):NEXT:GOSUB2020\n'
    result, line, actual = tokeniser.parse_line(sample)
    assert result == 0
    assert line == "20"
    assert actual == expected


def test_string_literal_at_end_of_subline_is_one_byte():
    expected = [0x87, 0x22, 0x48, 0x45, 0x4c, 0x4c, 0x4f, 0x20,
                0x57, 0x4f, 0x52, 0x4c, 0x44, 0x22, 0x3b, 0x3a,
                0x81, 0xbc, 0x31, 0x30, 0]
    sample = '10 PRINT"HELLO WORLD";:GOTO10\n'
    result, line, actual = tokeniser.parse_line(sample)
    assert result == 0
    assert line == "10"
    assert actual == expected


def test_dont_add_extra_colon_before_else_if_not_needed():
    expected = [0x85, 0x41, 0x53, 0x20, 0xBF, 0x31, 0x38, 0x30,
                0x3A, 0x84, 0x31, 0x30, 0x30, 0x00]
    sample = "300 IFAS THEN180:ELSE100\n"
    result, line, actual = tokeniser.parse_line(sample)
    assert result == 0
    assert line == "300"
    assert actual == expected


def test_semicolon_resets_token_search():
    expected = [0x87, 0x40, 0x36, 0x34, 0x2C, 0x22, 0x58, 0x20,
                0x43, 0x4F, 0x2D, 0x4F, 0x52, 0x44, 0x22, 0x3B,
                0xFF, 0x8C, 0x28, 0x33, 0x32, 0x32, 0x36, 0x36,
                0x29, 0x00]
    sample = '310 PRINT@64,"X CO-ORD";PEEK(32266)\n'
    result, line, actual = tokeniser.parse_line(sample)
    assert result == 0
    assert line == "310"
    assert actual == expected


def test_comma_resets_token_search():
    expected = [0x87, 0x40, 0x36, 0x34, 0x2C, 0x22, 0x22, 0x3A,
                0x87, 0x3A, 0x87, 0x20, 0xCD, 0x22, 0x25, 0x20,
                0x20, 0x20, 0x25, 0x23, 0x23, 0x23, 0x2C, 0x23,
                0x23, 0x23, 0x2C, 0x23, 0x23, 0x23, 0x2C, 0x23,
                0x23, 0x23, 0x22, 0x3B, 0x22, 0x43, 0x41, 0x53,
                0x48, 0x3A, 0x22, 0x2C, 0xFF, 0x8C, 0x28, 0x33,
                0x32, 0x30, 0x35, 0x33, 0x29, 0xC5, 0x31, 0x36,
                0x37, 0x37, 0x37, 0x32, 0x31, 0x36, 0xC3, 0xFF,
                0x8C, 0x28, 0x33, 0x32, 0x30, 0x35, 0x34, 0x29,
                0xC5, 0x36, 0x35, 0x35, 0x33, 0x36, 0xC3, 0xFF,
                0x8C, 0x28, 0x33, 0x32, 0x30, 0x35, 0x35, 0x29,
                0xC5, 0x32, 0x35, 0x36, 0xC3, 0xFF, 0x8C, 0x28,
                0x33, 0x32, 0x30, 0x35, 0x36, 0x29, 0x00]
    sample = '380 PRINT@64,"":PRINT:PRINT USING"%   %###,###,###,###";' \
             '"CASH:",PEEK(32053)*16777216+PEEK(32054)*65536+PEEK(32055)' \
             '*256+PEEK(32056)\n'
    result, line, actual = tokeniser.parse_line(sample)
    assert result == 0
    assert line == "380"
    assert actual == expected


def test_dollar_always_means_end_of_string_variable_or_token():
    expected = [0x85, 0xFF, 0x96, 0x28, 0x42, 0x24, 0x28, 0x49,
                0x29, 0x2C, 0x31, 0x29, 0xCB, 0x41, 0x53, 0x24,
                0xBF, 0x49, 0x54, 0xCB, 0x49, 0x3A, 0x49, 0xCB,
                0x31, 0x30, 0x00]
    sample = '510 IFLEFT$(B$(I),1)=AS$THENIT=I:I=10\n'
    result, line, actual = tokeniser.parse_line(sample)
    assert result == 0
    assert line == "510"
    assert actual == expected


def test_parentheses_are_delimiters_too():
    expected = [0x85, 0x20, 0x41, 0x53, 0xCC, 0x30, 0x20, 0xC9,
                0x20, 0x41, 0x53, 0xCA, 0x42, 0x4D, 0x28, 0x49,
                0x54, 0x29, 0xBF, 0x35, 0x34, 0x30, 0x00]
    sample = '550 IF AS<0 OR AS>BM(IT)THEN540\n'
    result, line, actual = tokeniser.parse_line(sample)
    assert result == 0
    assert line == "550"
    assert actual == expected


def test_end_of_program_needs_double_null():
    expected = bytearray(b'\x1e\x0b\x00\n\x81\xbc 10\x00\x00\x00')
    sample = "10 GOTO 10\n"
    result, actual = tokeniser.parse_program(sample, 0x1e00)
    assert result == 0
    assert actual == expected
