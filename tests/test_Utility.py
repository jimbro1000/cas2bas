import pytest

from formats.Utility import invert_dictionary, find_verbosity, find_binary_flag


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


@pytest.mark.parametrize("test_input", ["-b", "--binary"])
def test_evaluate_true_for_binary_flag(test_input):
    opts = [test_input]
    actual = find_binary_flag(opts)
    assert actual == True


@pytest.mark.parametrize("test_input", ["--silent", "-q", ""])
def test_evaluate_false_for_binary_flag(test_input):
    opts = [test_input]
    actual = find_binary_flag(opts)
    assert actual == False

def test_find_program_name_returns_value_after_p_option():
    from formats.Utility import find_program_name
    assert find_program_name(["-q", "-p", "GAME"]) == "GAME"


def test_find_program_name_returns_value_as_upper_case():
    from formats.Utility import find_program_name
    assert find_program_name(["-q", "-p", "work"]) == "WORK"


def test_find_program_name_returns_none_when_absent_or_missing_value():
    from formats.Utility import find_program_name
    assert find_program_name([]) is None
    assert find_program_name(["-q"]) is None
    assert find_program_name(["-q", "-p"]) is None
