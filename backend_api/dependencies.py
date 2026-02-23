from fastapi import Request
from mem_repo import MemUserRepository, MemRecipeRepository, MemIngredientRepository
#from sql_repo import SQLUserRepository, SQLRecipeRepository, SQLIngredientRepository

def state_change(app, state: str):
    if state == 'dev':
        app.state.user_repo = MemUserRepository()
        app.state.recipe_repo = MemRecipeRepository()
        app.state.ingredient_repo = MemIngredientRepository()
    elif state == 'prod':
        #app.state.user_repo = SQLUserRepository()
        #app.state.recipe_repo = SQLRecipeRepository()
        #app.state.ingredient_repo = SQLIngredientRepository()
        pass

def get_user_repo(request: Request):
    return request.app.state.user_repo

def get_recipe_repo(request: Request):
    return request.app.state.recipe_repo

def get_ingredient_repo(request: Request):
    return request.app.state.ingredient_repo