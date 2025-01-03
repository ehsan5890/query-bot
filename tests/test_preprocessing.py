import pytest
from unittest.mock import patch, Mock
from app.preprocessing import (
    fix_encoding,
    replace_unknown_chars,
    clean_text,
    preprocess_text,
    count_tokens,
    process_large_text
)

# --- Tests for fix_encoding ---
def test_fix_encoding():
    text = 'Caf\xe9'
    result = fix_encoding(text)
    assert result == 'Café'

    invalid_text = '\udce2\udce3'
    result = fix_encoding(invalid_text)
    assert any(char in result for char in ['�', '?']), "Replacement character mismatch"


# --- Tests for replace_unknown_chars ---
def test_replace_unknown_chars():
    text = 'This is a test � character'
    result = replace_unknown_chars(text)
    assert result == 'This is a test [UNK] character'

# --- Tests for clean_text ---
def test_clean_text():
    text = 'This is a valid string!\x00\x01'
    result = clean_text(text)
    assert result == 'This is a valid string!'

# --- Tests for preprocess_text ---
def test_preprocess_text():
    text = 'This is a test � string with invalid encoding \x00'
    result = preprocess_text(text)
    expected = 'This is a test  string with invalid encoding '
    assert result.strip() == expected.strip(), f"Expected: {expected}, Got: {result}"


# --- Tests for count_tokens ---
@patch('app.preprocessing.tiktoken.encoding_for_model')
def test_count_tokens(mock_encoding_for_model):
    mock_encoding = Mock()
    mock_encoding.encode.return_value = [1, 2, 3, 4]
    mock_encoding_for_model.return_value = mock_encoding

    result = count_tokens('This is a test', model='gpt-3.5-turbo')
    assert result == 4

# --- Tests for process_large_text ---
@patch('app.preprocessing.count_tokens')
def test_process_large_text(mock_count_tokens):
    mock_count_tokens.return_value = 100
    text = 'This is a sample text.'

    processed_text, token_count = process_large_text(text)
    assert processed_text == 'This is a sample text.'
    assert token_count == 100

if __name__ == '__main__':
    pytest.main()
