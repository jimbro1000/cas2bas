from formats.Utility import invert_dictionary


def test_given_an_empty_dictionary_invert_dictionary_returns_an_empty_dictionary():
    source = {}
    expected = {}
    actual = invert_dictionary(source)
    assert actual == expected


def test_given_a_dictionary_invert_dictionary_returns_a_matching_dictionary_of_value_key_pairs():
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
