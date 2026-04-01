import unittest
import copy
from repo import User, Recipe, Ingredient, MealPlan
from mem_repo import MemUserRepository, MemRecipeRepository, MemIngredientRepository, mem_repo_startup

# Object Creation Tests

class TestCreateObjects(unittest.TestCase):

    def test_create_user_object(self):
        user = User(id=None, username='Test', email='test@testing.com', password_hash=User.hash_password('testpassword'))
        self.assertIsInstance(user, User)

    def test_create_ingredient_object(self):
        ingredient = Ingredient(id=None, name='This is a test')
        self.assertIsInstance(ingredient, Ingredient)

    def test_create_recipe_object(self):
        recipe = Recipe(id=None, title='This is a test', instructions='This is also a test', cook_time= 0, user_id=None, username=None)
        self.assertIsInstance(recipe, Recipe)

    def test_create_mealplan_object(self):
        # JSON null changed to Python None / conversion normally handled by json.loads
        plans = {"plans": {"2026-03-08": {"breakfast": 5,"lunch": 2,"dinner": None},
                        "2026-03-09": {"breakfast": 99,"lunch": 7,"dinner": 3},
                        "2026-03-10": {"breakfast": 56,"lunch": 71,"dinner": 43}
                        }
                }
        mealplan = MealPlan(id=None, plans=plans)
        self.assertIsInstance(mealplan, MealPlan)

# User Method Tests

class TestCreateUserFucntion(unittest.TestCase):

    def test_create_user(self):
        user_repo = MemUserRepository()
        user = User(id=None, username='Test', email='test@testing.com', password_hash=User.hash_password('testpassword'))
        self.assertEqual(0, len(user_repo.users))
        user_repo.create_user(user)
        self.assertIn(user, user_repo.users.values())
        user_repo.create_user(user)
        self.assertEqual(1, len(user_repo.users))
        
class TestDeleteUserFucntion(unittest.TestCase):

    def test_del_user(self):
        ing_repo, repo, user_repo = mem_repo_startup()
        user_repo.del_user(1)
        self.assertNotIn(1, user_repo.users)
        self.assertIsNone(user_repo.del_user(1))

class TestGetUserByIDFucntion(unittest.TestCase):

    def test_get_user_by_id(self):
        ing_repo, repo, user_repo = mem_repo_startup()
        self.assertIsNotNone(user_repo.get_user_by_id(1))
        self.assertIsNone(user_repo.get_user_by_id(101))

class TestGetUserByUsernameFucntion(unittest.TestCase):

    def test_get_user_by_username(self):
        ing_repo, repo, user_repo = mem_repo_startup()
        self.assertIsNotNone(user_repo.get_user_by_username('User1'))
        self.assertIsNone(user_repo.get_user_by_username('User101'))

class TestUserLoginFucntion(unittest.TestCase):

    def test_user_login(self):
        ing_repo, repo, user_repo = mem_repo_startup()
        self.assertIsNotNone(user_repo.user_login('user1', '1234'))
        self.assertIsNone(user_repo.user_login('user1', 'password'))

class TestCreateMealPlanFucntion(unittest.TestCase):

    def test_create_meal_plan(self):
        ing_repo, repo, user_repo = mem_repo_startup() 
        plans = {"plans": {"2026-03-08": {"breakfast": 5,"lunch": 2,"dinner": None},
                        "2026-03-09": {"breakfast": 99,"lunch": 7,"dinner": 3},
                        "2026-03-10": {"breakfast": 56,"lunch": 71,"dinner": 43}
                        }
                }
        mealplan = MealPlan(id=None, plans=plans)
        self.assertIn(user_repo.create_meal_plan(user_id=1, meal_plan=mealplan), user_repo.meal_plans.values())

    def test_create_meal_plan_no_plans(self):
        ing_repo, repo, user_repo = mem_repo_startup() 
        plans = {}
        mealplan = MealPlan(id=None, plans=plans)
        self.assertIn(user_repo.create_meal_plan(user_id=1, meal_plan=mealplan), user_repo.meal_plans.values())

    def test_create_meal_plan_no_user(self):
        ing_repo, repo, user_repo = mem_repo_startup() 
        plans = {"plans": {"2026-03-08": {"breakfast": 5,"lunch": 2,"dinner": None},
                        "2026-03-09": {"breakfast": 99,"lunch": 7,"dinner": 3},
                        "2026-03-10": {"breakfast": 56,"lunch": 71,"dinner": 43}
                        }
                }
        mealplan = MealPlan(id=None, plans=plans)
        self.assertIsNone(user_repo.create_meal_plan(user_id=None, meal_plan=mealplan))

class TestUpdateMealPlanFucntion(unittest.TestCase):

    def test_update_meal_plan(self):
        ing_repo, repo, user_repo = mem_repo_startup() 
        plans = {"plans": {"2026-03-08": {"breakfast": 5,"lunch": 2,"dinner": None},
                        "2026-03-09": {"breakfast": 99,"lunch": 7,"dinner": 3},
                        "2026-03-10": {"breakfast": 56,"lunch": 71,"dinner": 43}
                        }
                }
        new_plans = {}
        mealplan = MealPlan(id=None, plans=plans)
        user_repo.create_meal_plan(user_id=1, meal_plan=mealplan)
        user_repo.update_meal_plan(user_id=1, meal_plan_id=mealplan.id, meal_plan_data=new_plans)
        self.assertEqual(mealplan.plans, new_plans)

    def test_update_meal_plan_no_user(self):
        ing_repo, repo, user_repo = mem_repo_startup() 
        plans = {"plans": {"2026-03-08": {"breakfast": 5,"lunch": 2,"dinner": None},
                        "2026-03-09": {"breakfast": 99,"lunch": 7,"dinner": 3},
                        "2026-03-10": {"breakfast": 56,"lunch": 71,"dinner": 43}
                        }
                }
        new_plans = {}
        mealplan = MealPlan(id=None, plans=plans)
        user_repo.create_meal_plan(user_id=1, meal_plan=mealplan)
        self.assertIsNone(user_repo.update_meal_plan(user_id=None, meal_plan_id=mealplan.id, meal_plan_data=new_plans))

    def test_update_meal_plan_no_plan(self):
        ing_repo, repo, user_repo = mem_repo_startup() 
        plans = {"plans": {"2026-03-08": {"breakfast": 5,"lunch": 2,"dinner": None},
                        "2026-03-09": {"breakfast": 99,"lunch": 7,"dinner": 3},
                        "2026-03-10": {"breakfast": 56,"lunch": 71,"dinner": 43}
                        }
                }
        new_plans = {}
        mealplan = MealPlan(id=None, plans=plans)
        user_repo.create_meal_plan(user_id=1, meal_plan=mealplan)
        self.assertIsNone(user_repo.update_meal_plan(user_id=1, meal_plan_id=None, meal_plan_data=new_plans))

class TestGetMealPlanByIDFunction(unittest.TestCase):

    def test_get_meal_plan_by_id(self):
        ing_repo, repo, user_repo = mem_repo_startup() 
        plans = {"plans": {"2026-03-08": {"breakfast": 5,"lunch": 2,"dinner": None},
                        "2026-03-09": {"breakfast": 99,"lunch": 7,"dinner": 3},
                        "2026-03-10": {"breakfast": 56,"lunch": 71,"dinner": 43}
                        }
                }
        mealplan = MealPlan(id=None, plans=plans)
        user_repo.create_meal_plan(user_id=1, meal_plan=mealplan)
        self.assertIsNotNone(user_repo.get_meal_plan_by_id(1))

    def test_get_meal_plan_by_id_not_existing(self):
        ing_repo, repo, user_repo = mem_repo_startup() 
        self.assertIsNone(user_repo.get_meal_plan_by_id(1))

class TestGetMealPlanByUserIDFunction(unittest.TestCase):

    def test_get_meal_plans_by_user(self):
        ing_repo, repo, user_repo = mem_repo_startup()
        plans = {"plans": {"2026-03-08": {"breakfast": 5,"lunch": 2,"dinner": None},
                        "2026-03-09": {"breakfast": 99,"lunch": 7,"dinner": 3},
                        "2026-03-10": {"breakfast": 56,"lunch": 71,"dinner": 43}
                        }
                }
        mealplan = MealPlan(id=None, plans=plans)
        user_repo.create_meal_plan(user_id=1, meal_plan=mealplan)
        self.assertEqual(user_repo.get_meal_plans_by_user(1), {1: plans})

    def test_get_meal_plans_by_user_empty(self):
        ing_repo, repo, user_repo = mem_repo_startup() 
        self.assertEqual(user_repo.get_meal_plans_by_user(1), {})

class TestDeleteMealPlanFucntion(unittest.TestCase):
    
    def test_del_meal_plan(self):
        ing_repo, repo, user_repo = mem_repo_startup()
        plans = {"plans": {"2026-03-08": {"breakfast": 5,"lunch": 2,"dinner": None},
                        "2026-03-09": {"breakfast": 99,"lunch": 7,"dinner": 3},
                        "2026-03-10": {"breakfast": 56,"lunch": 71,"dinner": 43}
                        }
                }
        mealplan = MealPlan(id=None, plans=plans)
        user_repo.create_meal_plan(user_id=1, meal_plan=mealplan)
        self.assertIsNone(user_repo.del_meal_plan(meal_plan_id=1))

    def test_del_meal_plan_not_existing(self):
        ing_repo, repo, user_repo = mem_repo_startup()
        self.assertIsNone(user_repo.del_meal_plan(meal_plan_id=1))

# Ingredient Method Tests

class TestCreateIngredientFunction(unittest.TestCase):

    def test_create_ingredient(self):
        ing_repo = MemIngredientRepository()
        ingredient = Ingredient(id=None, name='This is a test')
        self.assertIn(ing_repo.create_ingredient(ingredient), ing_repo.ingredients.values())

    def test_create_ingredient_no_name(self):
        ing_repo = MemIngredientRepository()
        ingredient = Ingredient(id=None, name=None)
        self.assertIn(ing_repo.create_ingredient(ingredient), ing_repo.ingredients.values())

class TestDeleteIngredientFunction(unittest.TestCase):

    def test_del_ingredient(self):
        ing_repo, repo, user_repo = mem_repo_startup()
        self.assertIsNone(ing_repo.del_ingredient(1))

    def test_del_ingredient_not_existing(self):
        ing_repo, repo, user_repo = mem_repo_startup()
        self.assertIsNone(ing_repo.del_ingredient(1000))

class TestGetIngredientByIDFunction(unittest.TestCase):

    def test_get_ingredient_by_id(self):
        ing_repo, repo, user_repo = mem_repo_startup()
        self.assertEqual(ing_repo.get_ingredient_by_id(1), ing_repo.ingredients[1])

    def test_get_ingredient_by_id_not_existing(self):
        ing_repo, repo, user_repo = mem_repo_startup()
        self.assertIsNone(ing_repo.get_ingredient_by_id(1000))

class TestListAllIngredientsFunction(unittest.TestCase):

    def test_list_ingredients_empty(self):
        ing_repo = MemIngredientRepository()
        self.assertEqual(len(ing_repo.list_ingredients()), 0)

    def test_list_ingredients(self):
        ing_repo, repo, user_repo = mem_repo_startup()
        self.assertEqual(len(ing_repo.list_ingredients()), 100)

# Recipe Method Tests

class TestRecipeCreateFunciton(unittest.TestCase):

    def test_create_recipe(self):
        repo = MemRecipeRepository()
        ing_repo = MemIngredientRepository()
        recipe = Recipe(id=None, title='This is a test', instructions='This is also a test', cook_time= 0, user_id=None, username=None)
        ingredients = [{"name": "Ing1", "quantity": 1, "unit": "tsp"}, {"name": "Ing2", "quantity": 2, "unit": "cups"}, {"name": "Ing3", "quantity": 3, "unit": "gallons"}]
        self.assertIn(repo.create_recipe(recipe, ingredients, ing_repo), repo.recipes.values())

    def test_create_recipe_no_name(self):
        repo = MemRecipeRepository()
        ing_repo = MemIngredientRepository()
        recipe = Recipe(id=None, title=None, instructions='This is also a test', cook_time= 0, user_id=None, username=None)
        ingredients = [{"name": "Ing1", "quantity": 1, "unit": "tsp"}, {"name": "Ing2", "quantity": 2, "unit": "cups"}, {"name": "Ing3", "quantity": 3, "unit": "gallons"}]
        self.assertIn(repo.create_recipe(recipe, ingredients, ing_repo), repo.recipes.values())

    def test_create_recipe_no_instructions(self):
        repo = MemRecipeRepository()
        ing_repo = MemIngredientRepository()
        recipe = Recipe(id=None, title='This is a test', instructions=None, cook_time= 0, user_id=None, username=None)
        ingredients = [{"name": "Ing1", "quantity": 1, "unit": "tsp"}, {"name": "Ing2", "quantity": 2, "unit": "cups"}, {"name": "Ing3", "quantity": 3, "unit": "gallons"}]
        self.assertIn(repo.create_recipe(recipe, ingredients, ing_repo), repo.recipes.values())

    def test_create_recipe_no_ingredients(self):
        repo = MemRecipeRepository()
        ing_repo = MemIngredientRepository()
        recipe = Recipe(id=None, title='This is a test', instructions='This is also a test', cook_time= 0, user_id=None, username=None)
        ingredients = []
        self.assertIn(repo.create_recipe(recipe, ingredients, ing_repo), repo.recipes.values())

class TestUpdateRecipeFunction(unittest.TestCase):

    def test_update_recipe(self):
        ing_repo, repo, user_repo = mem_repo_startup()
        class DataObject1():
            def __init__(self, n, q, u):
                self.name = n
                self.quantity = q
                self.unit = u
        recipe_data = {"title": "Test","instructions": "This is a test","cook_time": 120,
            "ingredients": [DataObject1("Ing1", 1, "tsp"), DataObject1("Ing2", 2, "cups"), DataObject1("Ing3", 3, "gal")]}
        class DataObject2():
            def __init__(self):
                self.title = recipe_data["title"]
                self.instructions = recipe_data["instructions"]
                self.cook_time = recipe_data["cook_time"]
                self.ingredients = recipe_data["ingredients"]
        recipe_data_object = DataObject2()
        self.assertEqual(repo.update_recipe(recipe_id=1, recipe_data=recipe_data_object, ing_repo=ing_repo), repo.recipes[1])

    def test_update_recipe_versus_old(self):
        ing_repo, repo, user_repo = mem_repo_startup()
        recipe_old = copy.deepcopy(repo.recipes[1])
        class DataObject1():
            def __init__(self, n, q, u):
                self.name = n
                self.quantity = q
                self.unit = u
        recipe_data = {"title": "Test","instructions": "This is a test","cook_time": 120,
            "ingredients": [DataObject1("Ing1", 1, "tsp"), DataObject1("Ing2", 2, "cups"), DataObject1("Ing3", 3, "gal")]}
        class DataObject2():
            def __init__(self):
                self.title = recipe_data["title"]
                self.instructions = recipe_data["instructions"]
                self.cook_time = recipe_data["cook_time"]
                self.ingredients = recipe_data["ingredients"]
        recipe_data_object = DataObject2()
        recipe_new = repo.update_recipe(recipe_id=1, recipe_data=recipe_data_object, ing_repo=ing_repo)
        self.assertNotEqual(recipe_new, recipe_old)

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

class TestListRecipesByUserIDFunction(unittest.TestCase):

    def test_list_recipes_by_user_id(self):
        ing_repo, repo, user_repo = mem_repo_startup()
        recipe = Recipe(id=None, title='This is a test', instructions='This is also a test', cook_time= 0, user_id=1, username='user1')
        ingredients = [{"name": "Ing1", "quantity": 1, "unit": "tsp"}, {"name": "Ing2", "quantity": 2, "unit": "cups"}, {"name": "Ing3", "quantity": 3, "unit": "gallons"}]
        repo.create_recipe(recipe, ingredients, ing_repo)
        self.assertEqual(len(repo.list_recipes_by_user_id(1)), 1)
        recipe = Recipe(id=None, title='This is a test', instructions='This is also a test', cook_time= 0, user_id=1, username='user1')
        ingredients = [{"name": "Ing1", "quantity": 1, "unit": "tsp"}, {"name": "Ing2", "quantity": 2, "unit": "cups"}, {"name": "Ing3", "quantity": 3, "unit": "gallons"}]
        repo.create_recipe(recipe, ingredients, ing_repo)
        self.assertEqual(len(repo.list_recipes_by_user_id(1)), 2)

    def test_list_no_recipes_by_user_id(self):
        ing_repo, repo, user_repo = mem_repo_startup()
        self.assertIsNone(repo.list_recipes_by_user_id(1))

class TestAddIngredientToRecipeFunction(unittest.TestCase):

    def test_add_ingredient(self):
        ingredient_in_recipe = False
        ing_repo, repo, user_repo = mem_repo_startup()
        recipe = repo.get_recipe_by_id(1)
        ingredient = ing_repo.get_ingredient_by_id(1)
        repo.add_ingredient(recipe, ingredient, value=1, measurement='tsp')
        for ing in recipe.ingredients:
            if ing["id"] == ingredient.id:
                ingredient_in_recipe = True
        self.assertEqual(ingredient_in_recipe, True)

    def test_add_ingredient_no_name(self):
        ingredient_in_recipe = False
        ing_repo, repo, user_repo = mem_repo_startup()
        recipe = repo.get_recipe_by_id(1)
        ingredient = Ingredient(id=None, name='')
        ing_repo.create_ingredient(ingredient)
        repo.add_ingredient(recipe, ingredient, value=1, measurement='tsp')
        for ing in recipe.ingredients:
            if ing["id"] == ingredient.id:
                ingredient_in_recipe = True
        self.assertEqual(ingredient_in_recipe, True)

    def test_add_ingredient_no_value(self):
        ingredient_in_recipe = False
        ing_repo, repo, user_repo = mem_repo_startup()
        recipe = Recipe(id=None, title='This is a test', instructions='This is also a test', cook_time= 0, user_id=None, username=None)
        ingredient = Ingredient(id=None, name='Ing1')
        ing_repo.create_ingredient(ingredient)
        repo.add_ingredient(recipe, ingredient, value=None, measurement='tsp')
        for ing in recipe.ingredients:
            if ing["id"] == ingredient.id:
                ingredient_in_recipe = True
        self.assertEqual(ingredient_in_recipe, True)

    def test_add_ingredient_no_measurement(self):
        ingredient_in_recipe = False
        ing_repo, repo, user_repo = mem_repo_startup()
        recipe = Recipe(id=None, title='This is a test', instructions='This is also a test', cook_time= 0, user_id=None, username=None)
        ingredient = Ingredient(id=None, name='Ing1')
        ing_repo.create_ingredient(ingredient)
        repo.add_ingredient(recipe, ingredient, value=1, measurement=None)
        for ing in recipe.ingredients:
            if ing["id"] == ingredient.id:
                ingredient_in_recipe = True
        self.assertEqual(ingredient_in_recipe, True)

class TestRemoveIngredientFromRecipeFunciton(unittest.TestCase):

    def test_remove_ingredient(self):
        ing_repo, repo, user_repo = mem_repo_startup()
        recipe = repo.recipes[1]
        ingredient = Ingredient(id=None, name='Ing1')
        ing_repo.create_ingredient(ingredient)
        repo.add_ingredient(recipe, ingredient, value=1, measurement='tsp')
        repo.remove_ingredient(recipe, ingredient)
        self.assertNotIn(ingredient, recipe.ingredients)

    def test_remove_ingredient_not_existing(self):
        ing_repo, repo, user_repo = mem_repo_startup()
        recipe = repo.recipes[1]
        ingredient = Ingredient(id=None, name='Ing1')
        ing_repo.create_ingredient(ingredient)
        self.assertIsNone(repo.remove_ingredient(recipe, ingredient))

class TestAddIngredientToRecipeByIDFunction(unittest.TestCase):

    def test_add_ingredient_by_id(self):
        ing_repo, repo, user_repo = mem_repo_startup()
        recipe_id = 1
        ingredient_id = 1
        value = 5
        measurement = 'tsp'
        repo.add_ingredient_by_id(recipe_id, ingredient_id, value, measurement, ing_repo)
        ingredient_data = {'id': 1, 'name': 'salt', 'quantity': 5, 'unit': 'tsp'}
        self.assertIn(ingredient_data, repo.recipes[recipe_id].ingredients)

    def test_add_ingredient_by_id_no_recipe(self):
        ing_repo, repo, user_repo = mem_repo_startup()
        recipe_id = None
        ingredient_id = 1
        value = 5
        measurement = 'tsp'
        self.assertIsNone(repo.add_ingredient_by_id(recipe_id, ingredient_id, value, measurement, ing_repo))

    def test_add_ingredient_by_id_no_ingredient(self):
        ing_repo, repo, user_repo = mem_repo_startup()
        recipe_id = 1
        ingredient_id = None
        value = 5
        measurement = 'tsp'
        self.assertIsNone(repo.add_ingredient_by_id(recipe_id, ingredient_id, value, measurement, ing_repo))

    def test_add_ingredient_by_id_no_value(self):
        ing_repo, repo, user_repo = mem_repo_startup()
        recipe_id = 1
        ingredient_id = 1
        value = None
        measurement = 'tsp'
        repo.add_ingredient_by_id(recipe_id, ingredient_id, value, measurement, ing_repo)
        ingredient_data = {'id': 1, 'name': 'salt', 'quantity': None, 'unit': 'tsp'}
        self.assertIn(ingredient_data, repo.recipes[recipe_id].ingredients)

    def test_add_ingredient_by_id_no_measurment(self):
        ing_repo, repo, user_repo = mem_repo_startup()
        recipe_id = 1
        ingredient_id = 1
        value = 5
        measurement = None
        repo.add_ingredient_by_id(recipe_id, ingredient_id, value, measurement, ing_repo)
        ingredient_data = {'id': 1, 'name': 'salt', 'quantity': 5, 'unit': None}
        self.assertIn(ingredient_data, repo.recipes[recipe_id].ingredients)

class TestRemoveIngredientFromRecipeByIDFunciton(unittest.TestCase):

    def test_remove_ingredient_by_id(self):
        ing_repo, repo, user_repo = mem_repo_startup()
        recipe = repo.recipes[1]
        ingredient = Ingredient(id=None, name='Ing1')
        ing_repo.create_ingredient(ingredient)
        repo.add_ingredient(recipe, ingredient, value=1, measurement='tsp')
        repo.remove_ingredient_by_id(1, ingredient.id)
        self.assertNotIn(ingredient, recipe.ingredients)

    def test_remove_ingredient_by_id_no_ingredient(self):
        ing_repo, repo, user_repo = mem_repo_startup()
        recipe = repo.recipes[1]
        self.assertIsNone(repo.remove_ingredient_by_id(recipe.id, 1000))

    def test_remove_ingredient_by_id_no_recipe(self):
        ing_repo, repo, user_repo = mem_repo_startup()
        ingredient_id = 1
        self.assertIsNone(repo.remove_ingredient_by_id(1000, ingredient_id))

if __name__ == '__main__':
    unittest.main()