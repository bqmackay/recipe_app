from pydantic import BaseModel, Field

# Pydantic models for validation
class Ingredient(BaseModel):
    """
    Use this model when representing a single ingredient in a recipe.
    """
    name: str = Field(description="Name of the ingredient")
    amount: float = Field(description="Quantity of the ingredient needed")
    unit: str = Field(description="Unit of measurement (e.g., cups, grams, pieces)")

    class Config:
        orm_mode = True 