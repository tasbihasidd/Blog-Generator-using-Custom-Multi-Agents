import requests
from bs4 import BeautifulSoup

class ContentFetcherAgent:
    @staticmethod
    def fetch_content(url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            return soup.get_text()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return ""