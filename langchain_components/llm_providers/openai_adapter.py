from ..llm_providers.base import BaseLLMProvider, PRESETS
from langchain_openai import ChatOpenAI

class OpenAIProvider(BaseLLMProvider):
    """OpenAI provider adapter.
    
    Requires:
    - api_key argument (OpenAI API key)
    """
    
    def __init__(self, model_name: str = None, api_key: str = None):
        if not api_key:
            raise ValueError("Provide an OpenAI API key in the settings panel")

        model = model_name or "gpt-4o-mini"
        self.llm = ChatOpenAI(model=model, api_key=api_key)

    def generate(self, prompt: str, mode: str = "natural") -> str:
        # LangChain ChatOpenAI invoke returns a BaseMessage; extract text

        # fallback safety
        if mode not in PRESETS:
            mode = "natural"
        
        from langchain_core.messages import HumanMessage
        response = self.llm.bind(**PRESETS[mode]).invoke([HumanMessage(content=prompt)])
        return response.content
