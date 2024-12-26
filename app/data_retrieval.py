from qdrant_client import QdrantClient
from typing import List, Dict
from app.embedding import get_embedding
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from typing import List
from qdrant_client import QdrantClient
from app.embedding import get_embedding
from typing import List, Dict

def retrieve_data_from_qdrant(query: str, top_k: int = 25, min_score: float = 0.5) -> List[Dict]:
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
    collection_name = "company_data_v3"
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





def remove_internal_duplicates(content_list: List[str]) -> List[str]:
    """
    Removes duplicate sentences within each string in a list.

    Args:
        content_list (List[str]): List of content strings with possible duplicates.

    Returns:
        List[str]: List of cleaned content strings with duplicates removed.
    """
    cleaned_list = []

    for content in content_list:
        # Split the content into sentences using newline and period delimiters
        sentences = content.split(".")  # Adjust if you have other delimiters like "\n"
        unique_sentences = list(dict.fromkeys(sentence.strip() for sentence in sentences if sentence.strip()))
        # Rejoin unique sentences into a single cleaned string
        cleaned_content = ". ".join(unique_sentences).strip()
        cleaned_list.append(cleaned_content)

    return cleaned_list


def filter_similar_content(data: List[str], threshold: float = 0.8) -> List[str]:
    """
    Filters similar content based on cosine similarity of text.

    Args:
        data (List[str]): List of content strings.
        threshold (float): Similarity threshold for deduplication.

    Returns:
        List[str]: Filtered content list.
    """
    vectorizer = TfidfVectorizer().fit_transform(data)
    vectors = vectorizer.toarray()
    similarity_matrix = cosine_similarity(vectors)

    filtered = []
    for i, content in enumerate(data):
        if all(similarity_matrix[i][j] < threshold for j in range(i)):
            filtered.append(content)

    return remove_internal_duplicates(filtered)


def summarize_content(content_list: List[str], max_length: int = 50000) -> str:
    """
    Summarizes content to fit within a specified length.

    Args:
        content_list (List[str]): List of content strings.
        max_length (int): Maximum character length of the summary.

    Returns:
        str: Summarized content.
    """
    combined = " ".join(content_list)
    return combined[:max_length] + "..." if len(combined) > max_length else combined

# Example usage
if __name__ == "__main__":
    all_data = retrieve_all_data_from_qdrant("company_data_v3")
    for data in all_data:
        print(data)

