# AI Recipe Generator

Streamlit + LangChain prototype that generates recipes from ingredients, estimates calories and cost, and suggests alternatives.

Quick start (local)

```bash
python -m venv .venv
source .venv/bin/activate   # or .venv\Scripts\Activate.ps1 on Windows
pip install -r requirements.txt
streamlit run app.py
```

Visit http://localhost:8501 and configure settings in the sidebar:
- Choose provider (`openai`, `huggingface`, or `openrouter`)
- Enter provider API key (do not commit keys to source control)
- Choose output language and generation mode
- Toggle raw output visibility

## LLM Providers

- **OpenAI**: Uses OpenAI's official API (https://api.openai.com/v1)
- **Hugging Face**: Uses Hugging Face's OpenAI-compatible endpoint (https://router.huggingface.co/v1)
- **OpenRouter**: Uses OpenRouter's OpenAI-compatible endpoint (https://openrouter.ai/api/v1)

Both providers use the same OpenAI-compatible interface under the hood, so they're interchangeable from the app's point of view.

## Docker

Build the production image and run the Streamlit app (default port 8501):

```bash
docker build -t ai-recipe:latest .
docker run --rm -p 8501:8501 ai-recipe:latest
```

Pass provider API keys via environment variables when running the container:

```bash
docker run --rm -p 8501:8501 \
    -e OPENAI_API_KEY=sk_xxx \
    -e HF_API_KEY=hf_xxx \
    -e OPENROUTER_API_KEY=or_xxx \
    ai-recipe:latest
```

To change the Streamlit port at runtime use the `PORT` env var (Dockerfile honors `$PORT`):

```bash
docker run --rm -p 8080:8080 -e PORT=8080 ai-recipe:latest
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

There is no automated test suite yet. Quick verification steps:

1. Run the app locally and exercise recipe generation for several inputs.
2. Confirm the structured parser (`langchain_components/output_parser.py`) maps responses into `RecipeResult` correctly.
3. Test different providers and confirm behavior when API keys are missing.

## Future Work

- Add a `tests/` directory for parser, provider factory, and orchestration coverage.
- Move sidebar settings into a typed configuration object or read them from env config files.
- Add a dedicated render helper for Arabic/RTL presentation if the UI grows further.
- Consider CI and automated dependency checks (Dependabot or Renovate) for pinned deps.

If you'd like, I can:

- Add `python-dotenv` and update `app.py` to load `.env` automatically for local development.
- Create a `docker-compose.yml` for local compose-based development.
