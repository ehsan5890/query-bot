import pytest
from unittest.mock import patch, Mock
from app.data_retrieval import (
    retrieve_data_from_qdrant,
    retrieve_all_data_from_qdrant,
    remove_internal_duplicates,
    filter_similar_content,
    summarize_content
)

# --- Tests for retrieve_data_from_qdrant ---
@patch('app.data_retrieval.QdrantClient')
def test_retrieve_data_from_qdrant(mock_client):
    mock_instance = mock_client.return_value
    mock_instance.search.return_value = [
        Mock(payload={'data': 'result1'}, score=0.9),
        Mock(payload={'data': 'result2'}, score=0.4)
    ]

    results = retrieve_data_from_qdrant('test query', 'test_collection', 2, 0.5)
    assert len(results) == 1
    assert results[0]['data'] == 'result1'

# --- Tests for retrieve_all_data_from_qdrant ---
@patch('app.data_retrieval.QdrantClient')
def test_retrieve_all_data_from_qdrant(mock_client):
    mock_instance = mock_client.return_value
    mock_instance.scroll.side_effect = [
        ([Mock(payload={'data': 'result1'})], 'offset1'),
        ([Mock(payload={'data': 'result2'})], None)
    ]

    results = retrieve_all_data_from_qdrant('test_collection', 2)
    assert len(results) == 2
    assert results[0]['data'] == 'result1'
    assert results[1]['data'] == 'result2'

# --- Tests for remove_internal_duplicates ---
def test_remove_internal_duplicates():
    input_data = [
        "This is a sentence. This is a sentence. Another sentence."
    ]
    result = remove_internal_duplicates(input_data)
    assert result == ["This is a sentence. Another sentence"]

# --- Tests for filter_similar_content ---
def test_filter_similar_content():
    input_data = [
        "This is unique content.",
        "This is unique content.",
        "Another different content."
    ]
    result = filter_similar_content(input_data, threshold=0.8)
    assert len(result) == 2
    assert "This is unique content" in result
    assert "Another different content" in result

# --- Tests for summarize_content ---
def test_summarize_content():
    input_data = ["This is a long content."] * 100
    result = summarize_content(input_data, max_length=50)
    assert len(result) <= 53  # Including "..."
    assert result.endswith('...')

if __name__ == '__main__':
    test_remove_internal_duplicates()
    pytest.main()
