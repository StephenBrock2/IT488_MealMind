from fastapi import Request
from mem_repo import MemUserRepository, MemRecipeRepository, MemIngredientRepository, mem_repo_startup
from sql_repo import init_db, SQLUserRepository, SQLRecipeRepository, SQLIngredientRepository

def state_change(app, state: str):
    app.state.env = state
    if state == 'dev':
        app.state.user_repo = MemUserRepository()
        app.state.recipe_repo = MemRecipeRepository()
        app.state.ingredient_repo = MemIngredientRepository()
    elif state == 'prod':
        app.state.user_repo = SQLUserRepository()
        app.state.recipe_repo = SQLRecipeRepository()
        app.state.ingredient_repo = SQLIngredientRepository()

def get_user_repo(request: Request):
    return request.app.state.user_repo

def get_recipe_repo(request: Request):
    return request.app.state.recipe_repo

def get_ingredient_repo(request: Request):
    return request.app.state.ingredient_repo

def init_db_startup():
    init_db()

def init_mem_startup():
    mem_repo_startup()