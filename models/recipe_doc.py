from pydantic import BaseModel, Field
from typing import List
from models.recipe import Recipe

class RecipeDoc(BaseModel):
    """
    Use this model when you have multiple recipes that you need to put into the doc
    """
    recipes: List[Recipe] = Field(description="a list of recipes")
