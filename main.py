from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from models.recipe import Recipe
from database import get_db, DBRecipe, DBIngredient
from recipe_converter import process_recipe
app = FastAPI()

class RecipeResponse(Recipe):
    id: int

    class Config:
        orm_mode = True

@app.get("/recipes/", response_model=List[RecipeResponse])
def get_recipes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    recipes = db.query(DBRecipe).offset(skip).limit(limit).all()
    return recipes

@app.get("/recipes/{recipe_id}", response_model=RecipeResponse)
def get_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = db.query(DBRecipe).filter(DBRecipe.id == recipe_id).first()
    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe

@app.post("/recipes/", response_model=RecipeResponse)
def create_recipe(recipe: Recipe, db: Session = Depends(get_db)):
    # Create the recipe first
    db_recipe = DBRecipe(
        title=recipe.title,
        instructions=recipe.instructions
    )
    db.add(db_recipe)
    db.flush()  # This gets us the recipe.id

    # Create the ingredients
    for ing in recipe.ingredients:
        db_ingredient = DBIngredient(
            name=ing.name,
            amount=ing.amount,
            unit=ing.unit,
            recipe_id=db_recipe.id
        )
        db.add(db_ingredient)

    db.commit()
    db.refresh(db_recipe)
    return db_recipe

@app.put("/recipes/{recipe_id}", response_model=RecipeResponse)
def update_recipe(recipe_id: int, recipe: Recipe, db: Session = Depends(get_db)):
    db_recipe = db.query(DBRecipe).filter(DBRecipe.id == recipe_id).first()
    if db_recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    # Update recipe basic info
    db_recipe.title = recipe.title
    db_recipe.instructions = recipe.instructions
    
    # Delete existing ingredients
    db.query(DBIngredient).filter(DBIngredient.recipe_id == recipe_id).delete()
    
    # Create new ingredients
    for ing in recipe.ingredients:
        db_ingredient = DBIngredient(
            name=ing.name,
            amount=ing.amount,
            unit=ing.unit,
            recipe_id=recipe_id
        )
        db.add(db_ingredient)
    
    db.commit()
    db.refresh(db_recipe)
    return db_recipe

@app.delete("/recipes/{recipe_id}")
def delete_recipe(recipe_id: int, db: Session = Depends(get_db)):
    db_recipe = db.query(DBRecipe).filter(DBRecipe.id == recipe_id).first()
    if db_recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    db.delete(db_recipe)
    db.commit()
    return {"message": "Recipe deleted successfully"}

class RecipeTextRequest(BaseModel):
    text: str

@app.post("/recipes/convert")
def convert_recipe_text(unstructured_recipes: RecipeTextRequest):
    processed_recipes = process_recipe(unstructured_recipes.text)
    return processed_recipes

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 