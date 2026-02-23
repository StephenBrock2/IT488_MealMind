from repo import User, Recipe, Ingredient, UserRepository, RecipeRepository, IngredientRepository

class MemUserRepository(UserRepository):
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
        if user_id in self.users.values():
            self.users.pop(user_id)
        else:
            return None
        
    def get_user_by_id(self, username: str) -> User | None:
        pass

    def get_user_by_username(self, user_name: str) -> User | None:
        for user in self.users.values():
            if user.username == user_name:
                return user.username
        return None

class MemRecipeRepository(RecipeRepository):
    def __init__(self):
        self.recipes = {}
        self.next_id = 1

    def create_recipe(self, recipe: Recipe) -> Recipe:
        recipe.id = self.next_id
        self.recipes[self.next_id] = recipe
        self.next_id += 1
        return recipe

    def del_recipe(self, recipe_id: int) -> None:
        if recipe_id in self.recipes.values():
            self.users.pop(recipe_id)
        else:
            return None

    def list_recipes(self) -> list[Recipe]:
        pass

    def get_recipe_by_title(self, title: str) -> Recipe | None:
        pass

    def add_ingredient(self, recipe: Recipe, ingredient: Ingredient) -> Ingredient:
        pass

    def remove_ingredient(self, recipe: Recipe, ingredient: Ingredient) -> None:
        pass

class MemIngredientRepository(IngredientRepository):
    def __init__(self):
        self.ingredients = {}
        self.next_id = 1

    def create_ingredient(self, ingredient: Ingredient) -> Ingredient:
        for i in self.ingredients.values():
            if i.name == ingredient.name:
                return i

        ingredient.id = self.next_id
        self.ingredients[self.next_id] = ingredient
        self.next_id += 1
        return ingredient
    
    def del_ingredient(self, ingredient_id: int) -> None:
        if ingredient_id in self.ingredients.values():
            self.ingredients.pop(ingredient_id)
        else:
            return None

    def list_ingredients(self) -> list[Ingredient]:
        pass