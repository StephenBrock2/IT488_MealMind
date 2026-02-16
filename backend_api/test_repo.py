from repo import User, Recipe, Ingredient, UserRepository, RecipeRepository, IngredientRepository

class Test_UserRepository(UserRepository):
    def __init__(self):
        self.users = {}

    def create_user(self, user: User) -> User:
        pass
    
    def del_user(self, user_id: int) -> None:
        pass

    def get_user_by_username(self, username: str) -> User | None:
        pass

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

    def add_ingredient(self, ingredient: Ingredient) -> Ingredient:
        pass

    def list_ingredients(self) -> list[Ingredient]:
        pass


repo_recipe = Test_RecipeRepository()

test_recipe = Recipe(1, 'Delicious Recipe', 'How to make it?')
repo_recipe.create_recipe(test_recipe)

recipe = repo_recipe.recipes[1]

print(recipe.title, recipe.instructions)