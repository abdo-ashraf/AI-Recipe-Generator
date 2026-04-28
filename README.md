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
- choose output language and generation mode
- toggle raw output visibility

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

- The code is written with a provider-agnostic `BaseLLMProvider` and adapters for OpenAI, Hugging Face, and OpenRouter.
- Shared OpenAI-compatible invocation logic lives in `langchain_components/llm_providers/openai_compatible.py`.
- The Streamlit app stays thin and renders a typed `RecipeResult` from `langchain_components/models.py`.
- The structured output parser is isolated from the UI and is used to produce typed recipe data.

## Adding a New Provider

1. Create `langchain_components/llm_providers/<provider>_adapter.py`:
   ```python
   from .base import BaseLLMProvider
   
   class MyProviderAdapter(BaseLLMProvider):
       def __init__(self, model_name: str = None, api_key: str = None):
           if not api_key:
               raise ValueError("Provide an API key")
           
           model = model_name or "default-model"
           
           # Initialize your LLM client here
           self.llm = YourLLMClient(api_key=api_key, model=model)

       def generate(self, prompt: str, mode: str = "natural") -> str:
           response = self.llm.generate(prompt)
           return response.text
   ```

2. Update `langchain_components/llm_wrapper.py` to register the new provider:
   ```python
   from .llm_providers.<provider>_adapter import MyProviderAdapter
   
   def get_llm_provider(provider_name: Optional[str] = None, model_name: Optional[str] = None, api_key: Optional[str] = None) -> BaseLLMProvider:
       name = (provider_name or "openai").lower()
       if name == "openai":
           return OpenAIProvider(model_name=model_name, api_key=api_key)
       elif name == "huggingface":
           return HuggingFaceProvider(model_name=model_name, api_key=api_key)
       elif name == "myprovider":
           return MyProviderAdapter(model_name=model_name, api_key=api_key)
       raise ValueError(f"Unsupported LLM provider: {name}")
   ```

3. Add your provider to the sidebar options in `app.py`.

See `langchain_components/llm_providers/PROVIDER_TEMPLATE.md` for detailed examples.

## Testing

There is not yet a dedicated automated test suite in this workspace. The current verification path is to run the Streamlit app locally and confirm recipe generation, structured parsing, and the raw-output toggle.

## Future Work

- Add a small `tests/` directory for parser, provider factory, and orchestration coverage.
- Move sidebar settings into a typed configuration object.
- Add a dedicated render helper for Arabic/RTL presentation if the UI grows further.
- Consider removing unused legacy compatibility folders once nothing imports them.
