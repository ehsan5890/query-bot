from app.data_extraction import fetch_company_data, clean_data, get_all_links
data_list = []
url = "https://modulai.io/"
links = get_all_links(url)
for link in links:
    data = fetch_company_data(link)
    data_list.append(data)
if data_list:
    print(data_list)
    processed_data = clean_data(data_list[0])
    print("Extracted Data:")
    print(processed_data)
else:
    print("Data extraction failed.")


from qdrant_client import QdrantClient
from typing import List

def search_keyword_in_qdrant(keyword: str, collection_name: str = "company_data_v3", top_k: int = 10) -> List[dict]:
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

    results = search_keyword_in_qdrant("Peter Grimvall")
    for result in results:
        print(result)
