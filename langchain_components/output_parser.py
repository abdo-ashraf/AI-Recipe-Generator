from langchain_classic.output_parsers import StructuredOutputParser, ResponseSchema, PydanticOutputParser
from langchain_core.output_parsers import BaseOutputParser

from .models import Recipe


def get_parse_recipe_output() -> BaseOutputParser:

    # response_schemas = [
    #     ResponseSchema(
    #         name="title",
    #         description="Short recipe title"
    #     ),
    #     ResponseSchema(
    #         name="ingredients",
    #         description="comma-separated List of ingredients as strings"
    #     ),
    #     ResponseSchema(
    #         name="steps",
    #         description="non-numbered comma-separated List of cooking steps as strings"
    #     ),
    #     ResponseSchema(
    #         name="estimated_time",
    #         description="Estimated cooking time in minutes as an integer"
    #     ),
    #     ResponseSchema(
    #         name="estimated_calories",
    #         description="Estimated calories as an integer (kcal)"
    #     ),
    #     ResponseSchema(
    #         name="estimated_cost",
    #         description="Estimated cost with currency, e.g. 'USD 10' or 'EGP 150'"
    #     ),
    #     ResponseSchema(
    #         name="alternatives",
    #         description="comma-separated List of ingredient alternatives in format 'ingredient -> alternative'"
    #     ),
    # ]

    # parser = StructuredOutputParser.from_response_schemas(response_schemas)
    parser = PydanticOutputParser(pydantic_object=Recipe)
    return parser


def parse_recipe_output(raw: str) -> Recipe:
    """Parse raw LLM output into a typed `Recipe` model."""
    parser = get_parse_recipe_output()

    try:
        parsed = parser.parse(raw)
    except Exception:
        print(raw)
        raise ValueError("Failed to parse LLM output")

    if not isinstance(parsed, dict):
        try:
            parsed = dict(parsed)
        except Exception:
            raise TypeError("Parsed output from StructuredOutputParser is not a dict")

    # Post-process: convert comma-separated strings to lists
    list_fields = ["ingredients", "steps", "alternatives"]
    for field in list_fields:
        if field in parsed and isinstance(parsed[field], str):
            # Split by comma and strip whitespace from each item
            parsed[field] = [item.strip() for item in parsed[field].split(",") if item.strip()]

    return Recipe.parse_obj(parsed)
