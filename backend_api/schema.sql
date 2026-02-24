DROP TABLE IF EXISTS recipe_ingredients;
DROP TABLE IF EXISTS recipes;
DROP TABLE IF EXISTS ingredients;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL
);

CREATE TABLE ingredients (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE recipes (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    instructions TEXT NOT NULL,
    user_id INTEGER REFERENCES users(id)
);

CREATE TABLE recipe_ingredients (
    recipe_id INTEGER REFERENCES recipes(id),
    ingredient_id INTEGER REFERENCES ingredients(id),
    quantity VARCHAR(50) NOT NULL,
    PRIMARY KEY (recipe_id, ingredient_id)
);
