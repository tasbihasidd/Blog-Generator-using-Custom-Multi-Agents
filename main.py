import openai
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from googleapiclient.discovery import build
import os

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')
cse_id = os.getenv('CSE_ID')
api_key = os.get('API_KEY')


def search_topic(api_key, cse_id, topic):
        service = build("customsearch", "v1", developerKey=api_key)
        res = service.cse().list(q=topic, cx=cse_id).execute()
        if 'items' in res:
            urls = [item['link'] for item in res['items']]
            return urls
        else:
            print("No search results found.")
            return []
        

def fetch_web_content(url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            return soup.get_text()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return ""
        

def generate_blog(api_key, cse_id, topic):
    # Step 1: Search for URLs based on the topic
    final_urls = search_topic(api_key, cse_id, topic)
    # print(type(final_urls), len(final_urls), "urls===========>", final_urls)
    
    summaries = []
    
    # Step 2: Summarize content from each URL
    for url in final_urls:
        print("url=====>", url)
        
        # Fetch content from the URL
        content = fetch_web_content(url)
        truncated_content = content[:5000]  # Truncate to avoid too long inputs
        
        # Step 3: Use OpenAI to generate summary
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": f"Summarize the following content: {truncated_content}"}],
            max_tokens=150
        )
        
        # Extract the summary from OpenAI response
        summary = response.choices[0].message['content'].strip()
        
        # Append the summary with the URL to the list
        summaries.append({'url': url, 'summary': summary})
        
        # If you only want to summarize the first URL, you can break here
        break
    
    return summaries

topic = input("Enter topic: ")
# Call the function to generate blog
blog_summaries = generate_blog(api_key, cse_id, topic)

# Print the result
for blog in blog_summaries:
    print(f"URL: {blog['url']}")
    print(f"Summary: {blog['summary']}")
    print("=" * 50)






