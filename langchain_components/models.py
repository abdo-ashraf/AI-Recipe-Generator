from typing import List, Optional

from pydantic import BaseModel, Field


class Recipe(BaseModel):
    title: str
    language: Optional[str] = None
    ingredients: List[str]
    steps: List[str]
    estimated_time: Optional[int] = None
    estimated_calories: Optional[int] = None
    estimated_cost: Optional[str] = None
    alternatives: List[str] = Field(default_factory=list)


class RecipeResult(BaseModel):
    raw: str
    parsed: Recipe
