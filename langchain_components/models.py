from typing import List, Optional
from pydantic import BaseModel, Field


class Recipe(BaseModel):
    title: str = Field(description="Short recipe title")

    ingredients: List[str] = Field(
        description="List of ingredients"
    )

    steps: List[str] = Field(
        description="Ordered list of cooking steps"
    )

    estimated_time: int = Field(
        description="Estimated cooking time in minutes"
    )

    estimated_calories: int = Field(
        description="Estimated calories in kcal"
    )

    estimated_cost: str = Field(
        description="Estimated cost with currency, e.g. 'USD 10'"
    )

    alternatives: List[str] = Field(
        description="List of alternatives in format 'ingredient -> alternative'"
    )


class RecipeResult(BaseModel):
    raw: str
    parsed: Recipe
