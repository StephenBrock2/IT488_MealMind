from mem_repo import MemUserRepository, MemRecipeRepository, MemIngredientRepository
#from sql_repo import SQLUserRepository, SQLRecipeRepository, SQLIngredientRepository

# define 'dev'/test state versus 'prod'/live state
state = 'dev'

def state_change(state):
    if state == 'dev':
        user_repo = MemUserRepository()
        recipe_repo = MemRecipeRepository()
        ingredient_repo = MemIngredientRepository()
    if state == 'prod':
        #user_repo = SQLUserRepository()
        #recipe_repo = SQLRecipeRepository()
        #ingredient_repo = SQLIngredientRepository()
        pass
    return user_repo, recipe_repo, ingredient_repo

user_repo, recipe_repo, ingredient_repo = state_change(state)

def get_user_repo():
    return user_repo

def get_recipe_repo():
    return recipe_repo

def get_ingredient_repo():
    return ingredient_repo