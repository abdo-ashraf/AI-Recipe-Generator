from ..llm_providers.base import BaseLLMProvider, PRESETS
from langchain_openai import ChatOpenAI


class OpenRouterProvider(BaseLLMProvider):
    """OpenRouter provider using OpenAI-compatible API.

    Notes:
    - Uses https://openrouter.ai/api/v1 as base URL.
    - Enables reasoning mode via extra request body.
    """

    def __init__(self, model_name: str = None, api_key: str = None):
        if not api_key:
            raise ValueError("Provide an OpenRouter API key in the settings panel")

        model = model_name or "nvidia/nemotron-3-super-120b-a12b:free"

        self.llm = ChatOpenAI(
            model=model,
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
            extra_body={"reasoning": {"enabled": True}},
        )

    def generate(self, prompt: str, mode: str = "natural") -> str:
        # LangChain ChatOpenAI invoke returns a BaseMessage; extract text

        # fallback safety
        if mode not in PRESETS:
            mode = "natural"
        
        from langchain_core.messages import HumanMessage
        response = self.llm.bind(**PRESETS[mode]).invoke([HumanMessage(content=prompt)])
        return response.content