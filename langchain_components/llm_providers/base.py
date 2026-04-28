from abc import ABC, abstractmethod

class BaseLLMProvider(ABC):
    """Abstract interface for LLM providers. Implementations should be small, focused adapters.

    Methods:
        generate(prompt, mode, max_tokens) -> str
    """

    @abstractmethod
    def generate(self, prompt: str, mode: str = "natural") -> str:
        raise NotImplementedError
