import uuid
from typing import List, Dict
from qdrant_client import QdrantClient
import openai


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
