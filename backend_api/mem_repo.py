from repo import User, Recipe, Ingredient, UserRepository, RecipeRepository, IngredientRepository

def mem_user_seed():
    pass

def mem_recipe_seed():
    pass

def mem_ingredient_seed():
    pass

class MemUserRepository(UserRepository):
    def __init__(self):
        self.users = {}
        self.next_id = 1

    def create_user(self, user: User) -> User:
        for i in self.users.values():
            if i.username == user.username:
                return i
        
        user.id = self.next_id
        self.users[self.next_id] = user
        self.next_id += 1
        return user
    
    def del_user(self, user_id: int) -> None:
        if user_id in self.users.values():
            self.users.pop(user_id)
        else:
            return None
        
    def get_user_by_id(self, user_id: int) -> User | None:
        for id in self.users.values():
            if id.id == user_id:
                return id.username
        return None

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
        recipe_list = []
        for i in self.recipes.values():
            recipe_data = {"id": i.id, "title": i.title, "instructions": i.instructions, "ingredients": i.ingredients}
            recipe_list.append(recipe_data)
        return recipe_list

    def get_recipe_by_title(self, title: str) -> Recipe | None:
        for i in self.recipes.values():
            if i.title == title:
                return i
            else:
                return None
            
    def get_recipe_by_id(self, recipe_id: int) -> Recipe | None:
        if recipe_id in self.recipes.keys():
            recipe = self.recipes[recipe_id]
            return recipe
        else:
            return None

    def add_ingredient(self, recipe: Recipe, ingredient: Ingredient, value: int, measurement: str) -> Recipe:
        if ingredient in recipe.ingredients:
            recipe.ingredients.pop(ingredient)
        recipe.ingredients.append({
            "name": ingredient.name, 
            "quantity": value, 
            "unit": measurement}
            )
        return recipe

    def remove_ingredient(self, recipe: Recipe, ingredient: Ingredient) -> None:
        if ingredient in recipe.ingredients.keys():
                recipe.ingredients.pop(ingredient)
        else:
            return None

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
        if ingredient_id in self.ingredients.keys():
            self.ingredients.pop(ingredient_id)
        else:
            return None

    def list_ingredients(self) -> list[Ingredient]:
        ingredient_list = []
        for i in self.ingredients.values():
            ingredient_list.append(i.name)
        return ingredient_list
    
'''
repo = MemRecipeRepository()
in_repo = MemIngredientRepository()

test_recipe = Recipe(None, "World's Best Meatloaf", "How to make meatloaf: ", 80)
repo.create_recipe(test_recipe)

beef = Ingredient(None, 'Ground Beef')
onion = Ingredient(None, 'Onion')
oil = Ingredient(None, 'Olive Oil')
eggs = Ingredient(None, 'Eggs')
garlic = Ingredient(None, 'Garlic Cloves')
ketchup = Ingredient(None, 'Ketchup')
parsley = Ingredient(None, 'Parsley')
crumbs = Ingredient(None, 'Panko Bread Crumbs')
milk = Ingredient(None, 'Milk')
salt = Ingredient(None, 'Salt')
seasoning = Ingredient(None, 'Italian Seasoning')
pepper = Ingredient(None, 'Black Pepper')

in_repo.create_ingredient(beef)
in_repo.create_ingredient(onion)
in_repo.create_ingredient(oil)
in_repo.create_ingredient(eggs)
in_repo.create_ingredient(garlic)
in_repo.create_ingredient(ketchup)
in_repo.create_ingredient(parsley)
in_repo.create_ingredient(crumbs)
in_repo.create_ingredient(milk)
in_repo.create_ingredient(salt)
in_repo.create_ingredient(seasoning)
in_repo.create_ingredient(pepper)

repo.add_ingredient(test_recipe, beef, 2, 'lbs')
repo.add_ingredient(test_recipe, onion, 1, 'cup')
repo.add_ingredient(test_recipe, oil, 1, 'tsp')
repo.add_ingredient(test_recipe, eggs, 2, 'large')
repo.add_ingredient(test_recipe, garlic, 3, 'cloves')
repo.add_ingredient(test_recipe, ketchup, 2, 'tbsp')
repo.add_ingredient(test_recipe, parsley, 3, 'tbsp')
repo.add_ingredient(test_recipe, crumbs, 3/4, 'cup')
repo.add_ingredient(test_recipe, milk, 1/3, 'cup')
repo.add_ingredient(test_recipe, salt, 1, 'tsp')
repo.add_ingredient(test_recipe, seasoning, 1, 'tsp')
repo.add_ingredient(test_recipe, pepper, 1/2, 'tsp')

print(repo.list_recipes())
print(in_repo.list_ingredients())
'''