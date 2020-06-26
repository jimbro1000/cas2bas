import Dragon_Tokens


def test_when_a_single_byte_token_is_supplied_return_the_token_keyword():
    expected = "CLEAR"
    token_value = 0x96
    tokeniser = Dragon_Tokens.DragonToken()
    actual = tokeniser.convert(token_value)
    assert actual == expected


def test_when_a_two_byte_token_is_supplied_return_the_token_keyword():
    expected = "JOYSTK"
    token_value = 0x93
    tokeniser = Dragon_Tokens.DragonToken()
    tokeniser.convert(0xFF)
    actual = tokeniser.convert(token_value)
    assert actual == expected


def test_when_an_ascii_value_byte_is_supplied_return_the_equivalent_character():
    expected = "A"
    byte_value = 0x41
    tokeniser = Dragon_Tokens.DragonToken()
    actual = tokeniser.convert(byte_value)
    assert actual == expected


def test_when_an_illegal_single_byte_token_is_supplied_return_an_error_message():
    expected = "invalid byte token"
    token_value = 0xFE
    tokeniser = Dragon_Tokens.DragonToken()
    actual = tokeniser.convert(token_value)
    assert actual == expected


def test_when_an_illegal_double_byte_token_is_supplied_return_an_error_message():
    expected = "invalid extended token"
    token_value = 0xB0
    tokeniser = Dragon_Tokens.DragonToken()
    tokeniser.convert(0xFF)
    actual = tokeniser.convert(token_value)
    assert actual == expected
