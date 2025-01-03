import pytest
from unittest.mock import patch
from app.routes import app
from unittest.mock import MagicMock, Mock



@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client


# --- Test Index Route ---
def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'<title>' in response.data  # Ensure the page has a title tag
    assert b'bot' in response.data  # Ensure there's a reference to the bot interface



# --- Test Extract Route ---
@patch('app.routes.get_all_links')
@patch('app.routes.fetch_company_data')
@patch('app.routes.clean_data')
@patch('app.routes.store_data_in_qdrant')
def test_extract_success(mock_store, mock_clean, mock_fetch, mock_get_links, client):
    mock_get_links.return_value = ['http://example.com/page1']
    mock_fetch.return_value = {'title': 'Test Title', 'content': 'Test Content', 'url': 'http://example.com/page1'}
    mock_clean.return_value.to_dict.return_value = [{'title': 'Test Title', 'content': 'Test Content'}]

    response = client.post('/extract', json={'url': 'http://example.com'})
    assert response.status_code == 200
    assert response.get_json() == {'message': 'Data extracted and stored successfully'}


@patch('app.routes.get_all_links')
def test_extract_missing_url(mock_get_links, client):
    response = client.post('/extract', json={})
    assert response.status_code == 400
    assert response.get_json() == {'error': 'No URL provided'}


# --- Test Query Route ---
@patch('app.routes.retrieve_data_from_qdrant')
@patch('app.routes.filter_similar_content')
@patch('app.routes.summarize_content')
@patch('app.routes.client.chat.completions.create')
def test_query_data(mock_openai, mock_summarize, mock_filter, mock_retrieve, client):
    mock_retrieve.return_value = [{'content': 'Test content'}]
    mock_filter.return_value = ['Test content']
    mock_summarize.return_value = 'Summarized content'
    mock_openai.return_value.choices = [
        Mock(message=Mock(content='AI Response'))
    ]

    response = client.post('/data/query', json={'query': 'Test Query'})
    print("Response Status Code:", response.status_code)
    print("Response JSON:", response.get_json())
    assert response.status_code == 200
    assert response.get_json() == {'response': 'AI Response'}



@patch('app.routes.retrieve_data_from_qdrant')
def test_query_data_missing_query(mock_retrieve, client):
    response = client.post('/data/query', json={})
    assert response.status_code == 400
    assert response.get_json() == {'error': 'No query provided'}


# --- Test Retrieve Route ---
@patch('app.routes.retrieve_data_from_qdrant')
def test_retrieve_data(mock_retrieve, client):
    mock_retrieve.return_value = [{'content': 'Test data'}]

    response = client.post('/retrieve', json={'query': 'Test Query'})
    assert response.status_code == 200
    assert response.get_json() == [{'content': 'Test data'}]


@patch('app.routes.retrieve_data_from_qdrant')
def test_retrieve_data_missing_query(mock_retrieve, client):
    response = client.post('/retrieve', json={})
    assert response.status_code == 400
    assert response.get_json() == {'error': 'No query provided'}


if __name__ == '__main__':
    pytest.main()
