from langchain_openai import ChatOpenAI
from pydantic import SecretStr
from .openai_compatible import OpenAICompatibleProvider


class OpenRouterProvider(OpenAICompatibleProvider):
    """OpenRouter provider using OpenAI-compatible API.

    Notes:
    - Uses https://openrouter.ai/api/v1 as base URL.
    - Enables reasoning mode via extra request body.
    """

    def __init__(self, model_name: str | None = None, api_key: str | None = None):
        if not api_key:
            raise ValueError("Provide an OpenRouter API key in the settings panel")

        model = model_name or "nvidia/nemotron-3-super-120b-a12b:free"

        self.llm = ChatOpenAI(
            model=model,
            base_url="https://openrouter.ai/api/v1",
            api_key=SecretStr(api_key),
            extra_body={"reasoning": {"enabled": True}},
        )
