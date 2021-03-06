import pytest

import formats.Cas_Format
from formats import Dragon_Tokens


def test_given_a_valid_byte_array_returns_a_formatted_string():
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
        6,
        0,
        0,
        0,
        0x0A,
        0x92,
        0,
        0,
        formats.Cas_Format.LEADER,
        formats.Cas_Format.LEADER,
        formats.Cas_Format.SYNC,
        formats.Cas_Format.END_OF_FILE_BLOCK]
    formatter = formats.Cas_Format.CasFormat(
        stream, Dragon_Tokens.DragonToken(), 1
    )
    expected = "10 STOP\n"
    header_pass = formatter.process_header()
    actual = ""
    if header_pass == 0:
        actual = formatter.process_file()
    assert expected == actual


def test_given_a_file_without_a_sync_in_the_header_return_an_error():
    stream = [formats.Cas_Format.LEADER, formats.Cas_Format.NAME_FILE_BLOCK, 0]
    formatter = formats.Cas_Format.CasFormat(
        stream, Dragon_Tokens.DragonToken(), 1
    )
    expected = -1
    actual = formatter.process_header()
    assert expected == actual


def test_given_a_file_without_a_data_block_sync_return_an_error():
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
        formats.Cas_Format.DATA_BLOCK]
    formatter = formats.Cas_Format.CasFormat(
        stream, Dragon_Tokens.DragonToken(), 1
    )
    expected = -1
    header_pass = formatter.process_header()
    actual = ""
    if header_pass == 0:
        actual = formatter.process_file()
    assert expected == actual


def test_given_a_file_without_an_eof_block_sync_return_an_error():
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
        6,
        0,
        0,
        0,
        0x0A,
        0x92,
        0,
        0,
        formats.Cas_Format.LEADER,
        formats.Cas_Format.LEADER,
        formats.Cas_Format.END_OF_FILE_BLOCK]
    formatter = formats.Cas_Format.CasFormat(
        stream, Dragon_Tokens.DragonToken(), 1
    )
    expected = -1
    header_pass = formatter.process_header()
    actual = ""
    if header_pass == 0:
        actual = formatter.process_file()
    assert expected == actual


def test_given_a_valid_multi_block_byte_array_returns_a_formatted_string():
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
    formatter = formats.Cas_Format.CasFormat(
        stream, Dragon_Tokens.DragonToken(), 1
    )
    expected = "10 STOP\n"
    header_pass = formatter.process_header()
    actual = ""
    if header_pass == 0:
        actual = formatter.process_file()
    assert expected == actual


def test_given_a_truncated_file_returns_an_error_and_halts():
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
        6,
        0,
        0,
        0,
        0x0A]
    formatter = formats.Cas_Format.CasFormat(
        stream, Dragon_Tokens.DragonToken(), 1
    )
    header_pass = formatter.process_header()
    if header_pass == 0:
        with pytest.raises(SystemExit) as pytest_wrapped_exception:
            formatter.process_file()
    assert pytest_wrapped_exception.type == SystemExit
    assert pytest_wrapped_exception.value.code == -1


def test_given_a_byte_array_without_a_name_block_returns_an_error():
    stream = [formats.Cas_Format.LEADER, formats.Cas_Format.SYNC,
              formats.Cas_Format.END_OF_FILE_BLOCK]
    formatter = formats.Cas_Format.CasFormat(
        stream, Dragon_Tokens.DragonToken(), 1
    )
    expected = -1
    actual = formatter.process_header()
    assert expected == actual


def test_given_a_byte_array_without_a_basic_id_block_returns_an_error():
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
        formats.Cas_Format.DATA_FILE_IDENTIFIER]
    formatter = formats.Cas_Format.CasFormat(
        stream, Dragon_Tokens.DragonToken(), 1
    )
    expected = -1
    actual = formatter.process_header()
    assert expected == actual


def test_given_byte_array_without_a_valid_format_flag_block_returns_error():
    stream = [formats.Cas_Format.LEADER, formats.Cas_Format.SYNC,
              formats.Cas_Format.NAME_FILE_BLOCK, 0, 0x41, 0x20, 0x20,
              0x20, 0x20, 0x20, 0x20, 0x20,
              formats.Cas_Format.BASIC_FILE_IDENTIFIER, 0x01]
    formatter = formats.Cas_Format.CasFormat(
        stream, Dragon_Tokens.DragonToken(), 1
    )
    expected = -1
    actual = formatter.process_header()
    assert expected == actual


def test_given_byte_array_without_continuous_file_flag_block_returns_error():
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
        0x01]
    formatter = formats.Cas_Format.CasFormat(
        stream, Dragon_Tokens.DragonToken(), 1
    )
    expected = -1
    actual = formatter.process_header()
    assert expected == actual


def test_given_byte_array_with_one_leader_between_data_blocks_returns_error():
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
    formatter = formats.Cas_Format.CasFormat(
        stream, Dragon_Tokens.DragonToken(), 1
    )
    expected = -1
    actual = 0
    header_pass = formatter.process_header()
    if header_pass == 0:
        actual = formatter.process_file()
    assert expected == actual


def test_given_byte_array_with_no_leaders_between_data_blocks_returns_error():
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
    formatter = formats.Cas_Format.CasFormat(
        stream, Dragon_Tokens.DragonToken(), 1
    )
    expected = -1
    actual = 0
    header_pass = formatter.process_header()
    if header_pass == 0:
        actual = formatter.process_file()
    assert expected == actual


def test_given_a_byte_array_without_an_end_of_file_block_returns_an_error():
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
        6,
        0,
        0,
        0,
        0x0A,
        0x92,
        0,
        0,
        formats.Cas_Format.LEADER,
        formats.Cas_Format.LEADER,
        formats.Cas_Format.SYNC,
        formats.Cas_Format.NAME_FILE_BLOCK]
    formatter = formats.Cas_Format.CasFormat(
        stream, Dragon_Tokens.DragonToken(), 1
    )
    expected = -1
    actual = 0
    header_pass = formatter.process_header()
    if header_pass == 0:
        actual = formatter.process_file()
    assert expected == actual


def test_build_header_takes_filename_to_return_basic_cas_stream():
    filename = "SAMPLE"
    formatter = formats.Cas_Format.CasFormat(
        [], Dragon_Tokens.DragonToken(), 1
    )
    actual = formatter.build_header(filename)
    assert isinstance(actual, list)
    assert len(actual) > 0
    formatter.data = actual
    header_pass = formatter.process_header()
    assert formatter.file_name == filename
    assert header_pass == 0


# integration test for file builder
def test_build_file_takes_filename_and_data_to_return_cas_stream():
    filename = "SAMPLE"
    formatter = formats.Cas_Format.CasFormat(
        [], Dragon_Tokens.DragonToken(), 1
    )
    expected = "10 STOP\n"
    data = [0, 0, 0, 0x0A, 0x92, 0]
    actual = formatter.build_file(filename, data)
    assert isinstance(actual, bytearray)
    assert len(actual) == 292
    formatter.data = actual
    header_pass = formatter.process_header()
    assert formatter.file_name == filename
    assert header_pass == 0
    rebuild = formatter.process_file()
    assert expected == rebuild
