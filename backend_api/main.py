from fastapi import FastAPI, Depends, Query
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from pydantic import BaseModel
from dependencies import state_change, init_db_startup, get_user_repo, get_recipe_repo, get_ingredient_repo
from repo import User, Recipe, Ingredient, UserRepository, RecipeRepository, IngredientRepository

app = FastAPI()

# define test state versus live state
state_change(app, "dev") # "dev" or "prod"

@app.on_event("startup")
def startup():
    if app.state.env == "prod":
        init_db_startup()

count = 0

class IngredientPydantic(BaseModel):
    name: str
    quantity: float
    unit: str

class RecipeCreate(BaseModel):
    title: str
    instructions: str
    ingredients: list[IngredientPydantic]

@app.get("/api/health")
def health():
    return {"ok": True}

@app.get("/api/count")
def count_get():
    global count
    count += 1
    return count

@app.get("/api/ingredient")
def ingredient_get(name=Query(None), repo: IngredientRepository = Depends(get_ingredient_repo)):
    ingredients = repo.list_ingredients()
    ingredientSearchedList = []

    if name:
        for ingredient in ingredients:
            if name.lower() in ingredient.name.lower():
                ingredientSearchedList.append(ingredient)
        return {"ingredients": ingredientSearchedList}

    return {"ingredients": ingredients}

@app.post("/api/ingredient")
def ingredient_put(ingredient: IngredientPydantic, repo: IngredientRepository = Depends(get_ingredient_repo)):
    new_ingredient = Ingredient(id=None, name=ingredient.name)
    saved_ingredient = repo.create_ingredient(new_ingredient)
    return {"id": saved_ingredient.id, "name": saved_ingredient.name}

@app.post("/api/recipe")
def create_recipe(recipe_data: RecipeCreate, repo: RecipeRepository = Depends(get_recipe_repo)):
    recipe = Recipe(id=None, title=recipe_data.title, instructions=recipe_data.instructions)
    saved_recipe = repo.create_recipe(recipe) 
    for i in recipe_data.ingredients:
        ingredient = Ingredient(id=None, name= i.name)
        repo.add_ingredient(saved_recipe, ingredient, value= i.quantity, measurement= i.unit)
    saved_recipe = repo.get_recipe_by_id(saved_recipe.id)
    ingredient_list = []
    for i, (quantity, unit) in saved_recipe.ingredients.items():
        ingredient_list.append({
            "name": i.name, 
            "quantity": quantity, 
            "unit": unit})
    return {"id": saved_recipe.id, "title": saved_recipe.title, "instructions": saved_recipe.instructions, "ingredients": ingredient_list}

@app.get("/api/recipe")
def get_recipe_by_title(recipe_title: str, repo: RecipeRepository = Depends(get_recipe_repo)):
    recipe = (recipe_title)
    return_recipe = repo.get_recipe_by_title(recipe)
    return {"id": return_recipe.id, "title": return_recipe.title, "instructions": return_recipe.instructions}

@app.get("/api/recipe_list")
def list_recipes(repo: RecipeRepository = Depends(get_recipe_repo)):
    recipe_list = repo.list_recipes()
    return_list = []
    ingredient_list = []
    for i in recipe_list:
        for ing, (quantity, unit) in i.ingredients.items():
            ingredient_list.append({
                "name": ing.name, 
                "quantity": quantity, 
                "unit": unit})
        recipe_data = {"id": i.id, "title": i.title, "instructions": i.instructions, "ingredients": ingredient_list}
        return_list.append(recipe_data)
        ingredient_list = []
    return return_list

DIST_DIR = Path(__file__).parent / "frontend_dist"
app.mount("/", StaticFiles(directory=DIST_DIR, html=True), name="frontend")
