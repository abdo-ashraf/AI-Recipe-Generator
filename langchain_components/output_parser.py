from langchain_classic.output_parsers import StructuredOutputParser, ResponseSchema
from langchain_core.output_parsers import BaseOutputParser


def get_parse_recipe_output() -> BaseOutputParser:

    response_schemas = [
        ResponseSchema(
            name="title",
            description="Short recipe title"
        ),
        ResponseSchema(
            name="ingredients",
            description="List of ingredients as strings"
        ),
        ResponseSchema(
            name="steps",
            description="Ordered list of cooking steps as strings"
        ),
        ResponseSchema(
            name="estimated_time",
            description="Estimated cooking time in minutes as an integer"
        ),
        ResponseSchema(
            name="estimated_calories",
            description="Estimated calories as an integer (kcal)"
        ),
        ResponseSchema(
            name="estimated_cost",
            description="Estimated cost with currency, e.g. 'USD 10' or 'EGP 150'"
        ),
        ResponseSchema(
            name="alternatives",
            description="List of ingredient alternatives in format 'ingredient -> alternative'"
        ),
    ]

    parser = StructuredOutputParser.from_response_schemas(response_schemas)
    return parser
