import requests
from bs4 import BeautifulSoup
import pandas as pd
import uuid
from typing import List, Dict, Optional
from qdrant_client import QdrantClient
from urllib.parse import urljoin
import openai


def get_all_links(base_url: str) -> List[str]:
    """
    Get all internal links from the base URL.

    Args:
        base_url (str): The starting URL to find all pages.

    Returns:
        List[str]: A list of all discovered URLs within the base domain.
    """
    visited = set()
    to_visit = [base_url]
    all_links = []

    while to_visit:
        url = to_visit.pop(0)
        if url in visited:
            continue

        visited.add(url)
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            for link in soup.find_all('a', href=True):
                full_url = urljoin(base_url, link['href'])

                # Filtering out unwanted links
                if (base_url in full_url and
                        full_url not in visited and
                        not any(keyword in full_url for keyword in
                                ['login', 'user-agreement', 'cookie-policy', 'help', 'legal'])):
                    to_visit.append(full_url)
                    all_links.append(full_url)

    return all_links


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


