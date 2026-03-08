import unittest
import os
from dotenv import load_dotenv
load_dotenv()
os.environ['DATABASE_URL'] = os.getenv('TEST_DATABASE_URL')
from repo import User, Recipe, Ingredient
from sql_repo import SQLUserRepository, SQLRecipeRepository, SQLIngredientRepository, db_connect, db_disconnect

class TestSQLUserRepository(unittest.TestCase):

    def setUp(self):
        cur, conn = db_connect()
        cur.execute("DELETE FROM users")
        db_disconnect(cur, conn)

    def test_create_user(self):
        repo = SQLUserRepository()
        user = User(id = None, username = 'Spongebob Squarepants', email = 'spongebob@squarepants.com', password_hash = b'password1')

        created_user = repo.create_user(user)

        self.assertIsNotNone(created_user.id)
        self.assertEqual(created_user.username, 'Spongebob Squarepants')
        self.assertEqual(created_user.email, 'spongebob@squarepants.com')

    def test_del_user(self):
        repo = SQLUserRepository()
        user = User(id = None, username = 'Sheldon Plankton', email = 'sheldon@plankton.com', password_hash = b'password2')
        created_user = repo.create_user(user)

        repo.del_user(created_user.id)

        found_user = repo.get_user_by_id(created_user.id)

        self.assertIsNone(found_user)

    def test_get_user_by_id(self):
        repo = SQLUserRepository()
        user = User(id = None, username = 'Patrick Star', email = 'patrick@star.com', password_hash = b'password3')
        created_user = repo.create_user(user)

        found_user = repo.get_user_by_id(created_user.id)

        self.assertIsNotNone(found_user)
        self.assertEqual(found_user.username, 'Patrick Star')
        self.assertEqual(found_user.email, 'patrick@star.com')

    def test_get_user_by_username(self):
        repo = SQLUserRepository()
        user = User(id = None, username = 'Squidward Tentacles', email = 'squidward@tentacles.com', password_hash = b'password4')
        created_user = repo.create_user(user)

        found_user = repo.get_user_by_username(created_user.username)

        self.assertIsNotNone(found_user)
        self.assertEqual(found_user.username, 'Squidward Tentacles')
        self.assertEqual(found_user.email, 'squidward@tentacles.com')

class TestSQLRecipeRepository(unittest.TestCase):

    def setUp(self):
        cur, conn = db_connect()
        cur.execute("DELETE FROM recipe_ingredients")
        cur.execute("DELETE FROM recipes")
        db_disconnect(cur, conn)

    def test_create_recipe(self):
        repo = SQLRecipeRepository()
        recipe = Recipe(id = None, title = 'Krabby Patty', instructions = 'Cook patty. Assemble sandwich', user_id = None, cook_time = 15)

        created_recipe = repo.create_recipe(recipe)

        self.assertIsNotNone(created_recipe.id)
        self.assertEqual(created_recipe.title, 'Krabby Patty')
        self.assertEqual(created_recipe.instructions, 'Cook patty. Assemble sandwich')
        self.assertEqual(created_recipe.cook_time, 15)

    def test_del_recipe(self):
        repo = SQLRecipeRepository()
        recipe = Recipe(id = None, title = 'Kelp Shake', instructions = 'Blend ingredients', user_id = None, cook_time = 5)
        created_recipe = repo.create_recipe(recipe)

        repo.del_recipe(created_recipe.id)

        found_recipe = repo.get_recipe_by_id(created_recipe.id)
        self.assertIsNone(found_recipe)

    def test_list_recipes(self):
        repo = SQLRecipeRepository()
        recipe1 = Recipe(id = None, title = 'Chum Bucket Special', instructions = 'Mix chum', user_id = None, cook_time = 10)
        recipe2 = Recipe(id = None, title = 'Coral Bits', instructions = 'Fry coral', user_id = None, cook_time = 20)

        repo.create_recipe(recipe1)
        repo.create_recipe(recipe2)

        all_recipes = repo.list_recipes()

        self.assertIsInstance(all_recipes, list)
        self.assertEqual(len(all_recipes), 2)

    def test_get_recipe_by_title(self):
        repo = SQLRecipeRepository()
        recipe = Recipe(id = None, title = 'Krabby Fries', instructions = 'Fry potatoes', user_id = None, cook_time = 15)
        created_recipe = repo.create_recipe(recipe)

        found_recipe = repo.get_recipe_by_title(created_recipe.title)
        self.assertIsNotNone(found_recipe)
        self.assertEqual(found_recipe.title, 'Krabby Fries')
        self.assertEqual(found_recipe.instructions, 'Fry potatoes')
        self.assertEqual(found_recipe.cook_time, 15)

    def test_get_recipe_by_id(self):
        repo = SQLRecipeRepository()
        recipe = Recipe(id = None, title = 'Pretty Patty', instructions = 'Cook pretty patty. Assemble sandwich', user_id = None, cook_time = 15)
        created_recipe = repo.create_recipe(recipe)

        found_recipe = repo.get_recipe_by_id(created_recipe.id)
        self.assertIsNotNone(found_recipe)
        self.assertEqual(found_recipe.title, 'Pretty Patty')
        self.assertEqual(found_recipe.instructions, 'Cook pretty patty. Assemble sandwich')
        self.assertEqual(found_recipe.cook_time, 15)

    def test_get_latest_recipes(self):
        repo = SQLRecipeRepository()
        recipes = [
            ('Krabby Patty', 'Cook patty. Assemble sandwich', 15),
            ('Chum Bucket Special', 'Mix chum', 10),
            ('Coral Bits', 'Fry coral', 20),
            ('Krabby Fries', 'Fry potatoes', 15),
            ('Pretty Patty', 'Cook pretty patty. Assemble sandwich', 15),
            ('Krusty Krab Pizza', 'Assemble. Bake at 400 degrees. Cut into slices', 30),
            ('Bran Flakes', 'Add milk', 5),
            ('Kelp Shake', 'Blend kelp', 3)
        ]

        for title, instructions, cook_time in recipes:
            recipe = Recipe(id = None, title = title, instructions = instructions, user_id = None, cook_time = cook_time)
            repo.create_recipe(recipe)

        latest_recipes = repo.get_latest_recipes()

        self.assertIsInstance(latest_recipes, list)
        self.assertLessEqual(len(latest_recipes), 6)
        self.assertEqual(len(latest_recipes), 6)
        self.assertEqual(latest_recipes[0].title, 'Kelp Shake')
        self.assertEqual(latest_recipes[1].title, 'Bran Flakes')

    def test_add_ingredient(self):
        recipe_repo = SQLRecipeRepository()
        ingredient_repo = SQLIngredientRepository()

        recipe = Recipe(id = None, title = 'Krabby Patty', instructions = 'Cook patty. Assemble sandwich', user_id = None, cook_time = 15)
        created_recipe = recipe_repo.create_recipe(recipe)

        ingredient = Ingredient(id = None, name = 'Pickles')
        created_ingredient = ingredient_repo.create_ingredient(ingredient)

        recipe_repo.add_ingredient(created_recipe, created_ingredient, value = 2, measurement = 'slices')

        cur, conn = db_connect()
        cur.execute(
            "SELECT quantity FROM recipe_ingredients WHERE recipe_id = %s AND ingredient_id = %s",
            (created_recipe.id, created_ingredient.id)
        )
        row = cur.fetchone()
        db_disconnect(cur, conn)

        self.assertIsNotNone(row)
        self.assertEqual(row[0], '2 slices')

    def test_remove_ingredient(self):
        recipe_repo = SQLRecipeRepository()
        ingredient_repo = SQLIngredientRepository()

        recipe = Recipe(id = None, title = 'Krabby Patty', instructions = 'Cook patty. Assemble sandwich', user_id = None, cook_time = 15)
        created_recipe = recipe_repo.create_recipe(recipe)

        ingredient = Ingredient(id = None, name = 'Pickles')
        created_ingredient = ingredient_repo.create_ingredient(ingredient)

        recipe_repo.add_ingredient(created_recipe, created_ingredient, value = 2, measurement = 'slices')

        recipe_repo.remove_ingredient(created_recipe, created_ingredient)

        cur, conn = db_connect()
        cur.execute(
            "SELECT * FROM recipe_ingredients WHERE recipe_id = %s AND ingredient_id = %s",
            (created_recipe.id, created_ingredient.id)
        )
        row = cur.fetchone()
        db_disconnect(cur, conn)

        self.assertIsNone(row)

    def test_add_ingredient_by_id(self):
        recipe_repo = SQLRecipeRepository()
        ingredient_repo = SQLIngredientRepository()

        recipe = Recipe(id = None, title = 'Krabby Patty', instructions = 'Cook patty. Assemble sandwich', user_id = None, cook_time = 15)
        created_recipe = recipe_repo.create_recipe(recipe)

        ingredient = Ingredient(id = None, name = 'Pickles')
        created_ingredient = ingredient_repo.create_ingredient(ingredient)

        recipe_repo.add_ingredient_by_id(created_recipe.id, created_ingredient.id, value = 2, measurement = 'slices')

        cur, conn = db_connect()
        cur.execute(
            "SELECT quantity FROM recipe_ingredients WHERE recipe_id = %s AND ingredient_id = %s",
            (created_recipe.id, created_ingredient.id)
        )
        row = cur.fetchone()
        db_disconnect(cur, conn)

        self.assertIsNotNone(row)
        self.assertEqual(row[0], '2 slices')

    def test_remove_ingredient_by_id(self):
        recipe_repo = SQLRecipeRepository()
        ingredient_repo = SQLIngredientRepository()

        recipe = Recipe(id = None, title = 'Krabby Patty', instructions = 'Cook patty. Assemble sandwich', user_id = None, cook_time = 15)
        created_recipe = recipe_repo.create_recipe(recipe)

        ingredient = Ingredient(id = None, name = 'Pickles')
        created_ingredient = ingredient_repo.create_ingredient(ingredient)

        recipe_repo.add_ingredient_by_id(created_recipe.id, created_ingredient.id, value = 2, measurement = 'slices')

        recipe_repo.remove_ingredient_by_id(created_recipe.id, created_ingredient.id)

        cur, conn = db_connect()
        cur.execute(
            "SELECT * FROM recipe_ingredients WHERE recipe_id = %s AND ingredient_id = %s",
            (created_recipe.id, created_ingredient.id)
        )
        row = cur.fetchone()
        db_disconnect(cur, conn)

        self.assertIsNone(row)

class TestSQLIngredientRepository(unittest.TestCase):

    def setUp(self):
        cur, conn = db_connect()
        cur.execute("DELETE FROM ingredients")
        db_disconnect(cur, conn)

    def test_create_ingredient(self):
        repo = SQLIngredientRepository()
        ingredient = Ingredient(id = None, name = 'Kelp')

        created_ingredient = repo.create_ingredient(ingredient)

        self.assertIsNotNone(created_ingredient.id)
        self.assertEqual(created_ingredient.name, 'Kelp')

    def test_del_ingredient(self):
        repo = SQLIngredientRepository()
        ingredient = Ingredient(id = None, name = 'Chum')
        created_ingredient = repo.create_ingredient(ingredient)

        repo.del_ingredient(created_ingredient)

        found_ingredient = repo.get_ingredient_by_id(created_ingredient.id)

        self.assertIsNone(found_ingredient)

    def test_get_ingredient_by_id(self):
        repo = SQLIngredientRepository()
        ingredient = Ingredient(id = None, name = 'Potato')
        created_ingredient = repo.create_ingredient(ingredient)

        found_ingredient = repo.get_ingredient_by_id(created_ingredient.id)

        self.assertIsNotNone(found_ingredient)
        self.assertEqual(found_ingredient.name, 'Potato')

    def test_list_ingredients(self):
        repo = SQLIngredientRepository()
        ingredient1 = Ingredient(id = None, name = 'Kelp')
        ingredient2 = Ingredient(id = None, name = 'Chum')
        ingredient3 = Ingredient(id = None, name = 'Potato')

        repo.create_ingredient(ingredient1)
        repo.create_ingredient(ingredient2)
        repo.create_ingredient(ingredient3)

        ingredients = repo.list_ingredients()

        self.assertIsInstance(ingredients, list)
        self.assertEqual(len(ingredients), 3)