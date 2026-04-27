from typing import Optional

from .llm_providers.base import BaseLLMProvider
from .llm_providers.openai_adapter import OpenAIProvider
from .llm_providers.huggingface_adapter import HuggingFaceProvider
from .llm_providers.openrouter_adapter import OpenRouterProvider


def get_llm_provider(
    provider_name: Optional[str] = None,
    model_name: Optional[str] = None,
    temperature: Optional[float] = None,
    api_key: Optional[str] = None,
) -> BaseLLMProvider:
    name = (provider_name or "openai").lower()
    if name == "openai":
        return OpenAIProvider(model_name=model_name, temperature=temperature if temperature is not None else 0.0, api_key=api_key)
    elif name == "huggingface":
        return HuggingFaceProvider(model_name=model_name, temperature=temperature if temperature is not None else 0.0, api_key=api_key)
    elif name == "openrouter":
        return OpenRouterProvider(model_name=model_name, temperature=temperature if temperature is not None else 0.0, api_key=api_key)
    raise ValueError(f"Unsupported LLM provider: {name}. Choose from: 'openai', 'huggingface', 'openrouter'")
