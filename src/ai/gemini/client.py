from google.genai.types import GenerateContentConfig

from src.core.base.ai.client import BaseAIClient
from google.genai import Client

from src.core.exceptions import RequestAIClientError, BuildAIClientError


class GeminiClient(BaseAIClient[Client]):
    """Gemini API client implementation using the google-genai SDK."""

    def start(self) -> None:
        """Create the Gemini SDK client."""
        try:
            self._client = Client(api_key=self._api_key)
        except Exception as e:
            raise BuildAIClientError(e)

    def close(self) -> None:
        """Close the Gemini SDK client."""
        self._client.close()

    def request(self, contents: str, prompt: str) -> str:
        """Send a generation request to Gemini and return the response text."""
        try:
            response = self._client.models.generate_content(
                model=self._model,
                contents=contents,
                config=GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.0,
                    system_instruction=prompt,
                ),
            )
            return response.text

        except Exception as e:
            raise RequestAIClientError(e)
