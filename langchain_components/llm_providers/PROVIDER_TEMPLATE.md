"""
Template for adding new LLM providers to the AI Recipe Generator.

Steps:
1. Copy this file and rename it: <provider>_adapter.py
2. Implement the BaseLLMProvider interface
3. Accept explicit runtime inputs: api_key, temperature, and optional model_name
4. Register your provider in langchain_components/llm_wrapper.py
"""

from .base import BaseLLMProvider


class TemplateProvider(BaseLLMProvider):
    """Template for implementing a new LLM provider adapter."""

    def __init__(self, model_name: str = None, temperature: float = 0.0, api_key: str = None):
        if not api_key:
            raise ValueError("Provide an API key")

        model = model_name or "default-model"
        temp = float(temperature)

        # Initialize provider SDK client here.
        # Example:
        # self.client = YourClient(api_key=api_key)
        # self.model = model
        # self.temperature = temp
        raise NotImplementedError("Implement provider-specific initialization")

    def generate(self, prompt: str, max_tokens: int = 1024, temperature: float = None) -> str:
        # Example:
        # response = self.client.generate(
        #     model=self.model,
        #     prompt=prompt,
        #     max_tokens=max_tokens,
        #     temperature=self.temperature if temperature is None else float(temperature),
        # )
        # return response.text
        raise NotImplementedError("Implement provider-specific generation")


class AnthropicProviderExample(BaseLLMProvider):
    """Pseudo-example for an Anthropic-style provider."""

    def __init__(self, model_name: str = None, temperature: float = 0.0, api_key: str = None):
        if not api_key:
            raise ValueError("Provide an API key")

        self.model = model_name or "claude-3-sonnet-20240229"
        self.temperature = float(temperature)
        # self.client = Anthropic(api_key=api_key)

    def generate(self, prompt: str, max_tokens: int = 1024, temperature: float = None) -> str:
        # response = self.client.messages.create(...)
        # return response.content[0].text
        raise NotImplementedError()


class OllamaProviderExample(BaseLLMProvider):
    """Pseudo-example for local Ollama; api_key can be optional depending on deployment."""

    def __init__(self, model_name: str = None, temperature: float = 0.0, api_key: str = None):
        self.model = model_name or "llama2"
        self.temperature = float(temperature)
        self.base_url = "http://localhost:11434"
        # Optionally use api_key if your gateway enforces auth.

    def generate(self, prompt: str, max_tokens: int = 1024, temperature: float = None) -> str:
        # Use requests to call Ollama and return concatenated text.
        raise NotImplementedError()
