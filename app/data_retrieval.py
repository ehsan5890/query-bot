from qdrant_client import QdrantClient
from typing import List
from dotenv import load_dotenv
import openai

# Load environment variables from .env file
load_dotenv()


def retrieve_data_from_qdrant(vector: List[float], top_k: int = 5) -> None:
    """
    Retrieves data from Qdrant using a similarity search based on a given vector.

    Args:
        vector (List[float]): The vector to use for similarity search.
        top_k (int): The number of most similar results to retrieve.

    Returns:
        None
    """
    # Initialize Qdrant client
    client = QdrantClient(host="localhost", port=6333)
    collection_name = "company_data"

    # Perform similarity search
    response = client.search(
        collection_name=collection_name,
        query_vector=vector,
        limit=top_k  # Retrieve top_k similar items
    )

    # Process and print the retrieved points
    if response:
        for point in response:
            print(f"ID: {point.id}, Payload: {point.payload}, Score: {point.score}")

# Example usage
if __name__ == "__main__":
    from data_extraction import get_embedding

    text_to_search = "modulai"
    vector = get_embedding(text_to_search)
    retrieve_data_from_qdrant(vector=vector, top_k=3)
    print(vector)
