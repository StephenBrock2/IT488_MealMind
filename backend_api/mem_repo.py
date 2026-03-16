from repo import User, Recipe, Ingredient, MealPlan, UserRepository, RecipeRepository, IngredientRepository
import random

class MemUserRepository(UserRepository):
    def __init__(self):
        self.users = {}
        self.next_id = 1
        self.user_tokens = []

        self.meal_plans = {}
        self.next_meal_id = 1

        self.pantries = {}
        self.next_pantry_id = 1

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
    
    def get_all_users(self):
        user_list = []
        for i in self.users.values():
            user_data = {"id": i.id, "name": i.username, "email": i.email, "password": isinstance(i.password_hash, bytes)}
            user_list.append(user_data)
        return user_list

    def user_login(username: str, password: str) -> User | None:
        pass

    def create_meal_plan(self, meal_plan: MealPlan) -> MealPlan:
        self.mealplans[meal_plan.id] = meal_plan
        return self.meal_plans[self.meal_plan.id]

    def get_meal_plan_by_id(self, meal_plan_id: int) -> MealPlan | None:
        for meal_plan in self.meal_plans.keys():
            if meal_plan == meal_plan_id:
                meal_plan_data = self.meal_plans[meal_plan].plans
                return meal_plan_data
            else:
                return None

    def del_meal_plan(self, meal_plan_id: int) -> None:
        if meal_plan_id in self.meal_plans.keys():
            self.meal_plans.pop(meal_plan_id)
        return None

    def add_recipe_to_meal_plan(self, meal_plan_id: int, meal_slot: str, recipe_id: int) -> MealPlan:
            self.meal_plans[meal_plan_id].plans[meal_slot] == recipe_id
            meal_plan_data = self.meal_plans[meal_plan_id].plans
            return meal_plan_data

    def remove_recipe_from_meal_plan(self, meal_plan_id: int, recipe_id: int) -> None:
        for meal_plan in self.meal_plans.keys():
            if meal_plan == meal_plan_id:
                for recipe in self.meal_plans[meal_plan].plans.values():
                    if recipe == recipe_id:
                        self.meal_plans[meal_plan].plans.pop(recipe)
                    return self.meal_plans[meal_plan_id]
        else:
            return None

class MemIngredientRepository(IngredientRepository):
    def __init__(self):
        self.ingredients = {}
        self.next_id = 1

    def create_ingredient(self, ingredient: Ingredient) -> Ingredient:
        for i in self.ingredients.values():
            if i.name.lower() == ingredient.name.lower():
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

    def get_ingredient_by_id(self, ingredient_id: int) -> Ingredient | None:
        if ingredient_id in self.ingredients.keys():
            ingredient = self.ingredients[ingredient_id]
            return ingredient
        else:
            return None

    def list_ingredients(self) -> list[Ingredient]:
        ingredient_list = []
        for i in self.ingredients.values():
            ingredient_list.append(i.name)
        return ingredient_list

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
        for id in self.recipes.keys():
            if recipe_id == id:
                self.recipes.pop(id)
                return True
        else:
            return None

    def list_recipes(self) -> list[Recipe]:
        recipe_list = []
        for i in self.recipes.values():
            recipe_data = {"id": i.id, "title": i.title, "cook_time": i.cook_time, "instructions": i.instructions, "ingredients": i.ingredients}
            recipe_list.append(recipe_data)
        return recipe_list
    
    def list_six_recipes(self) -> list:
        recipe_list = []
        for i in range(1, 7):
            recipe = random.choice(list(self.recipes.values()))
            recipe_data = {"id": recipe.id, "title": recipe.title, "cook_time": recipe.cook_time, "instructions": recipe.instructions, "ingredients": recipe.ingredients}
            recipe_list.append(recipe_data)
        return recipe_list

    def get_random_recipe(self) -> Recipe:
        recipe = random.choice(list(self.recipes.values()))
        return recipe

    def get_recipe_by_title(self, title: str) -> Recipe | None:
        title = f"{title}"
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
        for n, i in enumerate(recipe.ingredients):
            if i["name"] == ingredient.name:
                recipe.ingredients[n] = {
                    "id": ingredient.id,
                    "name": ingredient.name, 
                    "quantity": value, 
                    "unit": measurement
                    }
                break
        else:
            recipe.ingredients.append({
                "id": ingredient.id,
                "name": ingredient.name, 
                "quantity": value, 
                "unit": measurement}
                )
        return recipe

    def remove_ingredient(self, recipe: Recipe, ingredient: Ingredient) -> None:
        for i in recipe.ingredients:
            if i["name"] == ingredient.name:
                recipe.ingredients.remove(i)
                break
        else:
            return None
        
    def add_ingredient_by_id(self, recipe_id: int, ingredient_id: int, value: int, measurement: str, repo: MemIngredientRepository) -> Recipe:
        recipe = self.get_recipe_by_id(recipe_id)
        ingredient = repo.get_ingredient_by_id(ingredient_id)
        for n, i in enumerate(recipe.ingredients):
            if i["id"] == ingredient.id:
                recipe.ingredients[n] = {
                    "id": ingredient.id,
                    "name": ingredient.name, 
                    "quantity": value, 
                    "unit": measurement
                    }
                break
        else:
            recipe.ingredients.append({
                "id": ingredient.id,
                "name": ingredient.name, 
                "quantity": value, 
                "unit": measurement}
                )
        return recipe

    def remove_ingredient_by_id(self, recipe_id: int, ingredient_id: int) -> None:
        recipe = self.get_recipe_by_id(recipe_id)
        for n, i in enumerate(recipe.ingredients):
            if i["id"] == ingredient_id:
                recipe.ingredients.pop(n)
                break
        else:
            return None
   
def mem_user_repo_seed():
    user_repo = MemUserRepository()
    password = User.hash_password('1234')
    for i in range(1, 101):
        user = User(id=None, username=f'User{i}', email=f'user{i}@email.com', password_hash=password, password_salt=None)
        user_repo.create_user(user)
    return user_repo

def mem_recipe_repo_seed(ingredient_repo):
    recipe_repo = MemRecipeRepository()
    recipes = [
    "Pancakes",
    "Chocolate Chip Cookies",
    "Lasagna",
    "Chicken Soup",
    "Beef Stew",
    "Grilled Cheese",
    "Garlic Bread",
    "Mac and Cheese",
    "Chili",
    "Banana Bread",
    "Brownies",
    "Fried Rice",
    "Tacos",
    "Guacamole",
    "Mashed Potatoes",
    "Roast Chicken",
    "Meatballs",
    "Spaghetti",
    "Omelette",
    "French Toast",
    "Waffles",
    "Caesar Salad",
    "Potato Salad",
    "Coleslaw",
    "BBQ Ribs",
    "Burgers",
    "Veggie Burger",
    "Stir Fry",
    "Curry",
    "Pad Thai",
    "Sushi Rolls",
    "Pizza Dough",
    "Tomato Soup",
    "Lentil Soup",
    "Chicken Alfredo",
    "Shrimp Scampi",
    "Fish Tacos",
    "Quesadillas",
    "Nachos",
    "Hummus",
    "Falafel",
    "Baked Salmon",
    "Stuffed Peppers",
    "Shepherd's Pie",
    "Enchiladas",
    "Burrito",
    "Chicken Wings",
    "Sloppy Joes",
    "Meatloaf",
    "Cornbread",
    "Muffins",
    "Apple Pie",
    "Cheesecake",
    "Lemon Bars",
    "Cupcakes",
    "Smoothie",
    "Salad Dressing",
    "Marinara Sauce",
    "Alfredo Sauce",
    "Pesto",
    "Salsa",
    "Hot Chocolate",
    "Iced Coffee",
    "Chicken Tenders",
    "Fried Chicken",
    "Potato Soup",
    "Clam Chowder",
    "Risotto",
    "Paella",
    "Gnocchi",
    "Fajitas",
    "Curry Noodles",
    "Ramen Bowl",
    "Bolognese",
    "Tiramisu",
    "Chocolate Cake",
    "Carrot Cake",
    "Granola",
    "Energy Bars",
    "Chicken Salad",
    "Tuna Salad",
    "Veggie Stir Fry",
    "Roasted Vegetables",
    "Bruschetta",
    "Deviled Eggs",
    "Spinach Dip",
    "Artichoke Dip",
    "Curry Chicken Salad",
    "Shrimp Tacos",
    "Pork Chops",
    "Steak Marinade",
    "Baked Ziti",
    "French Fries",
    "Onion Rings",
    "Pancake Syrup",
    "Hot Wings",
    "Chocolate Mousse",
    "Fruit Salad",
    "Breakfast Burrito",
    "Chicken Pot Pie"
    ]
    instructions = 'Heat a pan with a little oil, then add your ingredients and cook until they’re golden and fragrant. Season to taste, let everything simmer briefly so the flavors come together, and serve warm.'
    cook_times = [10, 15, 20, 30, 45, 50, 60, 90, 120]
    measurements  = [
    "teaspoon",
    "tablespoon",
    "cup",
    "pint",
    "quart",
    "gallon",
    "milliliter",
    "liter",
    "gram",
    "kilogram",
    "ounce",
    "pound",
    "dash",
    "pinch",
    "slice"
    ]
    for i in recipes:
        recipe_repo.create_recipe(recipe = Recipe(None, title=f"World's Best {i}", instructions= instructions, cook_time=random.choice(cook_times)))
    for recipe in recipe_repo.recipes:
        for n in range(random.randint(1, 10)):
            recipe_repo.add_ingredient_by_id(recipe_id=recipe, ingredient_id=random.choice(list(ingredient_repo.ingredients.keys())), value=random.randint(1, 5), measurement=random.choice(measurements), repo=ingredient_repo)

    return recipe_repo

def mem_ingredient_repo_seed():
    ingredient_repo = MemIngredientRepository()
    ingredients = [
    "salt",
    "black pepper",
    "olive oil",
    "butter",
    "garlic",
    "onion",
    "tomato",
    "basil",
    "oregano",
    "thyme",
    "rosemary",
    "parsley",
    "cilantro",
    "ginger",
    "soy sauce",
    "vinegar",
    "lemon juice",
    "lime juice",
    "chicken broth",
    "beef broth",
    "vegetable broth",
    "flour",
    "sugar",
    "brown sugar",
    "honey",
    "maple syrup",
    "milk",
    "cream",
    "yogurt",
    "eggs",
    "rice",
    "pasta",
    "quinoa",
    "lentils",
    "black beans",
    "kidney beans",
    "chickpeas",
    "potatoes",
    "sweet potatoes",
    "carrots",
    "celery",
    "bell pepper",
    "mushrooms",
    "spinach",
    "kale",
    "cabbage",
    "corn",
    "peas",
    "green beans",
    "cumin",
    "paprika",
    "turmeric",
    "curry powder",
    "chili powder",
    "cayenne pepper",
    "nutmeg",
    "cinnamon",
    "cloves",
    "cardamom",
    "bay leaves",
    "mustard",
    "ketchup",
    "mayonnaise",
    "fish sauce",
    "sesame oil",
    "coconut milk",
    "tomato paste",
    "crushed tomatoes",
    "ground beef",
    "chicken breast",
    "pork loin",
    "salmon",
    "shrimp",
    "tofu",
    "tempeh",
    "parmesan cheese",
    "cheddar cheese",
    "mozzarella",
    "feta cheese",
    "bread crumbs",
    "yeast",
    "baking powder",
    "baking soda",
    "peanut butter",
    "almonds",
    "walnuts",
    "cashews",
    "raisins",
    "dried cranberries",
    "olive",
    "capers",
    "anchovies",
    "hot sauce",
    "salsa",
    "tortillas",
    "bacon",
    "sausage",
    "herbes de Provence",
    "five-spice powder",
    "saffron"
    ]

    for i in ingredients:
        ingredient_repo.create_ingredient(ingredient = Ingredient(None, i))

    return ingredient_repo

def mem_repo_startup():
    ingredient_repo = mem_ingredient_repo_seed()
    recipe_repo = mem_recipe_repo_seed(ingredient_repo)
    user_repo = mem_user_repo_seed()

    return ingredient_repo, recipe_repo, user_repo