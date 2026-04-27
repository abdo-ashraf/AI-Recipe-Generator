from ..llm_providers.base import BaseLLMProvider
from langchain_openai import ChatOpenAI


class OpenRouterProvider(BaseLLMProvider):
    """OpenRouter provider using OpenAI-compatible API.

    Notes:
    - Uses https://openrouter.ai/api/v1 as base URL.
    - Enables reasoning mode via extra request body.
    """

    def __init__(self, model_name: str = None, temperature: float = 0.0, api_key: str = None):
        if not api_key:
            raise ValueError("Provide an OpenRouter API key in the settings panel")

        model = model_name or "nvidia/nemotron-3-super-120b-a12b:free"
        temp = float(temperature)

        self.llm = ChatOpenAI(
            model=model,
            temperature=temp,
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
            extra_body={"reasoning": {"enabled": True}},
        )

    def generate(self, prompt: str, max_tokens: int = 1024, temperature: float = None) -> str:
        from langchain_core.messages import HumanMessage

        response = self.llm.invoke([HumanMessage(content=prompt)])
        return response.content
