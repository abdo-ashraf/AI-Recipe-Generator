from abc import ABC, abstractmethod

PRESETS = {
    "strict": {
        "temperature": 0.2,
        "top_p": 1.0,
        "frequency_penalty": 0.0,
        "presence_penalty": 0.0,
        "max_tokens": 1024,
    },
    "natural": {
        "temperature": 0.5,
        "top_p": 0.95,
        "frequency_penalty": 0.2,
        "presence_penalty": 0.1,
        "max_tokens": 1024,
    },
    "creative": {
        "temperature": 0.9,
        "top_p": 0.85,
        "frequency_penalty": 0.5,
        "presence_penalty": 0.5,
        "max_tokens": 1024,
    },
}

class BaseLLMProvider(ABC):
    """Abstract interface for LLM providers. Implementations should be small, focused adapters.

    Methods:
        generate(prompt, mode, max_tokens) -> str
    """

    @abstractmethod
    def generate(self, prompt: str, mode: str = "natural") -> str:
        raise NotImplementedError
