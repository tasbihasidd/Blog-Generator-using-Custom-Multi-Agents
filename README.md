# Blog Generator with Multi-Agents

This project leverages multiple agents to generate blog posts based on user input, including searching for content online, fetching the content, summarizing it, and generating a PDF file of the final blog. The project uses OpenAI for summarization and Google's Custom Search API for searching blog sources. Additionally, it uses the FPDF library to generate PDFs of the blog content.

## Features
- **Search Agent**: Fetches URLs from Google Custom Search Engine based on the input topic.
- **Content Fetcher Agent**: Extracts content from the fetched URLs.
- **Summarizer Agent**: Summarizes the extracted content using OpenAI's GPT model.
- **PDF Generator Agent**: Creates a PDF for each blog summary with a downloadable link.
- **Streamlit Interface**: A simple Streamlit interface to input topics and view generated blogs and PDFs.

## Instructions

### 1. Run the app
streamlit run app.py 

### 2. Usage 
 - Enter a Topic: Provide a topic for the blog you want to generate.
 - Enter an Outline (Optional): You can provide a custom outline for the blog (e.g., "Introduction, Main Content, Conclusion").
 - Generate Blog: The app will search for relevant sources, fetch their content, summarize it, and then display the summaries. It will also generate a downloadable PDF for each blog.

### 3. Clone the repository
```bash
git clone https://github.com/tasbihasidd/Blog-Generator-using-Custom-Multi-Agents
