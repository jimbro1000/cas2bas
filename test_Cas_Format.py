import pytest

import Dragon_Tokens
from Cas_Format import CasFormat, LEADER, SYNC, NAME_FILE_BLOCK, BASIC_FILE_IDENTIFIER, ASCII_FILE_FLAG, \
    CONTINUOUS_FILE, DATA_BLOCK, END_OF_FILE_BLOCK, DATA_FILE_IDENTIFIER


def test_given_a_valid_byte_array_returns_a_formatted_string():
    stream = [LEADER, SYNC, NAME_FILE_BLOCK, 0, 0x41, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, BASIC_FILE_IDENTIFIER,
              ASCII_FILE_FLAG, CONTINUOUS_FILE, 0, 0, 0, 0, 0, LEADER, LEADER, SYNC, DATA_BLOCK, 6, 0, 0, 0, 0x0A, 0x92,
              0, 0, LEADER, LEADER, SYNC, END_OF_FILE_BLOCK]
    formatter = CasFormat(stream, Dragon_Tokens.DragonToken())
    expected = "10 STOP" + chr(10) + chr(13)
    header_pass = formatter.process_header()
    actual = ""
    if header_pass == 0:
        actual = formatter.process_file()
    assert expected == actual


def test_given_a_file_without_a_sync_in_the_header_return_an_error():
    stream = [LEADER, NAME_FILE_BLOCK, 0]
    formatter = CasFormat(stream, Dragon_Tokens.DragonToken())
    expected = -1
    actual = formatter.process_header()
    assert expected == actual


def test_given_a_file_without_a_data_block_sync_return_an_error():
    stream = [LEADER, SYNC, NAME_FILE_BLOCK, 0, 0x41, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, BASIC_FILE_IDENTIFIER,
              ASCII_FILE_FLAG, CONTINUOUS_FILE, 0, 0, 0, 0, 0, LEADER, LEADER, DATA_BLOCK]
    formatter = CasFormat(stream, Dragon_Tokens.DragonToken())
    expected = -1
    header_pass = formatter.process_header()
    actual = ""
    if header_pass == 0:
        actual = formatter.process_file()
    assert expected == actual


def test_given_a_file_without_an_eof_block_sync_return_an_error():
    stream = [LEADER, SYNC, NAME_FILE_BLOCK, 0, 0x41, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, BASIC_FILE_IDENTIFIER,
              ASCII_FILE_FLAG, CONTINUOUS_FILE, 0, 0, 0, 0, 0, LEADER, LEADER, SYNC, DATA_BLOCK, 6, 0, 0, 0, 0x0A, 0x92,
              0, 0, LEADER, LEADER, END_OF_FILE_BLOCK]
    formatter = CasFormat(stream, Dragon_Tokens.DragonToken())
    expected = -1
    header_pass = formatter.process_header()
    actual = ""
    if header_pass == 0:
        actual = formatter.process_file()
    assert expected == actual


def test_given_a_valid_multi_block_byte_array_returns_a_formatted_string():
    stream = [LEADER, SYNC, NAME_FILE_BLOCK, 0, 0x41, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, BASIC_FILE_IDENTIFIER,
              ASCII_FILE_FLAG, CONTINUOUS_FILE, 0, 0, 0, 0, 0, LEADER, LEADER, SYNC, DATA_BLOCK, 3, 0, 0, 0, 0, LEADER,
              LEADER, SYNC, DATA_BLOCK, 3, 0x0A, 0x92, 0, 0, LEADER, LEADER, SYNC, END_OF_FILE_BLOCK]
    formatter = CasFormat(stream, Dragon_Tokens.DragonToken())
    expected = "10 STOP" + chr(10) + chr(13)
    header_pass = formatter.process_header()
    actual = ""
    if header_pass == 0:
        actual = formatter.process_file()
    assert expected == actual


def test_given_a_truncated_file_returns_an_error_and_halts():
    stream = [LEADER, SYNC, NAME_FILE_BLOCK, 0, 0x41, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, BASIC_FILE_IDENTIFIER,
              ASCII_FILE_FLAG, CONTINUOUS_FILE, 0, 0, 0, 0, 0, LEADER, LEADER, SYNC, DATA_BLOCK, 6, 0, 0, 0, 0x0A]
    formatter = CasFormat(stream, Dragon_Tokens.DragonToken())
    header_pass = formatter.process_header()
    if header_pass == 0:
        with pytest.raises(SystemExit) as pytest_wrapped_exception:
            formatter.process_file()
    assert pytest_wrapped_exception.type == SystemExit
    assert pytest_wrapped_exception.value.code == -1


def test_given_a_byte_array_without_a_name_block_returns_an_error():
    stream = [LEADER, SYNC, END_OF_FILE_BLOCK]
    formatter = CasFormat(stream, Dragon_Tokens.DragonToken())
    expected = -1
    actual = formatter.process_header()
    assert expected == actual


def test_given_a_byte_array_without_a_basic_id_block_returns_an_error():
    stream = [LEADER, SYNC, NAME_FILE_BLOCK, 0, 0x41, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, DATA_FILE_IDENTIFIER]
    formatter = CasFormat(stream, Dragon_Tokens.DragonToken())
    expected = -1
    actual = formatter.process_header()
    assert expected == actual


def test_given_a_byte_array_without_a_valid_format_flag_block_returns_an_error():
    stream = [LEADER, SYNC, NAME_FILE_BLOCK, 0, 0x41, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, BASIC_FILE_IDENTIFIER,
              0x01]
    formatter = CasFormat(stream, Dragon_Tokens.DragonToken())
    expected = -1
    actual = formatter.process_header()
    assert expected == actual


def test_given_a_byte_array_without_a_continuous_file_flag_block_returns_an_error():
    stream = [LEADER, SYNC, NAME_FILE_BLOCK, 0, 0x41, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, BASIC_FILE_IDENTIFIER,
              ASCII_FILE_FLAG, 0x01]
    formatter = CasFormat(stream, Dragon_Tokens.DragonToken())
    expected = -1
    actual = formatter.process_header()
    assert expected == actual


def test_given_a_byte_array_with_one_leader_between_data_blocks_returns_an_error():
    stream = [LEADER, SYNC, NAME_FILE_BLOCK, 0, 0x41, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, BASIC_FILE_IDENTIFIER,
              ASCII_FILE_FLAG, CONTINUOUS_FILE, 0, 0, 0, 0, 0, LEADER, LEADER, SYNC, DATA_BLOCK, 3, 0, 0, 0, 0, LEADER,
              SYNC, DATA_BLOCK, 3, 0x0A, 0x92, 0, 0, LEADER, LEADER, SYNC, END_OF_FILE_BLOCK]
    formatter = CasFormat(stream, Dragon_Tokens.DragonToken())
    expected = -1
    actual = 0
    header_pass = formatter.process_header()
    if header_pass == 0:
        actual = formatter.process_file()
    assert expected == actual


def test_given_a_byte_array_with_no_leaders_between_data_blocks_returns_an_error():
    stream = [LEADER, SYNC, NAME_FILE_BLOCK, 0, 0x41, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, BASIC_FILE_IDENTIFIER,
              ASCII_FILE_FLAG, CONTINUOUS_FILE, 0, 0, 0, 0, 0, LEADER, LEADER, SYNC, DATA_BLOCK, 3, 0, 0, 0, 0,
              SYNC, DATA_BLOCK, 3, 0x0A, 0x92, 0, 0, LEADER, LEADER, SYNC, END_OF_FILE_BLOCK]
    formatter = CasFormat(stream, Dragon_Tokens.DragonToken())
    expected = -1
    actual = 0
    header_pass = formatter.process_header()
    if header_pass == 0:
        actual = formatter.process_file()
    assert expected == actual


def test_given_a_byte_array_without_an_end_of_file_block_returns_an_error():
    stream = [LEADER, SYNC, NAME_FILE_BLOCK, 0, 0x41, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, BASIC_FILE_IDENTIFIER,
              ASCII_FILE_FLAG, CONTINUOUS_FILE, 0, 0, 0, 0, 0, LEADER, LEADER, SYNC, DATA_BLOCK, 6, 0, 0, 0, 0, 0x0A,
              0x92, 0, 0, LEADER, LEADER, SYNC, NAME_FILE_BLOCK]
    formatter = CasFormat(stream, Dragon_Tokens.DragonToken())
    expected = -1
    actual = 0
    header_pass = formatter.process_header()
    if header_pass == 0:
        actual = formatter.process_file()
    assert expected == actual
