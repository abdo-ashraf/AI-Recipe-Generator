from .llm_wrapper import get_llm_provider
from .prompts import RECIPE_PROMPT_TEMPLATE
from .output_parser import parse_recipe_output

class Orchestrator:
    def __init__(self, provider_name: str = None, model_name: str = None, temperature: float = None, api_key: str = None):
        self.provider = get_llm_provider(provider_name, model_name=model_name, temperature=temperature, api_key=api_key)

    def generate_recipe(self, ingredients: str) -> dict:
        # Format prompt using LangChain's ChatPromptTemplate
        prompt = RECIPE_PROMPT_TEMPLATE.format(ingredients=ingredients)
        raw = self.provider.generate(prompt)
        parsed = parse_recipe_output(raw)
        return {
            "raw": raw,
            "parsed": parsed,
        }
