import Dragon_Tokens
from Cas_Format import CasFormat, LEADER, SYNC, NAME_FILE_BLOCK, BASIC_FILE_IDENTIFIER, ASCII_FILE_FLAG, \
    CONTINUOUS_FILE, DATA_BLOCK, END_OF_FILE_BLOCK


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
