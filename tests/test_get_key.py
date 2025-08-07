import re
import pytest
from src.logparser import get_key


@pytest.fixture
def get_key_test_data():
    input_string = "/api/homeworks/..."
    result = get_key(input_string)
    return input_string, result


def test_get_key_contains_only_hex_chars_v2(get_key_test_data):
    _, result = get_key_test_data
    assert re.match(r'^[0-9a-f]*$', result.lower())


def test_get_key_result_has_correct_length_v2(get_key_test_data):
    input_string, result = get_key_test_data
    assert len(result) == len(input_string) * 2


def test_string_to_hex_empty_string():
    input_string = ""
    result = get_key(input_string)
    assert result == ""