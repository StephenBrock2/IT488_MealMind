import unittest
from repo import User, Recipe, Ingredient
from mem_repo import MemUserRepository, MemRecipeRepository, MemIngredientRepository

class TestRecipeCreateFunciton(unittest.TestCase):

    def test_create_recipe(self):
        repo = MemRecipeRepository()
        recipe = Recipe(id=None, title='This is a test', instructions='This is also a test', cook_time= 0)
        self.assertIn(repo.create_recipe(recipe), repo.recipes.values())

    def test_create_recipe_no_name(self):
        repo = MemRecipeRepository()
        recipe = Recipe(id=None, title=None, instructions='This is also a test', cook_time= 120)
        self.assertIn(repo.create_recipe(recipe), repo.recipes.values())

    def test_create_recipe_no_instrucitons(self):
        repo = MemRecipeRepository()
        recipe = Recipe(id=None, title='This is a test', instructions=None, cook_time= 150)
        self.assertIn(repo.create_recipe(recipe), repo.recipes.values())

    def test_create_recipe_no_ingredients(self):
        repo = MemRecipeRepository()
        recipe = Recipe(id=None, title='This is a test', instructions='This is also a test', cook_time= 50)
        self.assertIn(repo.create_recipe(recipe), repo.recipes.values())




if __name__ == '__main__':
    unittest.main()