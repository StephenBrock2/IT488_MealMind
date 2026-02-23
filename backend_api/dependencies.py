from mem_repo import MemUserRepository, MemRecipeRepository, MemIngredientRepository
#from sql_repo import SQLUserRepository, SQLRecipeRepository, SQLIngredientRepository

# In Memory Testing Repositories 
user_repo = MemUserRepository()
recipe_repo = MemRecipeRepository()
ingredient_repo = MemIngredientRepository()

# Production Database Repositories 
#user_repo = SQLUserRepository()
#recipe_repo = SQLRecipeRepository()
#ingredient_repo = SQLIngredientRepository()


def get_user_repo():
    return user_repo

def get_recipe_repo():
    return recipe_repo

def get_ingredient_repo():
    return ingredient_repo