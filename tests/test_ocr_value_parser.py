from app.ocr.value_parser import OCRValueParser


def test_parse_regular_integer():
    assert OCRValueParser.parse("123") == 123.0


def test_parse_decimal_dot():
    assert OCRValueParser.parse("123.45") == 123.45


def test_parse_decimal_comma():
    assert OCRValueParser.parse("123,45") == 123.45


def test_parse_negative_value():
    assert OCRValueParser.parse("-12.5") == -12.5


def test_parse_time_like_value():
    assert OCRValueParser.parse("00:54,71") == 54.71


def test_parse_time_like_value_with_minutes():
    assert OCRValueParser.parse("01:14,74") == 74.74


def test_parse_empty_text():
    assert OCRValueParser.parse("") is None


def test_parse_invalid_text():
    assert OCRValueParser.parse("abc") is None