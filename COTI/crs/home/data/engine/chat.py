from openai import OpenAI

class gpt:
    """
    A class to interact with OpenAI's GPT models for keyword extraction.

    Attributes:
        api_key (str): The API key for authenticating with OpenAI's API.
        client (OpenAI): The OpenAI client for API requests.
    """

    def __init__(self):
        """
        Initializes the KeywordExtractor with an API key.

        Parameters:
            api_key (str): The API key for OpenAI.
        """
        self.api_key = "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"
        self.client = OpenAI(api_key=self.api_key)

    def chat(self, content, max_tokens):
        """
        Extracts keywords from the provided content using OpenAI's model.

        Parameters:
            content (str): The content from which to extract keywords.
            max_tokens (int): The maximum number of tokens to generate in the response.

        Returns:
            str: The extracted keywords or relevant response from the model.
        """
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "you are a software engineer"},
                {"role": "user", "content": content}
            ],
            temperature=0.2,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content

