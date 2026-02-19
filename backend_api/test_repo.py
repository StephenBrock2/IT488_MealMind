from repo import User, Recipe, Ingredient, UserRepository, RecipeRepository, IngredientRepository

class Test_UserRepository(UserRepository):
    def __init__(self):
        self.users = {}
        self.next_id = 1

    def create_user(self, user: User) -> User:
        for i in self.users.values():
            if i.username == user.username:
                return None
        
        user.id = self.next_id
        self.users[self.next_id] = user
        self.next_id += 1
        return user
    
    def del_user(self, user_id: int) -> None:
        pass

    def get_user_by_username(self, user_name: str) -> User | None:
        for user in self.users.values():
            if user.username == user_name:
                return user.username

        return None

class Test_RecipeRepository(RecipeRepository):
    def __init__(self):
        self.recipes = {}
        self.next_id = 1

    def create_recipe(self, recipe: Recipe) -> Recipe:
        recipe.id = self.next_id
        self.recipes[self.next_id] = recipe
        self.next_id += 1
        return recipe

    def del_recipe(self, recipe_id: int) -> None:
        pass

    def list_recipes(self) -> list[Recipe]:
        pass

class Test_IngredientRepository(IngredientRepository):
    def __init__(self):
        self.ingredients = {}
        self.next_id = 1

    def add_ingredient(self, ingredient: Ingredient) -> Ingredient:
        for i in self.ingredients.values():
            if i.name == ingredient.name:
                return i

        ingredient.id = self.next_id
        self.ingredients[self.next_id] = ingredient
        self.next_id += 1
        return ingredient

    def list_ingredients(self) -> list[Ingredient]:
        pass