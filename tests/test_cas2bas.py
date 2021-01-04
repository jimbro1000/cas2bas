import pytest

from cas2bas.Main import Main, find_tokeniser, initialise_formatter, find_verbosity
from formats.Cas_Format import LEADER, SYNC, NAME_FILE_BLOCK, BASIC_FILE_IDENTIFIER, ASCII_FILE_FLAG, CONTINUOUS_FILE, \
    DATA_BLOCK, END_OF_FILE_BLOCK, CasFormat
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
    result = initialise_formatter(filename, DragonToken(), 1)
    open.assert_called_once_with(filename, 'rb')
    assert isinstance(result.tokeniser, DragonToken)


# semi-integration test with mocked IO
def test_given_a_valid_file_and_tokeniser_generate_a_listing_file(mocker):
    mocker.patch("builtins.open")
    mocker.patch("builtins.print")
    stream = [
        LEADER,
        SYNC,
        NAME_FILE_BLOCK,
        0,
        0x41,
        0x20,
        0x20,
        0x20,
        0x20,
        0x20,
        0x20,
        0x20,
        BASIC_FILE_IDENTIFIER,
        ASCII_FILE_FLAG,
        CONTINUOUS_FILE,
        0,
        0,
        0,
        0,
        0,
        LEADER,
        LEADER,
        SYNC,
        DATA_BLOCK,
        3,
        0,
        0,
        0,
        0,
        LEADER,
        LEADER,
        SYNC,
        DATA_BLOCK,
        3,
        0x0A,
        0x92,
        0,
        0,
        LEADER,
        LEADER,
        SYNC,
        END_OF_FILE_BLOCK]
    formatter = CasFormat(stream, DragonToken(), 1)
    subject = Main()
    subject.filename = "testfile"
    subject.output = "textfile"
    subject.process_cas(formatter)
    open.assert_called_once_with("textfile", "w")
    print.assert_any_call("Located program A")
    print.assert_any_call("textfile extracted from testfile using \x1b[1mDragon tokens\x1b[0m")


@pytest.mark.parametrize("test_input", ["--silent", "-s"])
def test_given_a_silent_option_find_verbosity_sets_to_silent(test_input):
    opts = [test_input]
    actual = find_verbosity(opts)
    assert actual == 3


@pytest.mark.parametrize("test_input", ["--quiet", "-q"])
def test_given_a_quiet_option_find_verbosity_sets_to_silent(test_input):
    opts = [test_input]
    actual = find_verbosity(opts)
    assert actual == 2


@pytest.mark.parametrize("test_input", ["--verbose", "-v"])
def test_given_a_verbose_option_find_verbosity_sets_to_noisy(test_input):
    opts = [test_input]
    actual = find_verbosity(opts)
    assert actual == 0


@pytest.mark.parametrize("test_input", ["--any", "-dd"])
def test_not_given_any_verbosity_options_find_verbosity_sets_to_normal(test_input):
    opts = [test_input]
    actual = find_verbosity(opts)
    assert actual == 1