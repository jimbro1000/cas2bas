import pytest

from formats.Utility import invert_dictionary, find_verbosity


def test_given_an_empty_dictionary_invert_dictionary_returns_empty():
    source = {}
    expected = {}
    actual = invert_dictionary(source)
    assert actual == expected


def test_given_a_dictionary_invert_dictionary_returns_inverse_dictionary():
    source = {
        0x80: "FOR",
        0x81: "GO"
    }
    expected = {
        "FOR": 0x80,
        "GO": 0x81
    }
    actual = invert_dictionary(source)
    assert actual == expected


@pytest.mark.parametrize("test_input", ["-s", "--silent"])
def test_given_a_silent_option_find_verbosity_sets_to_silent(test_input):
    opts = [test_input]
    actual = find_verbosity(opts)
    assert actual == 3


@pytest.mark.parametrize("test_input", ["--quiet", "-q"])
def test_given_a_quiet_option_find_verbosity_sets_to_quiet(test_input):
    opts = [test_input]
    actual = find_verbosity(opts)
    assert actual == 2


@pytest.mark.parametrize("test_input", ["--verbose", "-v"])
def test_given_a_verbose_option_find_verbosity_sets_to_noisy(test_input):
    opts = [test_input]
    actual = find_verbosity(opts)
    assert actual == 0


@pytest.mark.parametrize("test_input", ["--any", "-dd"])
def test_not_given_any_verbosity_options_find_verbosity_sets_to_normal(
        test_input):
    opts = [test_input]
    actual = find_verbosity(opts)
    assert actual == 1
