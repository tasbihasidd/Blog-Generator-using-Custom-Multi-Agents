import openai
from abc import ABC, abstractmethod
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

class ContentAgentBase(ABC):
    """
    Abstract base class for blog generator agents.
    This class provides a foundation for agents to perform specific tasks, 
    like searching for topics, fetching content, or summarizing.
    """

    def __init__(self, name, max_retries=3, verbose=True):
        """
        Initialize the agent.

        :param name: Name of the agent (e.g., "SearchAgent")
        :param max_retries: Number of retries in case of LLM failure
        :param verbose: If True, prints detailed output
        """
        self.name = name
        self.max_retries = max_retries
        self.verbose = verbose

    @abstractmethod
    def execute(self, *args, **kwargs):
        """
        Abstract method to be implemented by subclasses.
        This method should define the specific task of the agent.
        """
        pass

    def call_llm(self, prompt, temperature=0.7, max_tokens=150):
        """
        Helper function to call the OpenAI LLM.

        :param prompt: The input text for the LLM
        :param temperature: Sampling temperature for LLM response
        :param max_tokens: Maximum tokens for the response
        :return: The LLM response
        """
        retries = 0
        while retries < self.max_retries:
            try:
                if self.verbose:
                    print(f"[{self.name}]: Sending prompt to OpenAI: {prompt}")

                # OpenAI API call
                response = openai.Completion.create(
                    model="gpt-4",
                    prompt=prompt,
                    temperature=temperature,
                    max_tokens=max_tokens
                )

                # Extract and print the response
                reply = response['choices'][0]['text'].strip()
                if self.verbose:
                    print(f"[{self.name}]: Received response from OpenAI: {reply}")

                return reply

            except Exception as e:
                retries += 1
                if self.verbose:
                    print(f"[{self.name}]: Error calling OpenAI. Retrying... ({retries}/{self.max_retries}) - Error: {e}")

        raise Exception(f"[{self.name}] Failed to get a response from OpenAI after {self.max_retries} retries.")
