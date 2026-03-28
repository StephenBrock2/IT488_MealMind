import unittest
import os
from dotenv import load_dotenv

load_dotenv()
os.environ['DATABASE_URL'] = os.getenv('TEST_DATABASE_URL')
from repo import User, Recipe, Ingredient, MealPlan
from sql_repo import SQLUserRepository, SQLRecipeRepository, SQLIngredientRepository, db_connect, db_disconnect


class TestSQLUserRepository(unittest.TestCase):

    def setUp(self):
        cur, conn = db_connect()
        cur.execute("DELETE FROM meal_plan_recipes")
        cur.execute("DELETE FROM meal_plans")
        cur.execute("DELETE FROM users")
        db_disconnect(cur, conn)

    def test_create_user(self):
        repo = SQLUserRepository()
        user = User(id=None, username='Spongebob Squarepants', email='spongebob@squarepants.com', password_hash=b'password1')

        created_user = repo.create_user(user)

        self.assertIsNotNone(created_user.id)
        self.assertEqual(created_user.username, 'Spongebob Squarepants')
        self.assertEqual(created_user.email, 'spongebob@squarepants.com')

    def test_del_user(self):
        repo = SQLUserRepository()
        user = User(id=None, username='Sheldon Plankton', email='sheldon@plankton.com', password_hash=b'password2')
        created_user = repo.create_user(user)

        repo.del_user(created_user.id)

        found_user = repo.get_user_by_id(created_user.id)

        self.assertIsNone(found_user)

    def test_get_user_by_id(self):
        repo = SQLUserRepository()
        user = User(id=None, username='Patrick Star', email='patrick@star.com', password_hash=b'password3')
        created_user = repo.create_user(user)

        found_user = repo.get_user_by_id(created_user.id)

        self.assertIsNotNone(found_user)
        self.assertEqual(found_user.username, 'Patrick Star')
        self.assertEqual(found_user.email, 'patrick@star.com')

    def test_get_user_by_username(self):
        repo = SQLUserRepository()
        user = User(id=None, username='Squidward Tentacles', email='squidward@tentacles.com', password_hash=b'password4')
        created_user = repo.create_user(user)

        found_user = repo.get_user_by_username(created_user.username)

        self.assertIsNotNone(found_user)
        self.assertEqual(found_user.username, 'Squidward Tentacles')
        self.assertEqual(found_user.email, 'squidward@tentacles.com')

    def test_user_login_success(self):
        repo = SQLUserRepository()
        password_hash = User.hash_password('password5')
        user = User(id=None, username='Sandy Cheeks', email='sandy@cheeks.com', password_hash=password_hash)
        created_user = repo.create_user(user)

        logged_in_user = repo.user_login('Sandy Cheeks', 'password5')

        self.assertIsNotNone(logged_in_user)
        self.assertEqual(logged_in_user.username, 'Sandy Cheeks')
        self.assertEqual(logged_in_user.email, 'sandy@cheeks.com')

    def test_user_login_wrong_password(self):
        repo = SQLUserRepository()
        password_hash = User.hash_password('password6')
        user = User(id=None, username='Eugene Krabs', email='eugene@krabs.com', password_hash=password_hash)
        repo.create_user(user)

        logged_in_user = repo.user_login('Eugene Krabs', 'wrongpassword')

        self.assertIsNone(logged_in_user)

    def test_user_login_nonexistent_user(self):
        repo = SQLUserRepository()

        logged_in_user = repo.user_login('Bubble Bass', 'password7')

        self.assertIsNone(logged_in_user)

    def test_create_meal_plan(self):
        user_repo = SQLUserRepository()
        password_hash = User.hash_password('password8')
        user = User(id=None, username='Mermaid Man', email='mermaid@man.com', password_hash=password_hash)
        created_user = user_repo.create_user(user)

        meal_plan = MealPlan(id=None, plans={})
        created_meal_plan = user_repo.create_meal_plan(created_user.id, meal_plan)

        self.assertIsNotNone(created_meal_plan.id)
        self.assertIsInstance(created_meal_plan.plans, dict)

    def test_get_meal_plan_by_id(self):
        user_repo = SQLUserRepository()
        password_hash = User.hash_password('password9')
        user = User(id=None, username='Pearl', email='pearl@krabs.com', password_hash=password_hash)
        created_user = user_repo.create_user(user)

        meal_plan = MealPlan(id=None, plans={})
        created_meal_plan = user_repo.create_meal_plan(created_user.id, meal_plan)

        found_meal_plan = user_repo.get_meal_plan_by_id(created_meal_plan.id)

        self.assertIsNotNone(found_meal_plan)
        self.assertEqual(found_meal_plan.id, created_meal_plan.id)

    def test_get_meal_plans_by_user(self):
        user_repo = SQLUserRepository()
        password_hash = User.hash_password('password10')
        user = User(id=None, username='Mrs Puff', email='mrs@puff.com', password_hash=password_hash)
        created_user = user_repo.create_user(user)

        meal_plan1 = MealPlan(id=None, plans={})
        meal_plan2 = MealPlan(id=None, plans={})
        user_repo.create_meal_plan(created_user.id, meal_plan1)
        user_repo.create_meal_plan(created_user.id, meal_plan2)

        user_meal_plans = user_repo.get_meal_plans_by_user(created_user.id)

        self.assertIsInstance(user_meal_plans, list)
        self.assertEqual(len(user_meal_plans), 2)

    def test_update_meal_plan(self):
        user_repo = SQLUserRepository()
        recipe_repo = SQLRecipeRepository()
        ingredient_repo = SQLIngredientRepository()

        password_hash = User.hash_password('password11')
        user = User(id=None, username='Larry', email='larry@lobster.com', password_hash=password_hash)
        created_user = user_repo.create_user(user)

        recipe1 = Recipe(id=None, title='Krabby Patty', instructions='Cook patty. Assemble sandwich', user_id=None, cook_time=15, username='SpongeBob')
        recipe2 = Recipe(id=None, title='Kelp Shake', instructions='Blend ingredients', user_id=None, cook_time=5, username='SpongeBob')
        created_recipe1 = recipe_repo.create_recipe(recipe1, [], ingredient_repo)
        created_recipe2 = recipe_repo.create_recipe(recipe2, [], ingredient_repo)

        meal_plan = MealPlan(id=None, plans={})
        created_meal_plan = user_repo.create_meal_plan(created_user.id, meal_plan)

        meal_plan_data = {
            "2026-03-22": {"breakfast": created_recipe1.id, "lunch": created_recipe2.id},
            "2026-03-23": {"breakfast": created_recipe1.id}
        }

        updated_meal_plan = user_repo.update_meal_plan(created_user.id, created_meal_plan.id, meal_plan_data)

        self.assertIsNotNone(updated_meal_plan)
        self.assertEqual(updated_meal_plan.id, created_meal_plan.id)

        cur, conn = db_connect()
        cur.execute(
            "SELECT COUNT(*) FROM meal_plan_recipes WHERE meal_plan_id = %s",
            (created_meal_plan.id,)
        )
        count = cur.fetchone()[0]
        db_disconnect(cur, conn)

        self.assertEqual(count, 3)

    def test_del_meal_plan(self):
        user_repo = SQLUserRepository()
        password_hash = User.hash_password('password12')
        user = User(id=None, username='Neptune', email='neptune@sea.com', password_hash=password_hash)
        created_user = user_repo.create_user(user)

        meal_plan = MealPlan(id=None, plans={})
        created_meal_plan = user_repo.create_meal_plan(created_user.id, meal_plan)

        user_repo.del_meal_plan(created_user.id, created_meal_plan.id)

        found_meal_plan = user_repo.get_meal_plan_by_id(created_meal_plan.id)

        self.assertIsNone(found_meal_plan)

    def test_del_meal_plan_wrong_user(self):
        user_repo = SQLUserRepository()
        password_hash = User.hash_password('password123')
        user1 = User(id=None, username='Barnacle Boy', email='barnacle@boy.com', password_hash=password_hash)
        user2 = User(id=None, username='Flying Dutchman', email='flying@dutchman.com', password_hash=password_hash)
        created_user1 = user_repo.create_user(user1)
        created_user2 = user_repo.create_user(user2)

        meal_plan = MealPlan(id=None, plans={})
        created_meal_plan = user_repo.create_meal_plan(created_user1.id, meal_plan)

        user_repo.del_meal_plan(created_user2.id, created_meal_plan.id)

        found_meal_plan = user_repo.get_meal_plan_by_id(created_meal_plan.id)

        self.assertIsNotNone(found_meal_plan)


class TestSQLRecipeRepository(unittest.TestCase):

    def setUp(self):
        cur, conn = db_connect()
        cur.execute("DELETE FROM recipe_ingredients")
        cur.execute("DELETE FROM recipes")
        cur.execute("DELETE FROM ingredients")
        db_disconnect(cur, conn)

    def test_create_recipe(self):
        recipe_repo = SQLRecipeRepository()
        ingredient_repo = SQLIngredientRepository()

        recipe = Recipe(id=None, title='Krabby Patty', instructions='Cook patty. Assemble sandwich', user_id=None, cook_time=15, username='SpongeBob')
        ingredients = []

        created_recipe = recipe_repo.create_recipe(recipe, ingredients, ingredient_repo)

        self.assertIsNotNone(created_recipe.id)
        self.assertEqual(created_recipe.title, 'Krabby Patty')
        self.assertEqual(created_recipe.instructions, 'Cook patty. Assemble sandwich')
        self.assertEqual(created_recipe.cook_time, 15)

    def test_create_recipe_with_ingredients(self):
        recipe_repo = SQLRecipeRepository()
        ingredient_repo = SQLIngredientRepository()

        recipe = Recipe(id=None, title='Krabby Patty Deluxe', instructions='Cook patty. Add toppings. Assemble', user_id=None, cook_time=20, username='SpongeBob')

        ingredients = [
            {"name": "Bun", "quantity": 2, "unit": "pieces"},
            {"name": "Patty", "quantity": 1, "unit": "piece"},
            {"name": "Lettuce", "quantity": 2, "unit": "leaves"}
        ]

        created_recipe = recipe_repo.create_recipe(recipe, ingredients, ingredient_repo)

        self.assertIsNotNone(created_recipe.id)
        self.assertEqual(created_recipe.title, 'Krabby Patty Deluxe')

        cur, conn = db_connect()
        cur.execute(
            "SELECT COUNT(*) FROM recipe_ingredients WHERE recipe_id = %s",
            (created_recipe.id,)
        )
        count = cur.fetchone()[0]
        db_disconnect(cur, conn)

        self.assertEqual(count, 3)

    def test_update_recipe(self):
        recipe_repo = SQLRecipeRepository()
        ingredient_repo = SQLIngredientRepository()

        recipe = Recipe(id=None, title='Krabby Patty', instructions='Cook patty. Assemble sandwich', user_id=None, cook_time=15, username='SpongeBob')
        created_recipe = recipe_repo.create_recipe(recipe, [], ingredient_repo)

        patty = ingredient_repo.create_ingredient(Ingredient(id=None, name='Patty'))
        bun = ingredient_repo.create_ingredient(Ingredient(id=None, name='Bun'))

        recipe_repo.add_ingredient(created_recipe, patty, value=1, measurement='piece')
        recipe_repo.add_ingredient(created_recipe, bun, value=2, measurement='pieces')

        class RecipeData:
            title = 'Krabby Patty Deluxe'
            instructions = 'Cook patty. Add lettuce. Assemble sandwich'
            cook_time = 20
            ingredients = [
                {"name": "Patty", "quantity": 1, "unit": "piece"},
                {"name": "Bun", "quantity": 2, "unit": "pieces"},
                {"name": "Lettuce", "quantity": 2, "unit": "leaves"},
            ]

        updated_recipe = recipe_repo.update_recipe(created_recipe.id, RecipeData(), ingredient_repo)

        self.assertEqual(updated_recipe.title, 'Krabby Patty Deluxe')
        self.assertEqual(updated_recipe.instructions, 'Cook patty. Add lettuce. Assemble sandwich')
        self.assertEqual(updated_recipe.cook_time, 20)
        self.assertEqual(len(updated_recipe.ingredients), 3)

        ingredient_names = [ing['name'] for ing in updated_recipe.ingredients]
        self.assertIn('Patty', ingredient_names)
        self.assertIn('Bun', ingredient_names)
        self.assertIn('Lettuce', ingredient_names)

    def test_del_recipe(self):
        recipe_repo = SQLRecipeRepository()
        ingredient_repo = SQLIngredientRepository()

        recipe = Recipe(id=None, title='Kelp Shake', instructions='Blend ingredients', user_id=None, cook_time=5, username='SpongeBob')
        created_recipe = recipe_repo.create_recipe(recipe, [], ingredient_repo)

        recipe_repo.del_recipe(created_recipe.id)

        found_recipe = recipe_repo.get_recipe_by_id(created_recipe.id)
        self.assertIsNone(found_recipe)

    def test_list_recipes(self):
        recipe_repo = SQLRecipeRepository()
        ingredient_repo = SQLIngredientRepository()

        recipe1 = Recipe(id=None, title='Chum Bucket Special', instructions='Mix chum', user_id=None, cook_time=10, username='SpongeBob')
        created_recipe1 = recipe_repo.create_recipe(recipe1, [], ingredient_repo)

        ingredient1 = ingredient_repo.create_ingredient(Ingredient(id=None, name='Chum'))
        recipe_repo.add_ingredient(created_recipe1, ingredient1, value=1, measurement='cup')

        recipe2 = Recipe(id=None, title='Coral Bits', instructions='Fry coral', user_id=None, cook_time=20, username='SpongeBob')
        created_recipe2 = recipe_repo.create_recipe(recipe2, [], ingredient_repo)

        ingredient2 = ingredient_repo.create_ingredient(Ingredient(id=None, name='Coral'))
        recipe_repo.add_ingredient(created_recipe2, ingredient2, value=2, measurement='pieces')

        all_recipes = recipe_repo.list_recipes()

        self.assertIsInstance(all_recipes, list)
        self.assertEqual(len(all_recipes), 2)

        for recipe in all_recipes:
            self.assertIsInstance(recipe.ingredients, list)
            self.assertEqual(len(recipe.ingredients), 1)

        recipe_titles_and_ingredients = {r.title: r.ingredients[0]['name'] for r in all_recipes}
        self.assertEqual(recipe_titles_and_ingredients['Chum Bucket Special'], 'Chum')
        self.assertEqual(recipe_titles_and_ingredients['Coral Bits'], 'Coral')

    def test_get_recipe_by_title(self):
        recipe_repo = SQLRecipeRepository()
        ingredient_repo = SQLIngredientRepository()

        recipe = Recipe(id=None, title='Krabby Fries', instructions='Fry potatoes', user_id=None, cook_time=15, username='SpongeBob')
        created_recipe = recipe_repo.create_recipe(recipe, [], ingredient_repo)

        potato = ingredient_repo.create_ingredient(Ingredient(id=None, name='Potato'))
        recipe_repo.add_ingredient(created_recipe, potato, value=5, measurement='pieces')

        found_recipe = recipe_repo.get_recipe_by_title('Krabby Fries')

        self.assertIsNotNone(found_recipe)
        self.assertEqual(found_recipe.title, 'Krabby Fries')
        self.assertEqual(found_recipe.instructions, 'Fry potatoes')
        self.assertEqual(found_recipe.cook_time, 15)

        self.assertEqual(len(found_recipe.ingredients), 1)
        self.assertEqual(found_recipe.ingredients[0]['name'], 'Potato')
        self.assertEqual(found_recipe.ingredients[0]['quantity'], '5 pieces')

    def test_get_recipe_by_id(self):
        recipe_repo = SQLRecipeRepository()
        ingredient_repo = SQLIngredientRepository()

        recipe = Recipe(id=None, title='Pretty Patty', instructions='Cook pretty patty. Assemble sandwich', user_id=None, cook_time=15, username='SpongeBob')
        created_recipe = recipe_repo.create_recipe(recipe, [], ingredient_repo)

        lettuce = ingredient_repo.create_ingredient(Ingredient(id=None, name='Lettuce'))
        tomato = ingredient_repo.create_ingredient(Ingredient(id=None, name='Tomato'))
        recipe_repo.add_ingredient(created_recipe, lettuce, value=2, measurement='cups')
        recipe_repo.add_ingredient(created_recipe, tomato, value=1, measurement='whole')

        found_recipe = recipe_repo.get_recipe_by_id(created_recipe.id)

        self.assertIsNotNone(found_recipe)
        self.assertEqual(found_recipe.title, 'Pretty Patty')
        self.assertEqual(found_recipe.instructions, 'Cook pretty patty. Assemble sandwich')
        self.assertEqual(found_recipe.cook_time, 15)

        self.assertEqual(len(found_recipe.ingredients), 2)
        ingredient_names = [ing['name'] for ing in found_recipe.ingredients]
        self.assertIn('Lettuce', ingredient_names)
        self.assertIn('Tomato', ingredient_names)

    def test_list_six_recipes(self):
        recipe_repo = SQLRecipeRepository()
        ingredient_repo = SQLIngredientRepository()

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

        for i, (title, instructions, cook_time) in enumerate(recipes):
            recipe = Recipe(id=None, title=title, instructions=instructions, user_id=None, cook_time=cook_time, username='SpongeBob')
            created_recipe = recipe_repo.create_recipe(recipe, [], ingredient_repo)

            ingredient = ingredient_repo.create_ingredient(Ingredient(id=None, name=f'Ingredient {i}'))
            recipe_repo.add_ingredient(created_recipe, ingredient, value=1, measurement='cup')

        latest_recipes = recipe_repo.list_six_recipes()

        self.assertIsInstance(latest_recipes, list)
        self.assertEqual(len(latest_recipes), 6)
        self.assertEqual(latest_recipes[0].title, 'Kelp Shake')
        self.assertEqual(latest_recipes[1].title, 'Bran Flakes')

        for recipe in latest_recipes:
            self.assertIsInstance(recipe.ingredients, list)
            self.assertEqual(len(recipe.ingredients), 1)

    def test_get_random_recipe(self):
        recipe_repo = SQLRecipeRepository()
        ingredient_repo = SQLIngredientRepository()

        recipe = Recipe(id=None, title='Random Recipe', instructions='Random', user_id=None, cook_time=10, username='SpongeBob')
        created_recipe = recipe_repo.create_recipe(recipe, [], ingredient_repo)

        ingredient = ingredient_repo.create_ingredient(Ingredient(id=None, name='Random Ingredient'))
        recipe_repo.add_ingredient(created_recipe, ingredient, value=3, measurement='tbsp')

        random_recipe = recipe_repo.get_random_recipe()

        self.assertIsNotNone(random_recipe)
        self.assertEqual(random_recipe.title, 'Random Recipe')

        self.assertEqual(len(random_recipe.ingredients), 1)
        self.assertEqual(random_recipe.ingredients[0]['name'], 'Random Ingredient')
        self.assertEqual(random_recipe.ingredients[0]['quantity'], '3 tbsp')

    def test_list_recipes_by_user_id(self):
        recipe_repo = SQLRecipeRepository()
        ingredient_repo = SQLIngredientRepository()
        user_repo = SQLUserRepository()

        user1 = User(id=None, username='SpongeBob', email='spongebob@bb.com', password_hash=b'password')
        user2 = User(id=None, username='Patrick', email='patrick@star.com', password_hash=b'password')
        created_user1 = user_repo.create_user(user1)
        created_user2 = user_repo.create_user(user2)

        recipe1 = Recipe(id=None, title='Krabby Patty', instructions='Cook', user_id=created_user1.id, cook_time=10, username='SpongeBob')
        recipe2 = Recipe(id=None, title='Kelp Shake', instructions='Blend', user_id=created_user1.id, cook_time=5, username='SpongeBob')
        recipe_repo.create_recipe(recipe1, [], ingredient_repo)
        recipe_repo.create_recipe(recipe2, [], ingredient_repo)

        recipe3 = Recipe(id=None, title='Chum', instructions='Mix', user_id=created_user2.id, cook_time=3, username='SpongeBob')
        recipe_repo.create_recipe(recipe3, [], ingredient_repo)

        user1_recipes = recipe_repo.list_recipes_by_user_id(created_user1.id)

        self.assertEqual(len(user1_recipes), 2)
        titles = [r.title for r in user1_recipes]
        self.assertIn('Krabby Patty', titles)
        self.assertIn('Kelp Shake', titles)
        self.assertNotIn('Chum', titles)

    def test_list_recipes_by_user_id_empty(self):
        recipe_repo = SQLRecipeRepository()
        user_repo = SQLUserRepository()

        user = User(id=None, username='Squidward', email='squidward@tent.com', password_hash=b'password')
        created_user = user_repo.create_user(user)

        recipes = recipe_repo.list_recipes_by_user_id(created_user.id)

        self.assertEqual(len(recipes), 0)
        self.assertIsInstance(recipes, list)

    def test_add_ingredient(self):
        recipe_repo = SQLRecipeRepository()
        ingredient_repo = SQLIngredientRepository()

        recipe = Recipe(id=None, title='Krabby Patty', instructions='Cook patty. Assemble sandwich', user_id=None, cook_time=15, username='SpongeBob')
        created_recipe = recipe_repo.create_recipe(recipe, [], ingredient_repo)

        ingredient = Ingredient(id=None, name='Pickles')
        created_ingredient = ingredient_repo.create_ingredient(ingredient)

        recipe_repo.add_ingredient(created_recipe, created_ingredient, value=2, measurement='slices')

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

        recipe = Recipe(id=None, title='Krabby Patty', instructions='Cook patty. Assemble sandwich', user_id=None, cook_time=15, username='SpongeBob')
        created_recipe = recipe_repo.create_recipe(recipe, [], ingredient_repo)

        ingredient = Ingredient(id=None, name='Pickles')
        created_ingredient = ingredient_repo.create_ingredient(ingredient)

        recipe_repo.add_ingredient(created_recipe, created_ingredient, value=2, measurement='slices')

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

        recipe = Recipe(id=None, title='Krabby Patty', instructions='Cook patty. Assemble sandwich', user_id=None, cook_time=15, username='SpongeBob')
        created_recipe = recipe_repo.create_recipe(recipe, [], ingredient_repo)

        ingredient = Ingredient(id=None, name='Pickles')
        created_ingredient = ingredient_repo.create_ingredient(ingredient)

        recipe_repo.add_ingredient_by_id(created_recipe.id, created_ingredient.id, value=2, measurement='slices')

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

        recipe = Recipe(id=None, title='Krabby Patty', instructions='Cook patty. Assemble sandwich', user_id=None, cook_time=15, username='SpongeBob')
        created_recipe = recipe_repo.create_recipe(recipe, [], ingredient_repo)

        ingredient = Ingredient(id=None, name='Pickles')
        created_ingredient = ingredient_repo.create_ingredient(ingredient)

        recipe_repo.add_ingredient_by_id(created_recipe.id, created_ingredient.id, value=2, measurement='slices')

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
        cur.execute("DELETE FROM recipe_ingredients")
        cur.execute("DELETE FROM ingredients")
        db_disconnect(cur, conn)

    def test_create_ingredient(self):
        repo = SQLIngredientRepository()
        ingredient = Ingredient(id=None, name='Kelp')

        created_ingredient = repo.create_ingredient(ingredient)

        self.assertIsNotNone(created_ingredient.id)
        self.assertEqual(created_ingredient.name, 'Kelp')

    def test_create_ingredient_duplicate_returns_existing(self):
        repo = SQLIngredientRepository()
        ingredient1 = Ingredient(id=None, name='Salt')
        ingredient2 = Ingredient(id=None, name='Salt')

        created_ingredient1 = repo.create_ingredient(ingredient1)
        created_ingredient2 = repo.create_ingredient(ingredient2)

        self.assertEqual(created_ingredient1.id, created_ingredient2.id)
        self.assertEqual(created_ingredient1.name, created_ingredient2.name)

    def test_del_ingredient(self):
        repo = SQLIngredientRepository()
        ingredient = Ingredient(id=None, name='Chum')
        created_ingredient = repo.create_ingredient(ingredient)

        repo.del_ingredient(created_ingredient)

        found_ingredient = repo.get_ingredient_by_id(created_ingredient.id)

        self.assertIsNone(found_ingredient)

    def test_get_ingredient_by_id(self):
        repo = SQLIngredientRepository()
        ingredient = Ingredient(id=None, name='Potato')
        created_ingredient = repo.create_ingredient(ingredient)

        found_ingredient = repo.get_ingredient_by_id(created_ingredient.id)

        self.assertIsNotNone(found_ingredient)
        self.assertEqual(found_ingredient.name, 'Potato')

    def test_list_ingredients(self):
        repo = SQLIngredientRepository()
        ingredient1 = Ingredient(id=None, name='Kelp')
        ingredient2 = Ingredient(id=None, name='Chum')
        ingredient3 = Ingredient(id=None, name='Potato')

        repo.create_ingredient(ingredient1)
        repo.create_ingredient(ingredient2)
        repo.create_ingredient(ingredient3)

        ingredients = repo.list_ingredients()

        self.assertIsInstance(ingredients, list)
        self.assertEqual(len(ingredients), 3)


if __name__ == '__main__':
    unittest.main()