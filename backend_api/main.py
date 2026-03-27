from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, Query, HTTPException, Request, Response
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from pydantic import BaseModel
from typing import Optional
from dependencies import state_change, init_db_startup, get_user_repo, get_recipe_repo, get_ingredient_repo
from repo import User, Recipe, Ingredient, MealPlan, UserRepository, RecipeRepository, IngredientRepository
import jwt
import datetime
from dotenv import load_dotenv
import os

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    if app.state.env == "prod":
        init_db_startup()

    yield

app = FastAPI(lifespan=lifespan)

# define test state versus live state
state_change(app, "dev") # "dev" or "prod"

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
    plans: dict[str, dict[str, Optional[int]]]

def require_jwt(func):
    import functools
    @functools.wraps(func)
    def wrapper(*args, request: Request, **kwargs):
        token = request.cookies.get("jwt_token")
        if not token:
            raise HTTPException(status_code=401, detail="Not authenticated")
        try:
            payload = jwt.decode(token, os.getenv("JWT_KEY"), algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")
        request.state.jwt_payload = payload
        return func(*args, request=request, **kwargs)
    return wrapper

@app.get("/api/health")
def health():
    return {"ok": True}

@app.get("/api/count")
def count_get():
    global count
    count += 1
    return count

# Ingredient CRUD

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

# Recipe CRUD

@app.get("/api/recipe")
def get_recipe_by_title(recipe_title: str, repo: RecipeRepository = Depends(get_recipe_repo)):
    recipe = (recipe_title)
    return_recipe = repo.get_recipe_by_title(recipe)
    return {"id": return_recipe.id, "title": return_recipe.title, "cook_time": return_recipe.cook_time, "instructions": return_recipe.instructions, "ingredients": return_recipe.ingredients}

@app.get("/api/recipe/{id}")
def get_recipe_by_id(id: int, repo: RecipeRepository = Depends(get_recipe_repo)):
    return_recipe = repo.get_recipe_by_id(id)
    if not return_recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return {"id": return_recipe.id, "title": return_recipe.title, "cook_time": return_recipe.cook_time, "instructions": return_recipe.instructions, "ingredients": return_recipe.ingredients}

@app.post("/api/recipe")
@require_jwt
def create_recipe(recipe_data: RecipeCreate, repo: RecipeRepository = Depends(get_recipe_repo), ing_repo: IngredientRepository = Depends(get_ingredient_repo)):
    recipe = Recipe(id=None, title=recipe_data.title, instructions=recipe_data.instructions, cook_time=recipe_data.cook_time)
    saved_recipe = repo.create_recipe(recipe, recipe_data.ingredients, ing_repo) 
    saved_recipe = repo.get_recipe_by_id(saved_recipe.id)
    return {"id": saved_recipe.id, "title": saved_recipe.title, "cook_time": saved_recipe.cook_time, "instructions": saved_recipe.instructions, "ingredients": saved_recipe.ingredients}

@app.put("/api/recipe/{id}")
@require_jwt
def update_recipe(request: Request,id: int, recipe_data: RecipeCreate, repo: RecipeRepository = Depends(get_recipe_repo), ing_repo: IngredientRepository = Depends(get_ingredient_repo)):
    recipe = repo.get_recipe_by_id(id)
    if recipe.user_id != request.state.jwt_payload['id']:
        raise HTTPException(status_code=403, detail="User is not the author of this recipe")
    return_recipe = repo.update_recipe(recipe.id, recipe_data, ing_repo)
    return {"id": return_recipe.id, "title": return_recipe.title, "cook_time": return_recipe.cook_time, "instructions": return_recipe.instructions, "ingredients": return_recipe.ingredients}

@app.delete("/api/recipe/{id}")
@require_jwt
def delete_recipe(request:Request, id: int, repo: RecipeRepository = Depends(get_recipe_repo), ing_repo: IngredientRepository = Depends(get_ingredient_repo)):
    recipe = repo.get_recipe_by_id(id)
    if recipe.user_id != request.state.jwt_payload['id']:
        raise HTTPException(status_code=403, detail="User is not the author of this recipe")
    recipe = repo.del_recipe(id)
    return recipe

@app.get("/api/user/recipes")
@require_jwt
def get_recipe_by_user_id(request:Request, user_id: int, repo: RecipeRepository = Depends(get_recipe_repo)):
    pass

@app.get("/api/recipe_list")
def list_recipes(repo: RecipeRepository = Depends(get_recipe_repo)):
    recipe_list = repo.list_recipes()
    return recipe_list

@app.get("/api/recipe_list/user")
@require_jwt
def list_user_recipes(repo: RecipeRepository = Depends(get_recipe_repo)):
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

# User CRUD

@app.post("/api/user/register")
def create_user(user_data: UserCreate, repo: UserRepository = Depends(get_user_repo)):
    password_hash = User.hash_password(user_data.password)
    user = User(id=None, username=user_data.username, email=user_data.email, password_hash=password_hash)
    saved_user = repo.create_user(user)
    return {"id": saved_user.id, "username": saved_user.username, "email": saved_user.email}

@app.post("/api/user/login")
def user_login(user_data: UserLogin, response: Response, repo: UserRepository = Depends(get_user_repo)):
    user = repo.user_login(user_data.username, user_data.password)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

# login time
    jwt_expiry_time_seconds = 60*60*24
    now = datetime.datetime.now(datetime.timezone.utc)
    jwt_data = {
        "id": user.id,
        "username": user.username,
        "iat": now,
        "exp": now + datetime.timedelta(seconds=jwt_expiry_time_seconds),
    }
    jwt_token = jwt.encode(jwt_data, os.getenv('JWT_KEY'), algorithm="HS256")
    response.set_cookie(
        key="jwt_token",
        value=jwt_token,
        httponly=True,
        samesite="lax",
        max_age=jwt_expiry_time_seconds,
    )
    return {
        "id": user.id,
        "username": user.username
    }

@app.get("/api/user/id")
@require_jwt
def user_id(request: Request):
    payload = request.state.jwt_payload 
    # token = request.cookies.get("jwt_token")
    # if not token:
    #     raise HTTPException(status_code=401, detail="Not authenticated")
    # try:
    #     payload = jwt.decode(token, os.getenv('JWT_KEY'), algorithms=["HS256"])
    # except jwt.ExpiredSignatureError:
    #     raise HTTPException(status_code=401, detail="Token expired")
    # except jwt.InvalidTokenError:
    #     raise HTTPException(status_code=401, detail="Invalid token")
    return {"id": payload["id"], "username": payload["username"]}

@app.get("/api/user/logout")
@require_jwt
def user_logout(request: Request, response: Response):
    response.delete_cookie(key="jwt_token", httponly=True, samesite="lax")
    return "logged out"

@app.post("/api/user/test")
def user_test():
    user_bob = User(id=5, username="bob", email="bob@example.com", password_hash=User.hash_password("bob123"))
    verify1 = user_bob.verify_password('bob123')
    
    pass_bob = User.hash_password("bob123")
    user_bob2 = User(id=5, username="bob", email="bob@example.com", password_hash=pass_bob)
    verify2 = user_bob2.verify_password('bob123')
    return [verify1, verify2]

@app.post("/api/user/testdecorator")
@require_jwt
def user_test_decorator(request: Request):
    return request.state.jwt_payload

# Meal Plan CRUD

@app.get("/api/meal_plan")
@require_jwt
def get_user_meal_plans(request: Request, repo: UserRepository = Depends(get_user_repo)):
    user_id = request.state.jwt_payload['id']
    return_user_mealplans = repo.get_mealplans_by_user(user_id=user_id)
    return return_user_mealplans

@app.post("/api/meal_plan")
@require_jwt
def create_meal_plan(request: Request, meal_plan_data: MealPlanCreate, repo: UserRepository = Depends(get_user_repo)):
    user_id = request.state.jwt_payload['id']
    mealplan = MealPlan(id=None, plans=meal_plan_data.plans)
    return_mealplan = repo.create_meal_plan(user_id=user_id, meal_plan=mealplan)
    return return_mealplan

@app.post("/api/meal_plan/{id}")
@require_jwt
def update_meal_plan(request: Request, meal_plan_id: int, meal_plan_data: MealPlanCreate, repo: UserRepository = Depends(get_user_repo)):
    user_id = request.state.jwt_payload['id']
    return_mealplan = repo.update_meal_plan(user_id=user_id, meal_plan_id=meal_plan_id, meal_plan_data=meal_plan_data)
    return return_mealplan

@app.delete("/api/meal_plan/{id}")
@require_jwt
def delete_meal_plan(meal_plan_id: int, repo: UserRepository = Depends(get_user_repo)):
    meal_plan = repo.del_meal_plan(meal_plan_id)
    return meal_plan

@app.get("/api/meal_plan/{id}")
@require_jwt
def get_meal_plan_by_id(meal_plan_id: int, repo: UserRepository = Depends(get_user_repo)):
    return_mealplan = repo.get_meal_plan_by_id(meal_plan_id=meal_plan_id)
    return return_mealplan


DIST_DIR = Path(__file__).parent / "frontend_dist"
app.mount("/", StaticFiles(directory=DIST_DIR, html=True), name="frontend")