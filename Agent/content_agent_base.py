import openai
from abc import ABC, abstractmethod
import os
from dotenv import load_dotenv
import time 
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
        pass

    def call_llm(self, messages, temperature=0.7, max_tokens=150):
        retries = 0
        while retries < self.max_retries:
            try:
                # Sending message to OpenAI
                response = openai.ChatCompletion.create(
                    model='gpt-4o',  # or another valid model name
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens
                )

                reply = response.choices[0].message['content']
                return reply

            except openai.error.RateLimitError as e:
                retries += 1
                print(f"[{self.name}] Rate limit exceeded. Retrying... (Attempt {retries})")
                time.sleep(10)  # Wait 10 seconds before retrying

            except openai.error.APIError as e:
                retries += 1
                print(f"[{self.name}] API error: {e}. Retrying... (Attempt {retries})")
                time.sleep(5)  # Wait 5 seconds before retrying

            except Exception as e:
                retries += 1
                print(f"[{self.name}] Failed to generate response from OpenAI. Retrying... (Attempt {retries}) Error: {e}")
                time.sleep(5)  # Delay for 5 seconds before retrying

        raise Exception(f"[{self.name}] Failed to get a response from OpenAI after {self.max_retries} retries.")
