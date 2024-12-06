from Agent.content_agent_base import ContentAgentBase
import openai

class SummarizerAgent(ContentAgentBase):
    """
    Agent for summarizing content using OpenAI's API.
    """

    def __init__(self, openai_api_key, max_retries=3, verbose=True):
        """
        Initialize the SummarizerAgent.

        :param api_key: OpenAI API key
        :param max_retries: Number of retries for failed LLM calls
        :param verbose: Enable detailed print output
        """
        super().__init__("SummarizerAgent", max_retries, verbose)
        openai.api_key = openai_api_key

    def execute(self, content,outline=None):
        """
        Summarize the given content.

        :param content: Text to summarize
        :return: Summarized text
        """
        if self.verbose:
            print(f"[{self.name}]: Summarizing content...")
        
        # Prepare the prompt for summarization
        prompt = f"Summarize the following content:\n\n{content}"
        user_content="You are an AI assisstant that summarizes content fetched from URLs."

        if outline:
            # Include the outline in the prompt for summarization
            prompt = f"Summarize the following content, following this outline: {outline}\nContent: {content}"
        else:
            # If no outline is provided, summarize the content without it
            prompt = f"Summarize the following content: {content}"

        messages = [
            {"role": "system", "content": user_content},
            {"role": "user", "content": prompt}
        ]
        
        # Call the LLM through the base class's `call_llm` method
        summary = self.call_llm(messages, temperature=0.7, max_tokens=1200)

        if self.verbose:
            print(f"[{self.name}]: Summary generated successfully.")

        return summary
