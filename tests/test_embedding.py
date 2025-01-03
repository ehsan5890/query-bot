import pytest
from unittest.mock import patch, Mock
from app.embedding import get_embedding, store_data_in_qdrant

# --- Tests for get_embedding ---
@patch('app.embedding.openai.embeddings.create')
def test_get_embedding(mock_openai):
    mock_response = Mock()
    mock_response.data = [Mock(embedding=[0.1, 0.2, 0.3])]
    mock_openai.return_value = mock_response

    result = get_embedding('test text')
    assert result == [0.1, 0.2, 0.3]

# --- Tests for store_data_in_qdrant ---
@patch('app.embedding.QdrantClient')
@patch('app.embedding.get_embedding')
@patch('app.embedding.process_large_text')
def test_store_data_in_qdrant(mock_process_large_text, mock_get_embedding, mock_qdrant_client):
    mock_client_instance = mock_qdrant_client.return_value
    mock_client_instance.collection_exists.return_value = False
    mock_client_instance.search.return_value = [Mock(score=0.8)]

    mock_get_embedding.return_value = [0.1, 0.2, 0.3]
    mock_process_large_text.return_value = ('processed text', 5000)

    sample_data = [{'content': 'Sample content', 'url': 'http://example.com'}]
    store_data_in_qdrant(sample_data, similarity_threshold=0.99, collection_name='test_collection')

    mock_client_instance.create_collection.assert_called_once()
    mock_client_instance.upsert.assert_called_once()

# Test duplicate handling
@patch('app.embedding.QdrantClient')
@patch('app.embedding.get_embedding')
@patch('app.embedding.process_large_text')
def test_store_data_in_qdrant_duplicate(mock_process_large_text, mock_get_embedding, mock_qdrant_client):
    mock_client_instance = mock_qdrant_client.return_value
    mock_client_instance.collection_exists.return_value = True
    mock_client_instance.search.return_value = [Mock(score=0.99)]

    mock_get_embedding.return_value = [0.1, 0.2, 0.3]
    mock_process_large_text.return_value = ('processed text', 5000)

    sample_data = [{'content': 'Sample content', 'url': 'http://example.com'}]
    store_data_in_qdrant(sample_data, similarity_threshold=0.99, collection_name='test_collection')

    mock_client_instance.upsert.assert_not_called()

if __name__ == '__main__':
    pytest.main()
