from formats.Utility import invert_dictionary


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
