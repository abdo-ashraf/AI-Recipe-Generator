# AI Recipe Generator

Streamlit + LangChain prototype that generates recipes from ingredients, estimates calories and cost, and suggests alternatives.

Quick start

```bash
pip install -r requirements.txt
streamlit run app.py
```

Visit `http://localhost:8501` and configure settings in the sidebar:
- choose provider (`openai`, `huggingface`, or `openrouter`)
- enter provider API key (never stored in `.env`)
- set temperature using the slider

## LLM Providers

- **OpenAI**: Uses OpenAI's official API (https://api.openai.com/v1)
- **Hugging Face**: Uses Hugging Face's OpenAI-compatible endpoint (https://router.huggingface.co/v1)
- **OpenRouter**: Uses OpenRouter's OpenAI-compatible endpoint (https://openrouter.ai/api/v1)

Both providers use the same OpenAI-compatible interface under the hood, so they're interchangeable from the app's point of view.

## Docker

```bash
docker build -t ai-recipe .
docker run -p 8501:8501 ai-recipe
```

## Architecture

- The code is written with a provider-agnostic `BaseLLMProvider` and adapters for OpenAI, Hugging Face, and OpenRouter. Add new providers by implementing `BaseLLMProvider` in `langchain_components/llm_providers/`.
- The `SYSTEM_PROMPT` in `langchain_components/prompts.py` is strict to encourage consistent parsing.
- All chains and parsers are independent of the LLM provider.

## Adding a New Provider

1. Create `langchain_components/llm_providers/<provider>_adapter.py`:
   ```python
   from .base import BaseLLMProvider
   
   class MyProviderAdapter(BaseLLMProvider):
       def __init__(self, model_name: str = None, temperature: float = 0.0, api_key: str = None):
           if not api_key:
               raise ValueError("Provide an API key")
           
           model = model_name or "default-model"
           temp = float(temperature)
           
           # Initialize your LLM client here
           self.llm = YourLLMClient(api_key=api_key, model=model)
       
       def generate(self, prompt: str, max_tokens: int = 1024, temperature: float = None) -> str:
           response = self.llm.generate(prompt)
           return response.text
   ```

2. Update `langchain_components/llm_wrapper.py` to register the new provider:
   ```python
   from .llm_providers.<provider>_adapter import MyProviderAdapter
   
   def get_llm_provider(provider_name: Optional[str] = None, model_name: Optional[str] = None, temperature: Optional[float] = None, api_key: Optional[str] = None) -> BaseLLMProvider:
       name = (provider_name or "openai").lower()
       if name == "openai":
           return OpenAIProvider(model_name=model_name, temperature=temperature if temperature is not None else 0.0, api_key=api_key)
       elif name == "huggingface":
           return HuggingFaceProvider(model_name=model_name, temperature=temperature if temperature is not None else 0.0, api_key=api_key)
       elif name == "myprovider":
           return MyProviderAdapter(model_name=model_name, temperature=temperature if temperature is not None else 0.0, api_key=api_key)
       raise ValueError(f"Unsupported LLM provider: {name}")
   ```

3. Add your provider to the sidebar options in `app.py`.

See `langchain_components/llm_providers/PROVIDER_TEMPLATE.md` for detailed examples.

## Testing

All tests are organized in the `tests/` directory:

```bash
# Run smoke tests
python tests/test_smoke.py

# Test Hugging Face integration
python tests/test_huggingface_integration.py

# Run comprehensive integration tests
python tests/test_comprehensive.py

# Validate app structure
python tests/test_app_structure.py
```

Run all tests at once with a simple loop:
```bash
for test in tests/test_*.py; do python "$test"; done
```
