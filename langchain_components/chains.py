from .llm_wrapper import get_llm_provider
from .prompts import RECIPE_PROMPT_TEMPLATE
from .output_parser import get_parse_recipe_output, parse_recipe_output
from .models import RecipeResult
from .config import MODE_INSTRUCTIONS


class Orchestrator:
    def __init__(self, provider_name: str | None = None, model_name: str | None = None, api_key: str | None = None):
        self.provider = get_llm_provider(provider_name, model_name=model_name, api_key=api_key)
        self.parse_recipe_output = get_parse_recipe_output()

    def generate_recipe(self, ingredients: str, language: str = "Arabic", mode: str = "natural") -> RecipeResult:
        mode = mode if mode in MODE_INSTRUCTIONS else "natural"
        prompt = RECIPE_PROMPT_TEMPLATE.format(
            user_input=ingredients,
            language=language,
            mode_instruction=MODE_INSTRUCTIONS[mode],
            format_instructions=self.parse_recipe_output.get_format_instructions(),
        )
        raw = self.provider.generate(prompt, mode=mode)

        parsed_model = parse_recipe_output(raw)
        return RecipeResult(raw=raw, parsed=parsed_model)
