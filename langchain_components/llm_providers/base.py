from abc import ABC, abstractmethod

class BaseLLMProvider(ABC):
    """Abstract interface for LLM providers. Implementations should be small, focused adapters.

    Methods:
        generate(prompt, max_tokens, temperature) -> str
    """

    @abstractmethod
    def generate(self, prompt: str, max_tokens: int = 1024) -> str:
        raise NotImplementedError
