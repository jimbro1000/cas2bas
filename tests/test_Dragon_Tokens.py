import pytest

from formats import Dragon_Tokens

tokeniser = Dragon_Tokens.DragonToken()
dos_tokeniser = Dragon_Tokens.DragonDosToken()
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


def test_given_a_string_without_a_valid_token_result_is_negative():
    sample = "10 STOKERMAN\n"
    result, line, actual = tokeniser.parse_line(sample)
    assert result == -1


def test_given_an_input_without_a_terminated_string_result_is_negative():
    sample = '10 PRINT"HELLO WORL\n'
    result, line, actual = tokeniser.parse_line(sample)
    assert result == -1


def test_given_a_goto_statment_result_is_correctly_two_tokens():
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
