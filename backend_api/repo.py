from abc import ABC, abstractmethod
import bcrypt as bc

class User():
    def __init__(self, id, username, email, password_hash):
        self.id = id
        self.username = username
        self.email = email
        self.password = password_hash

    @staticmethod
    def hash_password(password: str) -> bytes:
        return bc.hashpw(password.encode(), bc.gensalt())
    
    def verify_password(self, password: str) -> bool:
        return bc.checkpw(password.encode(), self.password)

class Ingredient():
    def __init__(self, id, name):
        self.id = id
        self.name = name

class Recipe():
    def __init__(self, id, title, instructions):
        self.id = id
        self.title = title
        self.instructions = instructions
        self.ingredients = {}

class UserRepository(ABC):

    @abstractmethod
    def create_user(self, user: User) -> User:
        pass
    
    @abstractmethod
    def del_user(self, user_id: int) -> None:
        pass

    @abstractmethod
    def get_user_by_username(self, username: str) -> User | None:
        pass

class RecipeRepository(ABC):

    @abstractmethod
    def create_recipe(self, recipe: Recipe) -> Recipe:
        pass

    @abstractmethod
    def del_recipe(self, recipe_id: int) -> None:
        pass

    @abstractmethod
    def list_recipes(self) -> list[Recipe]:
        pass

    @abstractmethod
    def add_ingredient(self, recipe: Recipe, ingredient: Ingredient) -> Ingredient:
        pass

    @abstractmethod
    def remove_ingredient(self, recipe: Recipe, ingredient: Ingredient) -> Ingredient:
        pass

class IngredientRepository(ABC):

    @abstractmethod
    def create_ingredient(self, ingredient: Ingredient) -> Ingredient:
        pass

    @abstractmethod
    def del_ingredient(self, ingredient: Ingredient) -> None:
        pass

    @abstractmethod
    def list_ingredients(self) -> list[Ingredient]:
        pass