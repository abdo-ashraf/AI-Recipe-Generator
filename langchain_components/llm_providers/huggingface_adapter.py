from ..llm_providers.base import BaseLLMProvider
from langchain_openai import ChatOpenAI

class HuggingFaceProvider(BaseLLMProvider):
    """Hugging Face provider using OpenAI-compatible API.
    
    Requires:
    - api_key argument (Hugging Face API token)
    """
    
    def __init__(self, model_name: str = None, temperature: float = 0.0, api_key: str = None):
        if not api_key:
            raise ValueError("Provide a Hugging Face API key in the settings panel")

        model = model_name or "google/gemma-4-31B-it:novita"
        temp = float(temperature)
        
        # Use LangChain's ChatOpenAI with Hugging Face endpoint
        self.llm = ChatOpenAI(
            model=model,
            temperature=temp,
            base_url="https://router.huggingface.co/v1",
            api_key=api_key,
        )

    def generate(self, prompt: str, max_tokens: int = 1024) -> str:
        # LangChain ChatOpenAI invoke returns a BaseMessage; extract text
        from langchain_core.messages import HumanMessage
        response = self.llm.invoke([HumanMessage(content=prompt)])
        return response.content
