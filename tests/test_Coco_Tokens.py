import pytest

from formats import Coco_Tokens

tokeniser = Coco_Tokens.CoCoToken()
dos_tokeniser = Coco_Tokens.RsDosToken()


@pytest.fixture(autouse=True)
def before_each():
    tokeniser.state = Coco_Tokens.KEYWORD
    dos_tokeniser.state = Coco_Tokens.KEYWORD


@pytest.mark.parametrize("test_input,expected",
                         [(0x92, "POKE"), (0xaa, "OFF"), (0xcb, "RENUM")])
def test_when_a_single_byte_token_is_supplied_return_the_coco_token_keyword(
        test_input,
        expected):
    actual = tokeniser.convert(test_input)
    assert actual == expected


def test_when_a_single_byte_value_of_255_is_supplied_no_result_is_returned_and_the_next_byte_is_treated_as_extended():
    expected = ''
    token_value = 0xFF
    actual = tokeniser.convert(token_value)
    assert actual == expected
    assert tokeniser.state == Coco_Tokens.FUNCTION


@pytest.mark.parametrize("test_input,expected",
                         [(0x8d, "JOYSTK"), (0x93, "MEM"), (0x9d, "VARPTR")])
def test_when_a_two_byte_token_is_supplied_return_the_token_keyword(
        test_input,
        expected):
    tokeniser.convert(0xFF)
    actual = tokeniser.convert(test_input)
    assert actual == expected


@pytest.mark.parametrize("test_input,expected",
                         [(0x96, "NEW"), (0xCE, "DIR"), (0xDD, "BACKUP"), (0xE0, "DSKO$")])
def test_when_a_dos_token_is_used_return_a_dos_keyword(test_input, expected):
    actual = dos_tokeniser.convert(test_input)
    assert actual == expected


@pytest.mark.parametrize("test_input,expected",
                         [(0x93, "MEM"), (0xA2, "CVN"), (0xA4, "LOC"), (0xA6, "MKN$")])
def test_when_a_two_byte_dos_token_is_supplied_return_the_token_function(
        test_input,
        expected):
    dos_tokeniser.convert(0xFF)
    actual = dos_tokeniser.convert(test_input)
    assert actual == expected
