import cas2bas.Main
import formats.Cas_Format
from formats.Dragon_Tokens import DragonToken


def test_given_a_valid_filename_initialise_the_formatter(mocker):
    filename = 'source'
    mocker.patch("builtins.open")
    result = cas2bas.Main.initialise_formatter(filename, DragonToken(), 1)
    open.assert_called_once_with(filename, 'rb')
    assert isinstance(result.tokeniser, DragonToken)


# semi-integration test with mocked IO
def test_given_a_valid_file_and_tokeniser_generate_a_listing_file(mocker):
    mocker.patch("builtins.open")
    mocker.patch("builtins.print")
    stream = [
        formats.Cas_Format.LEADER,
        formats.Cas_Format.SYNC,
        formats.Cas_Format.NAME_FILE_BLOCK,
        0,
        0x41,
        0x20,
        0x20,
        0x20,
        0x20,
        0x20,
        0x20,
        0x20,
        formats.Cas_Format.BASIC_FILE_IDENTIFIER,
        formats.Cas_Format.ASCII_FILE_FLAG,
        formats.Cas_Format.CONTINUOUS_FILE,
        0,
        0,
        0,
        0,
        0,
        formats.Cas_Format.LEADER,
        formats.Cas_Format.LEADER,
        formats.Cas_Format.SYNC,
        formats.Cas_Format.DATA_BLOCK,
        3,
        0,
        0,
        0,
        0,
        formats.Cas_Format.LEADER,
        formats.Cas_Format.LEADER,
        formats.Cas_Format.SYNC,
        formats.Cas_Format.DATA_BLOCK,
        3,
        0x0A,
        0x92,
        0,
        0,
        formats.Cas_Format.LEADER,
        formats.Cas_Format.LEADER,
        formats.Cas_Format.SYNC,
        formats.Cas_Format.END_OF_FILE_BLOCK]
    formatter = formats.Cas_Format.CasFormat(stream, DragonToken(), 1)
    subject = cas2bas.Main.Main()
    subject.filename = "testfile"
    subject.output = "textfile"
    subject.process_cas(formatter)
    open.assert_called_once_with("textfile", "w")
    print.assert_any_call("Located program A")
    print.assert_any_call("textfile extracted from testfile \
using \033[1mDragon Tokens\033[0m")
