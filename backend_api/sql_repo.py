import os
import psycopg2
from dotenv import load_dotenv
from repo import User, Recipe, Ingredient, MealPlan, UserRepository, RecipeRepository, IngredientRepository

load_dotenv()

def db_connect():
    DATABASE_URL = os.getenv("DATABASE_URL")
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    return cur, conn

def db_disconnect(cur, conn):
    conn.commit() 
    cur.close() 
    conn.close()

def init_db():
    cur, conn = db_connect()
    with open("schema.sql", "r") as schema:
        cur.execute(schema.read())
    db_disconnect(cur, conn)

class SQLUserRepository(UserRepository):

    def create_user(self, user: User) -> User:
        cur, conn = db_connect()

        try:
            cur.execute(
                "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s) RETURNING id",
                (user.username, user.email, user.password_hash.decode('utf-8'))
            )

            user.id = cur.fetchone()[0]
            db_disconnect(cur, conn)
            return user

        except psycopg2.IntegrityError:
            db_disconnect(cur, conn)
            return None

    def del_user(self, user_id: int) -> None:
        cur, conn = db_connect()

        cur.execute(
            "DELETE FROM users WHERE id = %s",
            (user_id,)
        )

        db_disconnect(cur, conn)

    def get_user_by_id(self, user_id: int) -> User | None:
        cur, conn = db_connect()

        cur.execute(
            "SELECT id, username, email, password_hash FROM users WHERE id = %s",
            (user_id,)
        )

        row = cur.fetchone()
        db_disconnect(cur, conn)

        if row:
            return User(id=row[0], username=row[1], email=row[2], password_hash=row[3])
        return None

    def get_user_by_username(self, username: str) -> User | None:
        cur, conn = db_connect()

        cur.execute(
            "SELECT id, username, email, password_hash FROM users WHERE username = %s",
            (username,)
        )

        row = cur.fetchone()
        db_disconnect(cur, conn)

        if row:
            return User(id=row[0], username=row[1], email=row[2], password_hash=row[3])
        return None
    
    def user_login(self, username: str, password: str) -> User | None:
        cur, conn = db_connect()

        cur.execute(
            "SELECT id, username, email, password_hash FROM users WHERE username = %s",
            (username,)
        )

        row = cur.fetchone()
        db_disconnect(cur, conn)

        if not row:
            return None

        user = User(id=row[0], username=row[1], email=row[2], password_hash=row[3].encode())

        if user.verify_password(password):
            return user
        return None

    def create_meal_plan(self, user_id: int, meal_plan: MealPlan) -> MealPlan:
        cur, conn = db_connect()

        cur.execute(
            "INSERT INTO meal_plans (user_id) VALUES (%s) RETURNING id",
            (user_id,)
        )

        meal_plan.id = cur.fetchone()[0]
        db_disconnect(cur, conn)
        return meal_plan

    def get_meal_plan_by_id(self, meal_plan_id: int) -> MealPlan | None:
        cur, conn = db_connect()

        cur.execute(
            "SELECT id, user_id FROM meal_plans WHERE id = %s",
            (meal_plan_id,)
        )

        row = cur.fetchone()
        db_disconnect(cur, conn)

        if row:
            return MealPlan(id=row[0], plans={})
        return None
    
    def get_mealplans_by_user(self, user_id: int) -> MealPlan | None:
        pass

    def del_meal_plan(self, meal_plan_id: int) -> None:
        cur, conn = db_connect()
        cur.execute(
            "DELETE FROM meal_plans WHERE id = %s",
            (meal_plan_id,)
        )

        db_disconnect(cur, conn)

    # Might be unecessary / Temporarily removed from repo
    def add_recipe_to_meal_plan(self, meal_plan_id: int, recipe_id: int) -> MealPlan:
        pass

    # Might be unecessary / Temporarily removed from repo
    def remove_recipe_from_meal_plan(self, meal_plan_id: int, recipe_id: int) -> None:
        pass

class SQLRecipeRepository(RecipeRepository):

    def create_recipe(self, recipe: Recipe) -> Recipe:
        cur, conn = db_connect()

        cur.execute(
            "INSERT INTO recipes (title, instructions, user_id, cook_time) VALUES (%s, %s, %s, %s) RETURNING id",
            (recipe.title, recipe.instructions, recipe.user_id, recipe.cook_time)
        )
        recipe.id = cur.fetchone()[0]
        db_disconnect(cur, conn)
        return recipe

    def del_recipe(self, recipe_id: int) -> None:
        cur, conn = db_connect()

        cur.execute(
            "DELETE FROM recipes WHERE id = %s",
            (recipe_id,)
        )

        db_disconnect(cur, conn)

    def list_recipes(self) -> list[Recipe]:
        cur, conn = db_connect()

        cur.execute(
            "SELECT id, title, instructions, user_id, cook_time FROM recipes ORDER BY id"
        )
        rows = cur.fetchall()
        db_disconnect(cur, conn)

        recipes = []
        for row in rows:
            recipe = Recipe(id=row[0], title=row[1], instructions=row[2], cook_time=row[4])
            recipes.append(recipe)

        return recipes
    
    def list_six_recipes(self) -> list:
        cur, conn = db_connect()
        cur.execute("SELECT * FROM recipes ORDER BY id DESC LIMIT 6")
        rows = cur.fetchall()
        db_disconnect(cur, conn)

        recipes = []
        for row in rows:
            recipe = Recipe(id=row[0], title=row[1], instructions=row[2], user_id=row[3], cook_time=row[4])
            recipes.append(recipe)

        return recipes

    def get_random_recipe(self) -> Recipe | None:
        cur, conn = db_connect()
        cur.execute("SELECT * FROM recipes ORDER BY RANDOM() LIMIT 1")
        row = cur.fetchone()
        db_disconnect(cur, conn)

        if row:
            return Recipe(id=row[0], title=row[1], instructions=row[2], user_id=row[3], cook_time=row[4])
        return None

    def get_recipe_by_title(self, title: str) -> Recipe | None:
        cur, conn = db_connect()

        cur.execute(
            "SELECT id, title, instructions, user_id, cook_time FROM recipes WHERE title = %s",
            (title,)
        )

        row = cur.fetchone()
        db_disconnect(cur, conn)
        if row:
            return Recipe(id=row[0], title=row[1], instructions=row[2], cook_time=row[4])
        return None
    
    def get_recipe_by_id(self, recipe_id: int) -> Recipe | None:
        cur, conn = db_connect()

        cur.execute(
            "SELECT id, title, instructions, user_id, cook_time FROM recipes WHERE id = %s",
            (recipe_id,)
        )

        row = cur.fetchone()
        db_disconnect(cur, conn)
        if row:
            return Recipe(id=row[0], title=row[1], instructions=row[2], cook_time=row[4])
        return None

    def add_ingredient(self, recipe: Recipe, ingredient: Ingredient, value: float, measurement: str) -> None:
        cur, conn = db_connect()
        quantity = f"{value} {measurement}"
        cur.execute(
            "INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity) VALUES (%s, %s, %s)",
            (recipe.id, ingredient.id, quantity)
        )
        db_disconnect(cur, conn)

    def remove_ingredient(self, recipe: Recipe, ingredient: Ingredient) -> None:
        cur, conn = db_connect()

        cur.execute(
            "DELETE FROM recipe_ingredients WHERE recipe_id = %s AND ingredient_id = %s",
            (recipe.id, ingredient.id)
        )

        db_disconnect(cur, conn)

    def add_ingredient_by_id(self, recipe_id: int, ingredient_id: int, value: float, measurement: str) -> None:
        cur, conn = db_connect()
        quantity = f"{value} {measurement}"
        cur.execute(
            "INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity) VALUES (%s, %s, %s)",
            (recipe_id, ingredient_id, quantity)
        )
        db_disconnect(cur, conn)

    def remove_ingredient_by_id(self, recipe_id: int, ingredient_id: int) -> None:
        cur,conn = db_connect()

        cur.execute(
            "DELETE FROM recipe_ingredients WHERE recipe_id = %s AND ingredient_id = %s",
            (recipe_id, ingredient_id)
        )

        db_disconnect(cur, conn)

class SQLIngredientRepository(IngredientRepository):

    def create_ingredient(self, ingredient: Ingredient) -> Ingredient:
        cur, conn = db_connect()

        cur.execute(
            "SELECT id, name FROM ingredients WHERE name = %s",
            (ingredient.name,)
        )

        row = cur.fetchone()

        if row:
            db_disconnect(cur, conn)
            return Ingredient(id=row[0], name=row[1])

        cur.execute(
            "INSERT INTO ingredients (name) VALUES (%s) RETURNING id",
            (ingredient.name,)
        )

        ingredient.id = cur.fetchone()[0]
        db_disconnect(cur, conn)
        return ingredient

    def del_ingredient(self, ingredient: Ingredient) -> None:
        cur, conn = db_connect()

        cur.execute(
            "DELETE FROM ingredients WHERE id = %s",
            (ingredient.id,)
        )

        db_disconnect(cur, conn)

    def get_ingredient_by_id(self, ingredient_id: int) -> Ingredient | None:
        cur, conn = db_connect()

        cur.execute(
            "SELECT id, name FROM ingredients WHERE id = %s",
            (ingredient_id,)
        )

        row = cur.fetchone()
        db_disconnect(cur, conn)
        if row:
            return Ingredient(id=row[0], name=row[1])
        return None

    def list_ingredients(self) -> list[Ingredient]:
        cur, conn = db_connect()

        cur.execute(
            "SELECT id, name FROM ingredients ORDER BY id"
        )

        rows = cur.fetchall()
        db_disconnect(cur, conn)

        ingredients = []
        for row in rows:
            ingredient = Ingredient(id=row[0], name=row[1])
            ingredients.append(ingredient)

        return ingredients