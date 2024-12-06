
import streamlit as st
from Agent.search_agent import SearchAgent
from Agent.content_fetcher_agent import ContentFetcherAgent 
from Agent.summarize_agent import SummarizerAgent
from Agent.pdf_generator_agent import PDFGeneratorAgent
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize API keys from environment variables
google_api_key = os.getenv('API_KEY')
cse_id = os.getenv('CSE_ID')
openai_api_key = os.getenv('OPENAI_API_KEY')


# Initialize agents
search_agent = SearchAgent(google_api_key, cse_id)
fetcher_agent = ContentFetcherAgent()
summarizer_agent = SummarizerAgent(openai_api_key)
pdf_generator_agent = PDFGeneratorAgent()

# Streamlit UI
st.title("Blog Generator with Multi-Agents")
st.write("Enter a topic to generate summarized blogs based on online sources.")

# User input
topic = st.text_input("Enter a topic", "")
outline = st.text_area("Enter an outline (optional):", height=150)


if topic and outline:
    st.write(f"**Searching for blogs related to:** {topic}")
    
    # Search for URLs
    urls = search_agent.search(topic)

    if not urls:
        st.error("No URLs found for the given topic. Please try another topic.")
    else:
        st.success(f"Found {len(urls)} sources. Processing...")
        summaries = []

        for i, url in enumerate(urls[:6], start=1):  # Limit to top 6 URLs
            # Fetch content from the URL
            content = fetcher_agent.fetch_content(url)

            if content:
                # Summarize the content
                summary = summarizer_agent.execute(content, outline)

                # Save the blog summary and content in a PDF
                pdf_path = pdf_generator_agent.generate_pdf(summary, i)

                summaries.append({'url': url, 'summary': summary, 'pdf': pdf_path})
            else:
                st.warning(f"Failed to fetch content from {url}")

        # Display summaries
        st.header("Generated Blog Summaries")
        if summaries:
            for blog in summaries:
                st.subheader(f"Blog from: {blog['url']}")
                st.write(f"**Summary:** {blog['summary']}")
                st.write(f"**Download PDF:** [Download PDF]({blog['pdf']})")  # Link to download the PDF
                st.write("---")
        else:
            st.error("No summaries could be generated.")


        # Fetch and summarize content
        # for url in urls[:6]:  # Limit to top 3 URLs
        #     # st.write(f"Fetching and summarizing content from: {url}")
        #     content = fetcher_agent.fetch_content(url)

        #     if content:
        #         summary = summarizer_agent.execute(content,outline)
        #         summaries.append({'url': url, 'summary': summary})
        #     else:
        #         st.warning(f"Failed to fetch content from {url}")

        # # Display summaries
        # st.header("Generated Blog Summaries")
        # if summaries:
        #     for i, blog in enumerate(summaries, 1):
        #         st.subheader(f"Blog {i}")
        #         st.write(f"**Source URL:** {blog['url']}")
        #         st.write(f"**Summary:** {blog['summary']}")
        #         st.write("---")
        # else:
        #     st.error("No summaries could be generated.")
