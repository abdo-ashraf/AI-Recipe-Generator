from langchain_core.messages import HumanMessage

from ..config import PRESETS
from .base import BaseLLMProvider


class OpenAICompatibleProvider(BaseLLMProvider):
    def generate(self, prompt: str, mode: str = "natural") -> str:
        normalized_mode = mode if mode in PRESETS else "natural"
        response = self.llm.bind(**PRESETS[normalized_mode]).invoke([HumanMessage(content=prompt)])
        return response.content