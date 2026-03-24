from abc import ABC, abstractmethod
import bcrypt as bc

class User():
    def __init__(self, id: int, username: str, email: str, password_hash: bytes, password_salt: bytes = None):
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.password_salt = password_salt
        self.login_state = False
        self.login_token = ''

        self.created_recipes = {}
        self.saved_recipes = {}
        self.meal_plans = {}
        self.pantry = {}

    @staticmethod
    def hash_password(password: str) -> bytes:
        return bc.hashpw(password.encode(), bc.gensalt())
    
    def verify_password(self, password: str) -> bool:
        return bc.checkpw(password.encode(), self.password_hash)

class Ingredient():
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name

class Recipe():
    def __init__(self, id: int, title: str, instructions: str, cook_time: int, user_id: int = None, username: str = None):
        self.id = id
        self.title = title
        self.cook_time = cook_time
        self.instructions = instructions
        self.user_id = user_id
        self.username = username
        self.ingredients = []

class MealPlan():
    def __init__(self, id: int, plans: dict):
        self.id = id
        self.plans = plans

class UserRepository(ABC):

    @abstractmethod
    def create_user(self, user: User) -> User:
        pass
    
    @abstractmethod
    def del_user(self, user_id: int) -> None:
        pass

    @abstractmethod
    def get_user_by_id(self, username: str) -> User | None:
        pass

    @abstractmethod
    def get_user_by_username(self, username: str) -> User | None:
        pass

    @abstractmethod
    def user_login(self, username: str, password: str) -> User | None:
        pass

    @abstractmethod
    def create_meal_plan(self, user_id: int, meal_plan: MealPlan) -> MealPlan:
        pass

    @abstractmethod
    def update_meal_plan(self, user_id: int, meal_plan_id: int, meal_plan_data: dict) -> MealPlan | None:
        pass

    @abstractmethod
    def get_meal_plan_by_id(self, meal_plan_id: int) -> MealPlan | None:
        pass

    @abstractmethod
    def get_meal_plans_by_user(self, user_id: int) -> list[MealPlan]:
        pass

    @abstractmethod
    def del_meal_plan(self, user_id: int, meal_plan_id: int) -> None:
        pass

    # Might be unecessary
    def add_recipe_to_meal_plan(self, user_id: int, meal_plan_id: int, recipe_id: int) -> User:
        pass
    
    # Might be unecessary
    def remove_recipe_from_meal_plan(self, user_id: int, meal_plan_id: int, recipe_id: int) -> None:
        pass

    def add_ingredient_to_pantry(self, user_id: int, pantry_id: int, ingredient_id: int) -> User:
        pass

    def remove_ingredient_from_pantry(self, user_id: int, pantry_id: int, ingredient_id: int) -> None:
        pass

    def del_pantry(self, user_id: int, pantry_id: int) -> None:
        pass

class IngredientRepository(ABC):

    @abstractmethod
    def create_ingredient(self, ingredient: Ingredient) -> Ingredient:
        pass

    @abstractmethod
    def del_ingredient(self, ingredient: Ingredient) -> None:
        pass

    @abstractmethod
    def get_ingredient_by_id(self, ingredient_id: int) -> Ingredient | None:
        pass

    @abstractmethod
    def list_ingredients(self) -> list[Ingredient]:
        pass

class RecipeRepository(ABC):

    @abstractmethod
    def create_recipe(self, recipe: Recipe) -> Recipe:
        pass

    @abstractmethod
    def create_recipe_2(self, recipe: Recipe, ingredients: list, ing_repo: IngredientRepository) -> Recipe:
        pass

    @abstractmethod
    def update_recipe(self, recipe_id: int, recipe_data: object, ing_repo: IngredientRepository) -> Recipe:
        pass

    @abstractmethod
    def del_recipe(self, recipe_id: int) -> None:
        pass

    @abstractmethod
    def list_recipes(self) -> list[Recipe]:
        pass

    @abstractmethod
    def list_six_recipes(self) -> list:
        pass

    @abstractmethod
    def get_random_recipe(self) -> Recipe | None:
        pass

    @abstractmethod
    def get_recipe_by_title(self, title: str) -> Recipe | None:
        pass

    @abstractmethod
    def get_recipe_by_id(self, id: int) -> Recipe | None:
        pass

    @abstractmethod
    def get_recipe_by_user_id(self, id: int) -> Recipe | None:
        pass

    @abstractmethod
    def add_ingredient(self, recipe: Recipe, ingredient: Ingredient, value: float, measurement: str) -> None:
        pass

    @abstractmethod
    def remove_ingredient(self, recipe: Recipe, ingredient: Ingredient) -> None:
        pass

    @abstractmethod
    def add_ingredient_by_id(self, recipe_id: int, ingredient_id: int, value: int, measurement: str, repo: IngredientRepository) -> Recipe:
        pass

    @abstractmethod
    def remove_ingredient_by_id(self, recipe_id: int, ingredient_id: int) -> None:
        pass