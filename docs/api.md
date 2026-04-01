# Overview #

The MealMind API provides basic CRUD operations for managing user accounts, ingredients, recipes, and meal plans.

# Authentication #

This API does not require authentication. All endpoints are publicly accessible and can be called without API keys, tokens, or user accounts.

## Required Headers ##

No authentication headers are required. The only header you need is:
	
    Content-Type: application/json

Example Request

    curl -X 'POST' \
    'http://127.0.0.1:8000/api/user/register' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{
    "username": "string",
    "email": "string",
    "password": "string"
    }'

# Endpoints #

## User Endpoints ##

### POST /api/user/register ###

Creates a User account with username, password, and email address

Example Parameter

    {
    "username": "string",
    "email": "string",
    "password": "string"
    }

Response Body

    {
    "id": 101,
    "username": "string",
    "email": "string"
    }

### POST /api/user/login ###

Generates an authentication token for successful login attempts

Example Parameter

    {
    "username": "string",
    "password": "string"
    }

Response Body

    {
    "id": 101,
    "username": "string"
    }

### GET /api/user/logout ###

Eliminates the authentication token until another successful login is achieved

Example Parameter

	JWT authentication token

Response Body

    "logged out"

### GET /api/user/id ###

Retrieve user account data from the database using an ID number

Example Parameter

	JWT authentication token

Response Body

    {
    "id": 101,
    "username": "string"
    }

## Recipe Endpoints ##

### POST /api/recipe ###

Creates a recipe with a title, suggested cook time, instructions, and required ingredients

Example Parameter

    {
    "title": "string",
    "instructions": "string",
    "cook_time": 0,
    "ingredients": [
        {
        "name": "string",
        "quantity": 0,
        "unit": "string"
        }
    ]
    }

Response Body

    {
    "id": 101,
    "title": "string",
    "cook_time": 0,
    "instructions": "string",
    "ingredients": [
        {
        "id": 101,
        "name": "string",
        "quantity": 0,
        "unit": "string"
        }
    ]
    }

### GET /api/recipe ###

Retrieves recipes from the database by title

Example Parameter

	Recipe title input as string, i.e. “string”

Response Body

    {
    "id": 101,
    "title": "string",
    "cook_time": 0,
    "instructions": "string",
    "ingredients": [
        {
        "id": 101,
        "name": "string",
        "quantity": 0,
        "unit": "string"
        }
    ]
    }

### GET /api/recipe/{id} ###

Retrieves recipes from the database by ID number

Example Parameter

	Recipe ID number integer, i.e. 101

Response Body

    {
    "id": 101,
    "title": "string",
    "cook_time": 0,
    "instructions": "string",
    "ingredients": [
        {
        "id": 101,
        "name": "string",
        "quantity": 0,
        "unit": "string"
        }
    ]
    }

### PUT /api/recipe/{id} ###

Updates recipe details on the database requiring authentication and recipe authorship

Example Parameter

    Recipe ID number integer, i.e. 101

    {
    "title": "stringUPDATE",
    "instructions": "stringUPDATE",
    "cook_time": 0,
    "ingredients": [
        {
        "name": "stringUPDATE",
        "quantity": 10,
        "unit": "stringUPDATE"
        }
    ]
    }

Response Body

    {
    "id": 101,
    "title": "stringUPDATE",
    "cook_time": 0,
    "instructions": "stringUPDATE",
    "ingredients": [
        {
        "id": 102,
        "name": "stringUPDATE",
        "quantity": "stringUPDATE",
        "unit": "stringUPDATE"
        }
    ]
    }

### DELETE /api/recipe/{id} ###

Deletes a recipe from the database by ID number

Example Parameter

	Recipe ID number integer, i.e. 101

Response Body

	true

### GET /api/user/recipes ###

Retrieves all recipes from the database that authenticated user created

Example Parameter

    JWT authentication token

Response Body

    [
    {
        "id": 101,
        "title": "string",
        "cook_time": 0,
        "instructions": "string",
        "ingredients": [
        {
            "id": 101,
            "name": "string",
            "quantity": 0,
            "unit": "string"
        }
        ]
    }
    ]

### GET /api/recipe_list ###

Retrieves a list of all recipes present on the database

Example Parameter

	None

Response Body

    [
    {
        "id": 1,
        "title": "World's Best Pancakes",
        "cook_time": 50,
        "instructions": "Heat a pan with a little oil, then add your ingredients and cook until they’re golden and fragrant. Season to taste, let everything simmer briefly so the flavors come together, and serve warm.",
        "ingredients": [
        {
            "id": 67,
            "name": "tomato paste",
            "quantity": 2,
            "unit": "liter"
        },
        {
            "id": 84,
            "name": "peanut butter",
            "quantity": 2,
            "unit": "quart"
        },
        {
            "id": 40,
            "name": "carrots",
            "quantity": 2,
            "unit": "pinch"
        },
        {
            "id": 34,
            "name": "lentils",
            "quantity": 2,
            "unit": "pint"
        }
        ]
    }
    ]

### GET /api/recipe_reel ###

Retrieves a sample list of six recipes from all recipes on the database for suggestion purposes

Example Parameter

	None

Response Body

    [
    {
        "id": 59,
        "title": "World's Best Alfredo Sauce",
        "cook_time": 20,
        "instructions": "Heat a pan with a little oil, then add your ingredients and cook until they’re golden and fragrant. Season to taste, let everything simmer briefly so the flavors come together, and serve warm.",
        "ingredients": [
        {
            "id": 67,
            "name": "tomato paste",
            "quantity": 2,
            "unit": "liter"
        },
        {
            "id": 84,
            "name": "peanut butter",
            "quantity": 2,
            "unit": "quart"
        },
        {
            "id": 40,
            "name": "carrots",
            "quantity": 2,
            "unit": "pinch"
        },
        {
            "id": 34,
            "name": "lentils",
            "quantity": 2,
            "unit": "pint"
        }
        ]
    },
    {
        "id": 31,
        "title": "World's Best Sushi Rolls",
        "cook_time": 20,
        "instructions": "Heat a pan with a little oil, then add your ingredients and cook until they’re golden and fragrant. Season to taste, let everything simmer briefly so the flavors come together, and serve warm.",
        "ingredients": [
        {
            "id": 67,
            "name": "tomato paste",
            "quantity": 2,
            "unit": "liter"
        },
        {
            "id": 84,
            "name": "peanut butter",
            "quantity": 2,
            "unit": "quart"
        },
        {
            "id": 40,
            "name": "carrots",
            "quantity": 2,
            "unit": "pinch"
        },
        {
            "id": 34,
            "name": "lentils",
            "quantity": 2,
            "unit": "pint"
        }
        ]
    },
    {
        "id": 91,
        "title": "World's Best Steak Marinade",
        "cook_time": 50,
        "instructions": "Heat a pan with a little oil, then add your ingredients and cook until they’re golden and fragrant. Season to taste, let everything simmer briefly so the flavors come together, and serve warm.",
        "ingredients": [
        {
            "id": 67,
            "name": "tomato paste",
            "quantity": 2,
            "unit": "liter"
        },
        {
            "id": 84,
            "name": "peanut butter",
            "quantity": 2,
            "unit": "quart"
        },
        {
            "id": 40,
            "name": "carrots",
            "quantity": 2,
            "unit": "pinch"
        },
        {
            "id": 34,
            "name": "lentils",
            "quantity": 2,
            "unit": "pint"
        }
        ]
    },
    {
        "id": 44,
        "title": "World's Best Shepherd's Pie",
        "cook_time": 50,
        "instructions": "Heat a pan with a little oil, then add your ingredients and cook until they’re golden and fragrant. Season to taste, let everything simmer briefly so the flavors come together, and serve warm.",
        "ingredients": [
        {
            "id": 67,
            "name": "tomato paste",
            "quantity": 2,
            "unit": "liter"
        },
        {
            "id": 84,
            "name": "peanut butter",
            "quantity": 2,
            "unit": "quart"
        },
        {
            "id": 40,
            "name": "carrots",
            "quantity": 2,
            "unit": "pinch"
        },
        {
            "id": 34,
            "name": "lentils",
            "quantity": 2,
            "unit": "pint"
        }
        ]
    },
    {
        "id": 86,
        "title": "World's Best Spinach Dip",
        "cook_time": 120,
        "instructions": "Heat a pan with a little oil, then add your ingredients and cook until they’re golden and fragrant. Season to taste, let everything simmer briefly so the flavors come together, and serve warm.",
        "ingredients": [
        {
            "id": 67,
            "name": "tomato paste",
            "quantity": 2,
            "unit": "liter"
        },
        {
            "id": 84,
            "name": "peanut butter",
            "quantity": 2,
            "unit": "quart"
        },
        {
            "id": 40,
            "name": "carrots",
            "quantity": 2,
            "unit": "pinch"
        },
        {
            "id": 34,
            "name": "lentils",
            "quantity": 2,
            "unit": "pint"
        }
        ]
    },
    {
        "id": 74,
        "title": "World's Best Bolognese",
        "cook_time": 30,
        "instructions": "Heat a pan with a little oil, then add your ingredients and cook until they’re golden and fragrant. Season to taste, let everything simmer briefly so the flavors come together, and serve warm.",
        "ingredients": [
        {
            "id": 67,
            "name": "tomato paste",
            "quantity": 2,
            "unit": "liter"
        },
        {
            "id": 84,
            "name": "peanut butter",
            "quantity": 2,
            "unit": "quart"
        },
        {
            "id": 40,
            "name": "carrots",
            "quantity": 2,
            "unit": "pinch"
        },
        {
            "id": 34,
            "name": "lentils",
            "quantity": 2,
            "unit": "pint"
        }
        ]
    }
    ]

### GET /api/recipe_random ###

Retrieves a single random recipe from the database for suggestion purposes

Example Parameter

	None

Response Body

    {
    "id": 26,
    "title": "World's Best Burgers",
    "cook_time": 30,
    "instructions": "Heat a pan with a little oil, then add your ingredients and cook until they’re golden and fragrant. Season to taste, let everything simmer briefly so the flavors come together, and serve warm.",
    "ingredients": [
        {
        "id": 67,
        "name": "tomato paste",
        "quantity": 2,
        "unit": "liter"
        },
        {
        "id": 84,
        "name": "peanut butter",
        "quantity": 2,
        "unit": "quart"
        },
        {
        "id": 40,
        "name": "carrots",
        "quantity": 2,
        "unit": "pinch"
        },
        {
        "id": 34,
        "name": "lentils",
        "quantity": 2,
        "unit": "pint"
        }
    ]
    }

## Meal Plan Endpoints ##

### POST /api/meal_plan ###

Creates a meal plan with date and recipe slots assigned recipe ID numbers

Example Parameter

    {
    "plans": {
        "date1": {
        "slot1": 10,
        "slot2": 20,
        "slot3": 30
        },
        "date2": {
        "slot1": 10,
        "slot2": 20,
        "slot3": 30
        },
        "date3": {
        "slot1": 10,
        "slot2": 20,
        "slot3": 30
        }
    }
    }

Response Body

    {
    "id": 1,
    "plans": {
        "date1": {
        "slot1": 10,
        "slot2": 20,
        "slot3": 30
        },
        "date2": {
        "slot1": 10,
        "slot2": 20,
        "slot3": 30
        },
        "date3": {
        "slot1": 10,
        "slot2": 20,
        "slot3": 30
        }
    }
    }

### GET /api/meal_plan/{id} ###

Retrieves a meal plan from the database by ID number

Example Parameter

    Meal Plan ID number integer, i.e. 1

Response Body

    {
    "date1": {
        "slot1": 10,
        "slot2": 20,
        "slot3": 30
    },
    "date2": {
        "slot1": 10,
        "slot2": 20,
        "slot3": 30
    },
    "date3": {
        "slot1": 10,
        "slot2": 20,
        "slot3": 30
    }
    }

### POST /api/meal_plan/{id} ###

Updates an already existing meal plan in the database

Example Parameter

    Meal Plan ID number integer, i.e. 1

    {
    "plans": {
        "additionalProp1": {
        "additionalProp1": 0,
        "additionalProp2": 0,
        "additionalProp3": 0
        },
        "additionalProp2": {
        "additionalProp1": 0,
        "additionalProp2": 0,
        "additionalProp3": 0
        },
        "additionalProp3": {
        "additionalProp1": 0,
        "additionalProp2": 0,
        "additionalProp3": 0
        }
    }
    }

Response Body

    {
    "id": 1,
    "plans": {
        "plans": {
        "additionalProp1": {
            "additionalProp1": 0,
            "additionalProp2": 0,
            "additionalProp3": 0
        },
        "additionalProp2": {
            "additionalProp1": 0,
            "additionalProp2": 0,
            "additionalProp3": 0
        },
        "additionalProp3": {
            "additionalProp1": 0,
            "additionalProp2": 0,
            "additionalProp3": 0
        }
        }
    }
    }

### DELETE /api/meal_plan/{id} ###

Deletes a meal plan from the database by ID number

Example Parameter

	Meal Plan ID number integer, i.e. 1

Response Body

    null

### GET /api/meal_plan ###

Retrieves a meal plan from the database by ID number

Example Parameter

	Meal Plan ID number integer, i.e. 1

Response Body

    {
    "additionalProp1": {
        "additionalProp1": 0,
        "additionalProp2": 0,
        "additionalProp3": 0
    },
    "additionalProp2": {
        "additionalProp1": 0,
        "additionalProp2": 0,
        "additionalProp3": 0
    },
    "additionalProp3": {
        "additionalProp1": 0,
        "additionalProp2": 0,
        "additionalProp3": 0
    }
    }

## Ingredient Endpoints ##

### POST /api/ingredient ###

Creates an ingredient on the database with a name, quantity, and unit of measurement

Example Parameter

    {
    "name": "string",
    "quantity": 0,
    "unit": "string"
    }

Response Body

    {
    "id": 101,
    "name": "string"
    }

### GET /api/ingredient ###

Retrieves an ingredient from the database by name

Example Parameter

    Ingredient name input as string, i.e. “string”

Response Body

    {
    "ingredients": [
        "string"
    ]
    }

### DELETE /api/ingredient/{id} ###

Deletes an ingredient from the database by ID number

Example Parameter

    Ingredient ID number integer, i.e. 101

Response Body

    {
    "ok": true
    }
