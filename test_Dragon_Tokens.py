import pytest

import Dragon_Tokens

tokeniser = Dragon_Tokens.DragonToken()


@pytest.fixture(autouse=True)
def before_each():
    tokeniser.state = Dragon_Tokens.NORMAL


@pytest.mark.parametrize("test_input,expected", [(0x96, "CLEAR"), (0xa9, "TROFF"), (0x83, "'")])
def test_when_a_single_byte_token_is_supplied_return_the_token_keyword(test_input, expected):
    actual = tokeniser.convert(test_input)
    assert actual == expected


def test_when_a_single_byte_value_of_255_is_supplied_no_result_is_returned_and_the_next_byte_is_treated_as_extended():
    expected = ''
    token_value = 0xFF
    actual = tokeniser.convert(token_value)
    assert actual == expected
    assert tokeniser.state == Dragon_Tokens.EXTENDED


@pytest.mark.parametrize("test_input,expected", [(0x93, "JOYSTK"), (0xA1, "USR"), (0x9C, "VARPTR")])
def test_when_a_two_byte_token_is_supplied_return_the_token_keyword(test_input, expected):
    tokeniser.convert(0xFF)
    actual = tokeniser.convert(test_input)
    assert actual == expected


@pytest.mark.parametrize("test_input,expected", [(0x41, "A"), (0x42, "B"), (0x53, "S"), (0x28, "(")])
def test_when_an_ascii_value_byte_is_supplied_return_the_equivalent_character(test_input, expected):
    actual = tokeniser.convert(test_input)
    assert actual == expected


def test_when_an_illegal_single_byte_token_is_supplied_return_an_error_message():
    expected = "invalid byte token"
    token_value = 0xFE
    actual = tokeniser.convert(token_value)
    assert actual == expected


def test_when_an_illegal_double_byte_token_is_supplied_return_an_error_message():
    expected = "invalid extended token"
    token_value = 0xB0
    tokeniser.convert(0xFF)
    actual = tokeniser.convert(token_value)
    assert actual == expected
