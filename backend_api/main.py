from fastapi import FastAPI, Depends, Query
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from pydantic import BaseModel
from typing import Optional
from dependencies import state_change, init_db_startup, get_user_repo, get_recipe_repo, get_ingredient_repo
from repo import User, Recipe, Ingredient, MealPlan, UserRepository, RecipeRepository, IngredientRepository

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
    cook_time: int
    ingredients: list[IngredientPydantic]

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class MealPlanCreate(BaseModel):
    username: str
    plans: dict[str, list[Optional[int]]]

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

    # if there is a name query string, filter results by name 
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

@app.delete("/api/ingredient/{id}")
def ingredient_delete(id: int, repo: IngredientRepository = Depends(get_ingredient_repo)):
    ingredient = Ingredient(id=id, name="")
    repo.del_ingredient(ingredient)
    return {"ok": True}

@app.get("/api/recipe")
def get_recipe_by_title(recipe_title: str, repo: RecipeRepository = Depends(get_recipe_repo)):
    recipe = (recipe_title)
    return_recipe = repo.get_recipe_by_title(recipe)
    return {"id": return_recipe.id, "title": return_recipe.title, "cook_time": return_recipe.cook_time, "instructions": return_recipe.instructions, "ingredients": return_recipe.ingredients}

@app.post("/api/recipe")
def create_recipe(recipe_data: RecipeCreate, repo: RecipeRepository = Depends(get_recipe_repo), ing_repo: IngredientRepository = Depends(get_ingredient_repo)):
    recipe = Recipe(id=None, title=recipe_data.title, instructions=recipe_data.instructions, cook_time=recipe_data.cook_time)
    saved_recipe = repo.create_recipe(recipe) 
    for i in recipe_data.ingredients:
        ingredient = Ingredient(id=None, name= i.name)
        saved_ingredient = ing_repo.create_ingredient(ingredient)
        saved_ingredient = ing_repo.get_ingredient_by_id(saved_ingredient.id)
        repo.add_ingredient(saved_recipe, saved_ingredient, value= i.quantity, measurement= i.unit)
    saved_recipe = repo.get_recipe_by_id(saved_recipe.id)
    return {"id": saved_recipe.id, "title": saved_recipe.title, "cook_time": saved_recipe.cook_time, "instructions": saved_recipe.instructions, "ingredients": saved_recipe.ingredients}

@app.get("/api/recipe_list")
def list_recipes(repo: RecipeRepository = Depends(get_recipe_repo)):
    recipe_list = repo.list_recipes()
    return recipe_list

@app.get("/api/recipe_reel")
def list_six_recipes(repo: RecipeRepository = Depends(get_recipe_repo)):
    six_list = repo.list_six_recipes()
    return six_list

@app.get("/api/recipe_random")
def get_random_recipe(repo: RecipeRepository = Depends(get_recipe_repo)):
    return_recipe = repo.get_random_recipe()
    return {"id": return_recipe.id, "title": return_recipe.title, "cook_time": return_recipe.cook_time, "instructions": return_recipe.instructions, "ingredients": return_recipe.ingredients}

@app.post("/api/user")
def create_user(user_data: UserCreate, repo: UserRepository = Depends(get_user_repo)):
    password_hash = User.hash_password(user_data.password)
    user = User(id=None, username=user_data.username, email=user_data.email, password_hash=password_hash)
    saved_user = repo.create_user(user)
    return {"id": saved_user.id, "username": saved_user.username, "email": saved_user.email}

@app.post("/api/user/login")
def user_login(user_data: UserLogin, repo: UserRepository = Depends(get_user_repo)):
    return {"Login Success"}

@app.post("/api/user/mealplan")
def create_meal_plan(mealplan_data: MealPlanCreate, repo: UserRepository = Depends(get_user_repo)):
    return {"Create Success"}

@app.get("/api/user/mealplan/id")
def get_meal_plan_by_id(user_id: int, meal_plan_id: int, repo: UserRepository = Depends(get_user_repo)):
    return {"Get Success"}

@app.get("/api/user/mealplan")
def get_user_meal_plans(user_id: int, repo: UserRepository = Depends(get_user_repo)):
    return {"Get Success"}

DIST_DIR = Path(__file__).parent / "frontend_dist"
app.mount("/", StaticFiles(directory=DIST_DIR, html=True), name="frontend")
