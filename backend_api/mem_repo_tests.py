import unittest
from repo import User, Recipe, Ingredient
from mem_repo import MemUserRepository, MemRecipeRepository, MemIngredientRepository, mem_repo_startup

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

class TestRecipeDeleteFunction(unittest.TestCase):

    def test_delete_existing_recipe(self):
        ing_repo, repo, user_repo = mem_repo_startup()
        self.assertIsNotNone(repo.del_recipe(recipe_id=1))

    def test_delete_non_existing_recipe(self):
        ing_repo, repo, user_repo = mem_repo_startup()
        self.assertIsNone(repo.del_recipe(recipe_id=1000))

class TestGetRecipeByTitleFucntion(unittest.TestCase):

    @unittest.skip('Work in progress')
    def test_get_recipe_by_title(self, title: str) -> Recipe | None:
        pass

class TestGetRecipeByIDFunction(unittest.TestCase):

    @unittest.skip('Work in progress')
    def get_recipe_by_id(self, id: int) -> Recipe | None:
        pass

class TestAddIngredientToRecipeFunction(unittest.TestCase):

    @unittest.skip('Work in progress')
    def add_ingredient(self, recipe: Recipe, ingredient: Ingredient) -> None:
        pass

class TestRemoveIngredientFromRecipeFunciton(unittest.TestCase):

    @unittest.skip('Work in progress')
    def remove_ingredient(self, recipe: Recipe, ingredient: Ingredient) -> None:
        pass

class TestAddIngredientToRecipeByIDFunction(unittest.TestCase):

    @unittest.skip('Work in progress')
    def add_ingredient_by_id(self, recipe_id: int, ingredient_id: int, value: int, measurement: str, repo: MemIngredientRepository) -> Recipe:
        pass

class TestRemoveIngredientFromRecipeByIDFunciton(unittest.TestCase):

    @unittest.skip('Work in progress')
    def remove_ingredient_by_id(self, recipe_id: int, ingredient_id: int) -> None:
        pass

if __name__ == '__main__':
    unittest.main()