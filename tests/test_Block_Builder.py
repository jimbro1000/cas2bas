import pytest

from formats.Block_Builder import FileBlock
from formats.Cas_Format import NAME_FILE_BLOCK, DATA_BLOCK, \
    BASIC_FILE_IDENTIFIER, BINARY_FILE_FLAG, CONTINUOUS_FILE


def test_file_block_creates_a_new_minimal_cas_block_byte_array():
    block = FileBlock(NAME_FILE_BLOCK)
    expected = [0x3c, 0x00, 0x00, 0x00]
    actual = block.seal_block()
    assert actual == expected


def test_block_append_adds_a_byte_to_the_block():
    block = FileBlock(DATA_BLOCK)
    expected = [0x3c, 0x01, 0x01, 0x01, 0x02]
    block.append(0x01)
    actual = block.seal_block()
    assert actual == expected


def test_block_capacity_returns_the_byte_capacity_left_in_the_block():
    block = FileBlock(DATA_BLOCK)
    expected = 253
    block.append(0x01)
    block.append(0x02)
    actual = block.capacity()
    assert actual == expected


def test_block_append_raises_exception_if_capacity_exceeded():
    block = FileBlock(DATA_BLOCK)
    for x in range(255):
        block.append(x)
    with pytest.raises(ValueError):
        block.append(1)


@pytest.mark.parametrize("test_input", ['a', -1, 256, 3.5])
def test_block_append_raises_exception_if_non_byte_value_supplied(test_input):
    block = FileBlock(DATA_BLOCK)
    with pytest.raises(ValueError):
        block.append(test_input)


def test_block_seal_closes_the_block_with_a_checksum():
    block = FileBlock(NAME_FILE_BLOCK)
    expected = [0x3c, 0x00, 0x0f, 0x54, 0x45, 0x45, 0x44, 0x20, 0x31, 0x2e,
                0x34, 0x00, 0x00, 0x00, 0x00, 0x00, 0x7c, 0xaf, 0x0f]
    filename = list("TEED 1.4")
    for x in range(8):
        block.append(ord(filename[x]))
    block.append(BASIC_FILE_IDENTIFIER)
    block.append(BINARY_FILE_FLAG)
    block.append(CONTINUOUS_FILE)
    block.append(0)
    block.append(0)
    block.append(0x7c)
    block.append(0xaf)
    actual = block.seal_block()
    assert actual == expected
