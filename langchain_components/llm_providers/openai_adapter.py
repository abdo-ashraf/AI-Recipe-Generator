from ..llm_providers.base import BaseLLMProvider
from langchain_openai import ChatOpenAI

class OpenAIProvider(BaseLLMProvider):
    """OpenAI provider adapter.
    
    Requires:
    - api_key argument (OpenAI API key)
    """
    
    def __init__(self, model_name: str = None, temperature: float = 0.0, api_key: str = None):
        if not api_key:
            raise ValueError("Provide an OpenAI API key in the settings panel")

        model = model_name or "gpt-4o-mini"
        temp = float(temperature)
        self.llm = ChatOpenAI(model=model, temperature=temp, api_key=api_key)

    def generate(self, prompt: str, max_tokens: int = 1024) -> str:
        # LangChain ChatOpenAI invoke returns a BaseMessage; extract text
        from langchain_core.messages import HumanMessage
        response = self.llm.invoke([HumanMessage(content=prompt)])
        return response.content
