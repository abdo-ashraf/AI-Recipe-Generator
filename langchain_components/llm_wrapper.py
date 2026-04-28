from typing import Optional

from .llm_providers.base import BaseLLMProvider
from .llm_providers.openai_adapter import OpenAIProvider
from .llm_providers.huggingface_adapter import HuggingFaceProvider
from .llm_providers.openrouter_adapter import OpenRouterProvider


PROVIDER_REGISTRY: dict[str, type[BaseLLMProvider]] = {
    "openai": OpenAIProvider,
    "huggingface": HuggingFaceProvider,
    "openrouter": OpenRouterProvider,
}


def get_llm_provider(
    provider_name: Optional[str] = None,
    model_name: Optional[str] = None,
    api_key: Optional[str] = None,
) -> BaseLLMProvider:
    name = (provider_name or "openai").lower()
    provider_class = PROVIDER_REGISTRY.get(name)
    if provider_class is None:
        supported = ", ".join(sorted(PROVIDER_REGISTRY))
        raise ValueError(f"Unsupported LLM provider: {name}. Choose from: {supported}")
    return provider_class(model_name=model_name, api_key=api_key)
