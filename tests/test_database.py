from qdrant_client import QdrantClient
from typing import List

def search_keyword_in_qdrant(keyword: str, collection_name: str = "company_data", top_k: int = 10) -> List[dict]:
    """
    Searches the Qdrant collection for records that contain the specified keyword in their payload.

    Args:
        keyword (str): The keyword to search for.
        collection_name (str): The name of the collection to search in.
        top_k (int): The number of most similar results to retrieve.

    Returns:
        List[dict]: A list of payloads that match the keyword.
    """
    client = QdrantClient(host="localhost", port=6333)

    # Scroll through all points in the collection
    all_points = client.scroll(
        collection_name=collection_name,
        limit=1000,  # Adjust depending on how many records you have
        with_payload=True
    )

    # Manually filter for the keyword in the payload
    matching_points = []
    for points in all_points:
        for point in points:
            if 'content' in point.payload and keyword.lower() in point.payload['content'].lower():
                matching_points.append(point.payload)

        # Stop if we reach the required number of results
            if len(matching_points) >= top_k:
                break
        break
    return matching_points

# Example usage
if __name__ == "__main__":

    results = search_keyword_in_qdrant("machine learning")
    for result in results:
        print(result)
