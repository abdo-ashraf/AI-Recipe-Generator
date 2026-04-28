from ..llm_providers.base import BaseLLMProvider, PRESETS
from langchain_openai import ChatOpenAI

class HuggingFaceProvider(BaseLLMProvider):
    """Hugging Face provider using OpenAI-compatible API.
    
    Requires:
    - api_key argument (Hugging Face API token)
    """
    
    def __init__(self, model_name: str = None, api_key: str = None):
        if not api_key:
            raise ValueError("Provide a Hugging Face API key in the settings panel")

        model = model_name or "google/gemma-4-31B-it:novita"
        
        # Use LangChain's ChatOpenAI with Hugging Face endpoint
        self.llm = ChatOpenAI(
            model=model,
            base_url="https://router.huggingface.co/v1",
            api_key=api_key,
        )

    def generate(self, prompt: str, mode: str = "natural") -> str:
        # LangChain ChatOpenAI invoke returns a BaseMessage; extract text

        # fallback safety
        if mode not in PRESETS:
            mode = "natural"
        
        from langchain_core.messages import HumanMessage
        response = self.llm.bind(**PRESETS[mode]).invoke([HumanMessage(content=prompt)])
        return response.content
