from langchain_openai import ChatOpenAI
from pydantic import SecretStr
from .openai_compatible import OpenAICompatibleProvider

class OpenAIProvider(OpenAICompatibleProvider):
    """OpenAI provider adapter.
    
    Requires:
    - api_key argument (OpenAI API key)
    """
    
    def __init__(self, model_name: str | None = None, api_key: str | None = None):
        if not api_key:
            raise ValueError("Provide an OpenAI API key in the settings panel")

        model = model_name or "gpt-4o-mini"
        self.llm = ChatOpenAI(model=model, api_key=SecretStr(api_key))
