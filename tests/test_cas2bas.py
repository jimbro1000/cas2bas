import pytest

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


def test_given_a_program_name_skip_other_programs_and_extract_it(mocker):
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
        formats.Cas_Format.END_OF_FILE_BLOCK,
        formats.Cas_Format.LEADER,
        formats.Cas_Format.SYNC,
        formats.Cas_Format.NAME_FILE_BLOCK,
        0,
        0x42,
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
    subject.program = "B"
    subject.process_cas(formatter)
    open.assert_called_once_with("textfile", "w")
    print.assert_any_call("Skipped program A")
    print.assert_any_call("Located program B")
    print.assert_any_call("textfile extracted from testfile \
using \033[1mDragon Tokens\033[0m")


def test_given_a_program_name_not_in_file_report_not_found(mocker):
    mocker.patch("builtins.open")
    mocker.patch("builtins.print")
    stream = [
        formats.Cas_Format.LEADER,
        formats.Cas_Format.SYNC,
        formats.Cas_Format.NAME_FILE_BLOCK,
        0,
        0x41, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20,
        formats.Cas_Format.BASIC_FILE_IDENTIFIER,
        formats.Cas_Format.ASCII_FILE_FLAG,
        formats.Cas_Format.CONTINUOUS_FILE,
        0, 0, 0, 0, 0,
        formats.Cas_Format.LEADER,
        formats.Cas_Format.LEADER,
        formats.Cas_Format.SYNC,
        formats.Cas_Format.DATA_BLOCK,
        3, 0, 0, 0, 0,
        formats.Cas_Format.LEADER,
        formats.Cas_Format.LEADER,
        formats.Cas_Format.SYNC,
        formats.Cas_Format.END_OF_FILE_BLOCK,
        0,
        0xFF]
    formatter = formats.Cas_Format.CasFormat(stream, DragonToken(), 1)
    subject = cas2bas.Main.Main()
    subject.filename = "testfile"
    subject.output = "textfile"
    subject.program = "B"
    with pytest.raises(SystemExit) as exit_info:
        subject.process_cas(formatter)
    assert exit_info.value.code == 1
    open.assert_not_called()
    print.assert_any_call("Skipped program A")
    print.assert_any_call("Program B not found")


def build_segment(name, file_id, data_blocks):
    """Builds a cas segment with a full length header block"""
    cas = formats.Cas_Format
    padded = [ord(c) for c in name.ljust(8)]
    segment = [cas.LEADER, cas.SYNC, cas.NAME_FILE_BLOCK, 15] + padded + \
        [file_id, cas.BINARY_FILE_FLAG, cas.CONTINUOUS_FILE,
         0, 0, 0, 0, 0]
    for block in data_blocks:
        segment += [cas.LEADER, cas.LEADER, cas.SYNC, cas.DATA_BLOCK,
                    len(block)] + block + [0]
    segment += [cas.LEADER, cas.LEADER, cas.SYNC, cas.END_OF_FILE_BLOCK,
                0, 0xFF, cas.LEADER]
    return segment


def test_given_a_program_name_skip_segments_that_are_not_basic(mocker):
    mocker.patch("builtins.open")
    mocker.patch("builtins.print")
    stream = build_segment(
        "M", formats.Cas_Format.BINARY_FILE_IDENTIFIER,
        [[0x55, 0x3C, 0x01, 0xFF]]) + \
        build_segment(
            "B", formats.Cas_Format.BASIC_FILE_IDENTIFIER,
            [[0, 0, 0, 0x0A, 0x92, 0]])
    formatter = formats.Cas_Format.CasFormat(stream, DragonToken(), 1)
    subject = cas2bas.Main.Main()
    subject.filename = "testfile"
    subject.output = "textfile"
    subject.program = "B"
    subject.process_cas(formatter)
    open.assert_called_once_with("textfile", "w")
    print.assert_any_call("Skipped program M")
    print.assert_any_call("Located program B")
    assert subject.result == "10 STOP\n"


def test_given_a_program_name_that_is_not_basic_and_binary_flag_not_set_report_error(mocker):
    mocker.patch("builtins.open")
    mocker.patch("builtins.print")
    stream = build_segment(
        "B", formats.Cas_Format.BASIC_FILE_IDENTIFIER,
        [[0, 0, 0, 0x0A, 0x92, 0]]) + \
        build_segment(
            "M", formats.Cas_Format.BINARY_FILE_IDENTIFIER, [[1, 2, 3]])
    formatter = formats.Cas_Format.CasFormat(stream, DragonToken(), 1)
    subject = cas2bas.Main.Main()
    subject.filename = "testfile"
    subject.output = "textfile"
    subject.program = "M"
    with pytest.raises(SystemExit) as exit_info:
        subject.process_cas(formatter)
    assert exit_info.value.code == 1
    open.assert_not_called()
    print.assert_any_call("Skipped program B")
    print.assert_any_call("not a basic listing")


def test_given_binary_flag_is_set_extract_binary_block_instead_of_reporting_error(mocker):
    mocker.patch("builtins.open")
    mocker.patch("builtins.print")
    stream = build_segment(
        "A", formats.Cas_Format.BINARY_FILE_IDENTIFIER,
        [[0,0,0x17,0xFF,0x1E,0x00,0x0D],[1,2,3,4,5,6,7,8,9]])
    formatter = formats.Cas_Format.CasFormat(stream, DragonToken(), 1)
    subject = cas2bas.Main.Main()
    subject.filename = "testfile"
    subject.output = "textfile"
    with pytest.raises(SystemExit) as exit_info:
        subject.process_cas(formatter)
    assert exit_info.value.code == 0
    open.assert_called_once_with("textfile", "w")
    print.assert_any_call("Located program A")
    print.assert_any_call("textfile extracted from testfile \
using \033[1mDragon Tokens\033[0m")
