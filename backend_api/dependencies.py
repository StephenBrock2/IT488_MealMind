from mem_repo import MemUserRepository, MemRecipeRepository, MemIngredientRepository

mem_user_repo = MemUserRepository()
mem_recipe_repo = MemRecipeRepository()
mem_ingredient_repo = MemIngredientRepository()

def get_mem_user_repo():
    return mem_user_repo

def get_mem_recipe_repo():
    return mem_recipe_repo

def get_mem_ingredient_repo():
    return mem_ingredient_repo