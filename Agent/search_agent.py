from googleapiclient.discovery import build
from dotenv import load_dotenv
import os 


load_dotenv()
cse_id = os.getenv('CSE_ID')
api_key = os.getenv('API_KEY')

class SearchAgent:
    def __init__(self, api_key, cse_id):
        self.api_key = api_key
        self.cse_id = cse_id

    def search(self, topic):
        service = build("customsearch", "v1", developerKey=self.api_key)
        res = service.cse().list(q=topic, cx=self.cse_id).execute()
        if 'items' in res:
            urls = [item['link'] for item in res['items']]
            return urls
        else:
            print("No search results found.")
            return []