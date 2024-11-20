import requests
from bs4 import BeautifulSoup
import pandas as pd
import uuid
from typing import List, Dict, Optional
from qdrant_client import QdrantClient
import openai


def fetch_company_data(url: str) -> Optional[Dict[str, str]]:
    """
    Fetches company data from a given URL.

    Args:
        url (str): The URL of the company's webpage.

    Returns:
        Optional[Dict[str, str]]: A dictionary containing the title, main heading, and URL, or None if the request fails.
    """
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.find('title').get_text() if soup.find('title') else "No title found"
        main_heading = soup.find('h1').get_text() if soup.find('h1') else "No main heading found"
        return {"title": title, "main_heading": main_heading, "url": url}
    else:
        print(f"Failed to retrieve data from {url}")
        return None


def clean_data(data_list: List[Dict[str, str]]) -> pd.DataFrame:
    """
    Cleans the given list of company data dictionaries.

    Args:
        data_list (List[Dict[str, str]]): A list of dictionaries containing company data.

    Returns:
        pd.DataFrame: A cleaned DataFrame containing the company data.
    """
    df = pd.DataFrame(data_list)
    df.dropna(inplace=True)
    df['title'] = df['title'].str.strip().str.lower()
    return df


def get_embedding(text: str) -> List[float]:
    """
    Generates an embedding for the given text using OpenAI's embedding model.

    Args:
        text (str): The text to generate an embedding for.

    Returns:
        List[float]: A list representing the embedding vector.
    """
    response = openai.embeddings.create(
        model="text-embedding-ada-002",
        input=text
    )
    return response.data[0].embedding



def store_data_in_qdrant(data: List[Dict[str, str]]) -> None:
    """
    Stores the given data in Qdrant as vectors.

    Args:
        data (List[Dict[str, str]]): A list of dictionaries containing company data.
    """
    client = QdrantClient(host="localhost", port=6333)
    collection_name: str = "company_data"

    # Check if the collection exists, and create it if it doesn't
    if not client.collection_exists(collection_name=collection_name):
        client.create_collection(
            collection_name=collection_name,
            vectors_config={
                "size": len(get_embedding("test")),  # assuming the length of embedding from OpenAI model
                "distance": "Cosine"  # or "Euclidean" depending on your use case
            }
        )

    # Prepare points to upsert
    points: List[Dict] = []
    for item in data:
        vector = get_embedding(item['title'])
        point_id: str = str(uuid.uuid4())  # Generate a new UUID for the point ID
        points.append({
            "id": point_id,
            "vector": vector,
            "payload": item
        })

    # Upsert the points in Qdrant
    client.upsert(
        collection_name=collection_name,
        points=points
    )


# # Example usage
# def main():
#     urls = ["https://modulai.io/"]
#     data_list = [fetch_company_data(url) for url in urls if fetch_company_data(url) is not None]
#     if data_list:
#         cleaned_data = clean_data(data_list)
#         store_data_in_qdrant(cleaned_data.to_dict(orient='records'))
#
#
# if __name__ == "__main__":
#     main()
