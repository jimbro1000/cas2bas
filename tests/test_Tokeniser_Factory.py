import pytest

from formats.Coco_Rsdos_Tokens import RsDosToken
from formats.Coco_Tokens import CoCoToken
from formats.Dragon_Dos_Tokens import DragonDosToken
from formats.Dragon_Tokens import DragonToken
from formats.Tokeniser_Factory import find_tokeniser


def test_given_no_options_find_tokeniser_returns_the_default_dragon_tokens():
    opts = []
    actual = find_tokeniser(opts)
    assert isinstance(actual, DragonToken)


def test_given_an_invalid_option_find_tokeniser_ignores_it():
    opts = ["--rubbish"]
    actual = find_tokeniser(opts)
    assert isinstance(actual, DragonToken)


@pytest.mark.parametrize("test_input", ["--dragondos", "-dd"])
def test_given_a_dragondos_option_find_tokeniser_returns_the_dragondos_tokens(
        test_input):
    opts = [test_input]
    actual = find_tokeniser(opts)
    assert isinstance(actual, DragonDosToken)


@pytest.mark.parametrize("test_input", ["--coco", "-cc"])
def test_given_a_coco_option_find_tokeniser_returns_the_coco_tokens(
        test_input):
    opts = [test_input]
    actual = find_tokeniser(opts)
    assert isinstance(actual, CoCoToken)


@pytest.mark.parametrize("test_input", ["--rsdos", "-rd"])
def test_given_a_rsdos_option_find_tokeniser_returns_the_coco_rsdos_tokens(
        test_input):
    opts = [test_input]
    actual = find_tokeniser(opts)
    assert isinstance(actual, RsDosToken)


@pytest.mark.parametrize("test_input, expected", [
    (["-dd", "-rd"], DragonDosToken),
    (["-cc", "-dd"], DragonDosToken),
    (["-rd", "-cc"], CoCoToken)
])
def test_given_conflicting_options_returns_the_highest_priority_tokens(
        test_input, expected):
    actual = find_tokeniser(test_input)
    assert isinstance(actual, expected)
