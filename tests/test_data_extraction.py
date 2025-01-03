

import pytest
import requests
from unittest.mock import patch, Mock
import pandas as pd
from app.data_extraction import get_all_links, fetch_company_data, clean_data, get_collection_name

# Mock data for testing
MOCK_HTML = """
<html>
    <head><title>Test Page</title></head>
    <body>
        <a href="/link1">Link 1</a>
        <a href="/link2">Link 2</a>
        <a href="/login">Login</a>
        <h1>Main Heading</h1>
        <p>Sample paragraph.</p>
    </body>
</html>
"""

# --- Tests for get_all_links ---
@patch('app.data_extraction.requests.get')
def test_get_all_links(mock_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.content = MOCK_HTML.encode('utf-8')
    mock_get.return_value = mock_response

    base_url = 'http://example.com'
    expected_links = ['http://example.com/link1', 'http://example.com/link2']

    result = get_all_links(base_url)
    assert set(result) == set(expected_links)

# --- Tests for fetch_company_data ---
@patch('app.data_extraction.requests.get')
def test_fetch_company_data_success(mock_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.content = MOCK_HTML.encode('utf-8')
    mock_get.return_value = mock_response

    url = 'http://example.com/page'
    result = fetch_company_data(url)
    assert result is not None
    assert result['title'] == 'Test Page'
    assert 'Main Heading' in result['content']
    assert 'Sample paragraph.' in result['content']

@patch('app.data_extraction.requests.get')
def test_fetch_company_data_failure(mock_get):
    mock_response = Mock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response

    url = 'http://example.com/page'
    result = fetch_company_data(url)
    assert result is None

# --- Tests for clean_data ---
def test_clean_data():
    sample_data = [
        {'title': ' Title One ', 'content': 'Content 1'},
        {'title': None, 'content': 'Content 2'},
        {'title': 'Title Two', 'content': None},
    ]
    df = clean_data(sample_data)
    assert len(df) == 1
    assert df.iloc[0]['title'] == 'title one'

# --- Tests for get_collection_name ---
def test_get_collection_name():
    url = 'http://example.com/page'
    result = get_collection_name(url)
    assert result == 'collection_example_com'

if __name__ == '__main__':
    pytest.main()
