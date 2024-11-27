from qdrant_client import QdrantClient
from typing import List, Dict
from app.embedding import get_embedding


from qdrant_client import QdrantClient
from embedding import get_embedding
from typing import List, Dict

def retrieve_data_from_qdrant(query: str, top_k: int = 5, min_score: float = 0.5) -> List[Dict]:
    """
    Retrieves data from Qdrant using a similarity search and filters based on score.

    Args:
        query (str): The query text to find related data.
        top_k (int): The number of most similar results to retrieve.
        min_score (float): The minimum score to filter out irrelevant results.

    Returns:
        List[Dict]: A list of data points retrieved from Qdrant.
    """
    client = QdrantClient(host="localhost", port=6333)
    collection_name = "company_data_v2"
    vector = get_embedding(query)

    # Retrieve top_k results from Qdrant
    response = client.search(
        collection_name=collection_name,
        query_vector=vector,
        limit=top_k,
        with_payload=True,
        with_vectors=False
    )

    # Filter results based on a score threshold (assuming similarity scores are provided)
    filtered_results = [point.payload for point in response if point.score >= min_score]

    return filtered_results


# Example usage for RAG
# query = "machine learning services"
# retrieved_data = retrieve_data_from_qdrant(query)
# print(retrieved_data)

def retrieve_all_data_from_qdrant(collection_name: str, batch_size: int = 100) -> List[Dict]:
    """
    Retrieves all data points from a Qdrant collection.

    Args:
        collection_name (str): The name of the Qdrant collection.
        batch_size (int): The number of points to retrieve per scroll request.

    Returns:
        List[Dict]: A list of all data points retrieved from the collection.
    """
    # Initialize Qdrant client
    client = QdrantClient(host="localhost", port=6333)

    # Retrieve all data points from the collection using scroll
    all_points = []
    offset = None

    while True:
        response = client.scroll(
            collection_name=collection_name,
            limit=batch_size,
            offset=offset  # Scroll through the dataset in batches
        )

        # Extract points and add to the list
        all_points.extend(response[0])  # response[0] contains the list of points

        # Check if there are more points to retrieve
        offset = response[1]
        if offset is None:
            break

    # Convert the list of points to a list of payloads
    return [point.payload for point in all_points]


# Example usage
if __name__ == "__main__":
    all_data = retrieve_all_data_from_qdrant("company_data_v2")
    for data in all_data:
        print(data)

# def retrieve_data_from_qdrant(vector: List[float], top_k: int = 5) -> None:
#     """
#     Retrieves data from Qdrant using a similarity search based on a given vector.
#
#     Args:
#         vector (List[float]): The vector to use for similarity search.
#         top_k (int): The number of most similar results to retrieve.
#
#     Returns:
#         None
#     """
#     # Initialize Qdrant client
#     client = QdrantClient(host="localhost", port=6333)
#     collection_name = "company_data"
#
#     # Perform similarity search
#     response = client.search(
#         collection_name=collection_name,
#         query_vector=vector,
#         limit=top_k  # Retrieve top_k similar items
#     )
#
#     # Process and print the retrieved points
#     if response:
#         for point in response:
#             print(f"ID: {point.id}, Payload: {point.payload}, Score: {point.score}")

# Example usage
# if __name__ == "__main__":
#     from data_extraction import get_embedding
#
#     text_to_search = "modulai"
#     vector = get_embedding(text_to_search)
#     retrieve_data_from_qdrant(vector=vector, top_k=3)
