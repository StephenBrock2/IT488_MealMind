import unittest
from repo import User, Recipe, Ingredient, MealPlan
from mem_repo import MemUserRepository, MemRecipeRepository, MemIngredientRepository, mem_repo_startup

class TestCreateObjects(unittest.TestCase):

    def test_create_ingredient_object(self):
        ingredient = Ingredient(id=None, name='This is a test')
        self.assertIsInstance(ingredient, Ingredient)

    def test_create_recipe_object(self):
        recipe = Recipe(id=None, title='This is a test', instructions='This is also a test', cook_time= 0)
        self.assertIsInstance(recipe, Recipe)

    def test_create_user_object(self):
        user = User(id=None, username='Test', email='test@testing.com', password_hash=User.hash_password('testpassword'))
        self.assertIsInstance(user, User)

    def test_create_mealplan_object(self):
        # JSON null changed to Python None / conversion normally handled in json.loads
        plans = {"plans": {"2026-03-08": {"breakfast": 5,"lunch": 2,"dinner": None},
                        "2026-03-09": {"breakfast": 99,"lunch": 7,"dinner": 3},
                        "2026-03-10": {"breakfast": 56,"lunch": 71,"dinner": 43}
                        }
                }
        mealplan = MealPlan(id=None, plans=plans)
        self.assertIsInstance(mealplan, MealPlan)

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


class TestListAllRecipeFunction(unittest.TestCase):

    def test_list_recipes_return(self):
        ing_repo, repo, user_repo = mem_repo_startup()
        self.assertIsNotNone(repo.list_recipes())

    def test_list_recipes_type(self):
        ing_repo, repo, user_repo = mem_repo_startup()
        recipe_list = repo.list_recipes()
        self.assertIsInstance(recipe_list, list)

    def test_list_recipes_count(self):
        ing_repo, repo, user_repo = mem_repo_startup()
        self.assertEqual(100, second=len(repo.list_recipes()))

class TestListSixRecipeFunction(unittest.TestCase):

    def test_list_six_recipes_return(self):
        ing_repo, repo, user_repo = mem_repo_startup()
        self.assertIsNotNone(repo.list_six_recipes())

    def test_list_six_recipes_type(self):
        ing_repo, repo, user_repo = mem_repo_startup()
        recipe_list = repo.list_six_recipes()
        self.assertIsInstance(recipe_list, list)

    def test_list_six_recipes_count(self):
        ing_repo, repo, user_repo = mem_repo_startup()
        self.assertEqual(6, second=len(repo.list_six_recipes()))

class TestGetRandomRecipeFunction(unittest.TestCase):

    def test_get_random_recipe_return(self):
        ing_repo, repo, user_repo = mem_repo_startup()
        self.assertIsNotNone(repo.get_random_recipe())

    def test_get_random_recipe_type(self):
        ing_repo, repo, user_repo = mem_repo_startup()
        self.assertIsInstance(repo.get_random_recipe(), Recipe)

class TestGetRecipeByTitleFucntion(unittest.TestCase):

    def test_get_recipe_by_title(self):
        ing_repo, repo, user_repo = mem_repo_startup()
        self.assertIsNotNone(repo.get_recipe_by_title(title="World's Best Chili"))

    def test_get_recipe_by_no_title(self):
        ing_repo, repo, user_repo = mem_repo_startup()
        self.assertIsNone(repo.get_recipe_by_title(title=None))

class TestGetRecipeByIDFunction(unittest.TestCase):

    def test_get_recipe_by_id(self):
        ing_repo, repo, user_repo = mem_repo_startup()
        self.assertIsNotNone(repo.get_recipe_by_id(recipe_id=1))

    def test_get_recipe_by_no_id(self):
        ing_repo, repo, user_repo = mem_repo_startup()
        self.assertIsNone(repo.get_recipe_by_id(recipe_id=None))

class TestAddIngredientToRecipeFunction(unittest.TestCase):

    def test_add_ingredient(self):
        repo = MemRecipeRepository()
        ing_repo = MemIngredientRepository()
        recipe = Recipe(id=None, title='This is a test', instructions='This is also a test', cook_time= 0)
        ingredient = Ingredient(id=None, name='Ing1')
        repo.create_recipe(recipe)
        ing_repo.create_ingredient(ingredient)
        repo.add_ingredient(recipe, ingredient, value=1, measurement='tsp')
        ingredient_data = {"id": 1, "name": "Ing1", "quantity": 1, "unit": "tsp"}
        self.assertDictEqual(recipe.ingredients[0], ingredient_data)

    def test_add_ingredient_no_name(self):
        repo = MemRecipeRepository()
        ing_repo = MemIngredientRepository()
        recipe = Recipe(id=None, title='This is a test', instructions='This is also a test', cook_time= 0)
        ingredient = Ingredient(id=None, name=None)
        repo.create_recipe(recipe)
        ing_repo.create_ingredient(ingredient)
        repo.add_ingredient(recipe, ingredient, value=1, measurement='tsp')
        ingredient_data = {"id": 1, "name": None, "quantity": 1, "unit": "tsp"}
        self.assertIn(ingredient_data, recipe.ingredients)

    def test_add_ingredient_no_value(self):
        repo = MemRecipeRepository()
        ing_repo = MemIngredientRepository()
        recipe = Recipe(id=None, title='This is a test', instructions='This is also a test', cook_time= 0)
        ingredient = Ingredient(id=None, name='Ing1')
        repo.create_recipe(recipe)
        ing_repo.create_ingredient(ingredient)
        repo.add_ingredient(recipe, ingredient, value=None, measurement='tsp')
        ingredient_data = {"id": 1, "name": "Ing1", "quantity": None, "unit": "tsp"}
        self.assertIn(ingredient_data, recipe.ingredients)

    def test_add_ingredient_no_measurement(self):
        repo = MemRecipeRepository()
        ing_repo = MemIngredientRepository()
        recipe = Recipe(id=None, title='This is a test', instructions='This is also a test', cook_time= 0)
        ingredient = Ingredient(id=None, name='Ing1')
        repo.create_recipe(recipe)
        ing_repo.create_ingredient(ingredient)
        repo.add_ingredient(recipe, ingredient, value=1, measurement=None)
        ingredient_data = {"id": 1, "name": "Ing1", "quantity": 1, "unit": None}
        self.assertIn(ingredient_data, recipe.ingredients)

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