import os
from dotenv import load_dotenv
from abc import ABC, abstractmethod
from cryptography.fernet import Fernet

load_dotenv()
key = os.getenv('ENC_DEC_KEY')
cipher = Fernet(key)

class User():
    def __init__(self, id, username, email, password):
        self.id = id
        self.username = username
        self.email = email
        self.password = cipher.encrypt(password.encode())

class Ingredient():
    def __init__(self, id, name):
        self.id = id
        self.name = name

class Recipe():
    def __init__(self, id, title, instructions):
        self.id = id
        self.title = title
        self.instructions = instructions

class RecipeRepository(ABC):

    @abstractmethod
    def create_user():
        pass
    
    @abstractmethod
    def del_user():
        pass

    @abstractmethod
    def create_recipe():
        pass

    @abstractmethod
    def del_recipe():
        pass

    @abstractmethod
    def add_recipe():
        pass

    @abstractmethod
    def add_ingredient():
        pass

class TestRepository(RecipeRepository):
    def __init__(self):
        self.users = []
        self.recipes = []
        self.ingredients = []

    def create_user(self, username):
        self.users.append(username)
    
    def del_user(self, username):
        self.users.remove(username)

    def create_recipe(self):
        pass

    def del_recipe(self):
        pass

    def add_recipe(self):
        pass

    def add_ingredient(self):
        pass