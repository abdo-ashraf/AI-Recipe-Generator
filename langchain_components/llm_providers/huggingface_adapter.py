from langchain_openai import ChatOpenAI
from pydantic import SecretStr
from .openai_compatible import OpenAICompatibleProvider

class HuggingFaceProvider(OpenAICompatibleProvider):
    """Hugging Face provider using OpenAI-compatible API.
    
    Requires:
    - api_key argument (Hugging Face API token)
    """
    
    def __init__(self, model_name: str | None = None, api_key: str | None = None):
        if not api_key:
            raise ValueError("Provide a Hugging Face API key in the settings panel")

        model = model_name or "google/gemma-4-31B-it:novita"
        
        # Use LangChain's ChatOpenAI with Hugging Face endpoint
        self.llm = ChatOpenAI(
            model=model,
            base_url="https://router.huggingface.co/v1",
            api_key=SecretStr(api_key),
        )
