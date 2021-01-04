import pytest

from cas2bas.Main import find_tokeniser, initialise_formatter
from formats.Coco_Tokens import CoCoToken, RsDosToken
from formats.Dragon_Tokens import DragonToken, DragonDosToken


def test_given_no_options_find_tokeniser_returns_the_default_dragon_tokeniser():
    opts = []
    actual = find_tokeniser(opts)
    assert isinstance(actual, DragonToken)


def test_given_an_invalid_option_find_tokeniser_ignores_it():
    opts = ["--rubbish"]
    actual = find_tokeniser(opts)
    assert isinstance(actual, DragonToken)


@pytest.mark.parametrize("test_input", ["--dragondos", "-dd"])
def test_given_a_dragondos_option_find_tokeniser_returns_the_extended_dragondos_tokeniser(test_input):
    opts = [test_input]
    actual = find_tokeniser(opts)
    assert isinstance(actual, DragonDosToken)


@pytest.mark.parametrize("test_input", ["--coco", "-cc"])
def test_given_a_coco_option_find_tokeniser_returns_the_coco_tokeniser(test_input):
    opts = [test_input]
    actual = find_tokeniser(opts)
    assert isinstance(actual, CoCoToken)


@pytest.mark.parametrize("test_input", ["--rsdos", "-rd"])
def test_given_a_rsdos_option_find_tokeniser_returns_the_extended_coco_rsdos_tokeniser(test_input):
    opts = [test_input]
    actual = find_tokeniser(opts)
    assert isinstance(actual, RsDosToken)


@pytest.mark.parametrize("test_input, expected", [
    (["-dd", "-rd"], DragonDosToken),
    (["-cc", "-dd"], DragonDosToken),
    (["-rd", "-cc"], CoCoToken)
])
def test_given_multiple_conflicting_options_returns_the_highest_priority_tokeniser(test_input, expected):
    actual = find_tokeniser(test_input)
    assert isinstance(actual, expected)


def test_given_a_valid_filename_initialise_the_formatter(mocker):
    filename = 'source'
    mocker.patch("builtins.open")
    result = initialise_formatter(filename, DragonToken())
    open.assert_called_once_with(filename, 'rb')
    assert isinstance(result.tokeniser, DragonToken)
