import psycopg2
from repo import User, Recipe, Ingredient, UserRepository, RecipeRepository, IngredientRepository

def db_connect():
    conn = psycopg2.connect(dbname='test', user='postgres', password=None) 
    cur = conn.cursor()
    return cur, conn

def db_disconnect(cur, conn):
    conn.commit() 
    cur.close() 
    conn.close()

class SQLUserRepository(UserRepository):

    def create_user(self, user: User) -> User:
        pass
    
    def del_user(self, user_id: int) -> None:
        pass

    def get_user_by_id(self, username: str) -> User | None:
        pass

    def get_user_by_username(self, username: str) -> User | None:
        pass

class SQLRecipeRepository(RecipeRepository):

    def create_recipe(self, recipe: Recipe) -> Recipe:
        pass

    def del_recipe(self, recipe_id: int) -> None:
        pass

    def list_recipes(self) -> list[Recipe]:
        pass

    def get_recipe_by_title(self, title: str) -> Recipe | None:
        pass

    def add_ingredient(self, recipe: Recipe, ingredient: Ingredient) -> None:
        pass

    def remove_ingredient(self, recipe: Recipe, ingredient: Ingredient) -> None:
        pass

class SQLIngredientRepository(IngredientRepository):

    def create_ingredient(self, ingredient: Ingredient) -> Ingredient:
        pass

    def del_ingredient(self, ingredient: Ingredient) -> None:
        pass

    def list_ingredients(self) -> list[Ingredient]:
        pass