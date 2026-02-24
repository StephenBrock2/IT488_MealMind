from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from pydantic import BaseModel
from dependencies import state_change, get_user_repo, get_recipe_repo, get_ingredient_repo
from repo import User, Recipe, Ingredient, UserRepository, RecipeRepository, IngredientRepository

app = FastAPI()

# define test state versus live state
state_change(app, "dev") # "dev" or "prod"

count = 0

class IngredientPydantic(BaseModel):
    name: str

class RecipeCreate(BaseModel):
    title: str
    instructions: str

@app.get("/api/health")
def health():
    return {"ok": True}

@app.get("/api/count")
def count_get():
    global count
    count += 1
    return count

@app.get("/api/ingredient")
def ingredient_get(name: str):
    return {"ingredients": [{"name": name}, {"name": f"{name} juice"}]}

@app.post("/api/ingredient")
def ingredient_put(ingredient: IngredientPydantic):
    return {"message": f"added ingredient {ingredient.name}"}

@app.post("/api/recipe")
def create_recipe(recipe_data: RecipeCreate, repo: RecipeRepository = Depends(get_recipe_repo)):
    recipe = Recipe(id=None, title=recipe_data.title, instructions=recipe_data.instructions)
    saved_recipe = repo.create_recipe(recipe) 
    return {"id": saved_recipe.id, "title": saved_recipe.title, "instructions": saved_recipe.instructions}

DIST_DIR = Path(__file__).parent / "frontend_dist"
app.mount("/", StaticFiles(directory=DIST_DIR, html=True), name="frontend")
