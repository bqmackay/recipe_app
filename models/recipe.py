from pydantic import BaseModel, Field
from typing import List
from models.ingredient import Ingredient

class Recipe(BaseModel):
    """
    Use this model when working with complete cooking recipes.
    """
    title: str = Field(title="title", description="Name of the recipe")
    ingredients: List[Ingredient] = Field(title="ingredients", description="List of ingredients needed for the recipe")
    instructions: list[str] = Field(title="instructions", description="Step-by-step instructions to prepare the recipe")
