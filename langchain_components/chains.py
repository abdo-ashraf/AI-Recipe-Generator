from .llm_wrapper import get_llm_provider
from .prompts import RECIPE_PROMPT_TEMPLATE
from .output_parser import get_parse_recipe_output


MODE_INSTRUCTIONS = {
    "strict": 
        """Follow the format strictly. Be precise and factual.
Do not add extra descriptions, storytelling, or assumptions.
Keep ingredients and steps minimal and realistic.""",

    "natural": 
        """Follow the format strictly. Be clear and helpful.
Use natural phrasing while keeping things concise.
Ensure the recipe is practical and easy to follow.""",

    "creative": 
        """Follow the format strictly. Be creative but still realistic.
You may enhance the recipe with interesting variations, flavors, or presentation ideas.
Keep the structure intact but make the recipe more appealing."""
}

class Orchestrator:
    def __init__(self, provider_name: str = None, model_name: str = None, api_key: str = None):
        self.provider = get_llm_provider(provider_name, model_name=model_name, api_key=api_key)
        self.parse_recipe_output = get_parse_recipe_output()

    def generate_recipe(self, ingredients: str, language: str = "Arabic", mode: str = "natural") -> dict:
        mode = mode if mode in MODE_INSTRUCTIONS else "natural"
        prompt = RECIPE_PROMPT_TEMPLATE.format(user_input=ingredients, language=language, mode_instruction=MODE_INSTRUCTIONS[mode], format_instructions=self.parse_recipe_output.get_format_instructions())
        raw = self.provider.generate(prompt, mode=mode)
        parsed = self.parse_recipe_output.parse(raw)

        return {
            "raw": raw,
            "parsed": parsed,
        }
