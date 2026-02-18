from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship, DeclarativeBase


class Base(DeclarativeBase):
    pass


class RecipeIngredient(Base):
    __tablename__ = 'recipe_ingredients'

    recipe_id = Column(Integer, ForeignKey('recipes.id'), primary_key=True)
    ingredient_id = Column(Integer, ForeignKey('ingredients.id'), primary_key=True)
    quantity = Column(String(50))
    recipe = relationship("Recipe", back_populates="items")
    ingredient = relationship("Ingredient", back_populates="used_in")


class Recipe(Base):
    __tablename__ = 'recipes'

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    instructions = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    items = relationship("RecipeIngredient", back_populates="recipe")
    owner = relationship("User", back_populates="recipes")


class Ingredient(Base):
    __tablename__ = 'ingredients'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    used_in = relationship("RecipeIngredient", back_populates="ingredient")


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    recipes = relationship("Recipe", back_populates="owner")
