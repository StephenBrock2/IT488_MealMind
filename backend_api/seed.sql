-- Clear existing data
DELETE FROM recipe_ingredients;
DELETE FROM recipes;
DELETE FROM ingredients;

-- Reset sequences
ALTER SEQUENCE recipes_id_seq RESTART WITH 1;
ALTER SEQUENCE ingredients_id_seq RESTART WITH 1;

-- Insert Ingredients
INSERT INTO ingredients (name) VALUES
('Chicken Breast'),
('Olive Oil'),
('Garlic'),
('Lemon'),
('Salt'),
('Black Pepper'),
('Butter'),
('Onion'),
('Tomato'),
('Pasta'),
('Parmesan Cheese'),
('Basil'),
('Mozzarella Cheese'),
('Ground Beef'),
('Eggs'),
('Milk'),
('Flour'),
('Sugar'),
('Baking Powder'),
('Vanilla Extract'),
('Rice'),
('Soy Sauce'),
('Ginger'),
('Bell Pepper'),
('Broccoli'),
('Spinach'),
('Mushrooms'),
('Heavy Cream'),
('Cheddar Cheese'),
('Carrots'),
('Celery'),
('Chicken Stock'),
('Thyme'),
('Rosemary'),
('Chicken Thighs'),
('Coconut Milk'),
('Curry Powder'),
('Shrimp'),
('White Wine'),
('Salmon'),
('Penne Pasta'),
('Marinara Sauce'),
('Italian Sausage'),
('Feta Cheese'),
('Chickpeas'),
('Pork Chops'),
('Apple'),
('Sage'),
('Brown Sugar'),
('Taco Seasoning'),
('Sour Cream'),
('Salsa'),
('Tortillas'),
('Lime'),
('Avocado'),
('Cilantro'),
('Bacon'),
('Honey'),
('Balsamic Vinegar'),
('Bread'),
('Lettuce'),
('Mayo'),
('Mustard'),
('Red Onion');

-- 25 Recipes (no user_id)
INSERT INTO recipes (title, instructions, user_id, cook_time) VALUES
('Chicken Alfredo Made Simple', 'Pound chicken breasts thin. Dredge in flour, egg, then breadcrumbs. Pan-fry until golden. Top with marinara and mozzarella. Bake at 375°F for 15 minutes until cheese melts.', NULL, 35),
('Creamy Tuscan Chicken', 'Season chicken with salt and pepper. Sear in olive oil until golden. Remove chicken. Sauté garlic and sun-dried tomatoes. Add heavy cream, parmesan, and spinach. Simmer until thickened. Return chicken to pan.', NULL, 25),
('Garlic Butter Shrimp Pasta', 'Cook pasta according to package. Sauté shrimp in butter and garlic until pink. Add white wine and reduce. Toss with pasta, parmesan, and fresh parsley.', NULL, 20),
('Honey Garlic Salmon', 'Mix honey, soy sauce, and minced garlic. Brush on salmon fillets. Bake at 400°F for 12-15 minutes until flaky. Garnish with sesame seeds and green onions.', NULL, 15),
('Beef Tacos', 'Brown ground beef with taco seasoning. Warm tortillas. Fill with beef, lettuce, cheese, tomatoes, sour cream, and salsa. Serve with lime wedges.', NULL, 20),
('Chicken Stir-Fry', 'Cut chicken into strips. Stir-fry in hot oil with garlic and ginger. Add bell peppers, broccoli, and carrots. Toss with soy sauce mixture. Serve over rice.', NULL, 25),
('Creamy Pasta for Weeknights', 'Cook penne pasta. Mix with marinara, ricotta, and Italian sausage. Transfer to baking dish. Top with mozzarella. Bake at 375°F for 25 minutes.', NULL, 40),
('Chicken Caesar Salad', 'Grill seasoned chicken breast. Slice and serve over romaine lettuce with Caesar dressing, parmesan, and croutons.', NULL, 15),
('Mushroom Risotto', 'Sauté mushrooms and onions. Add arborio rice and toast. Gradually add warm chicken stock, stirring constantly. Finish with butter and parmesan.', NULL, 35),
('Lemon Herb Roasted Chicken', 'Rub whole chicken with olive oil, lemon, garlic, rosemary, and thyme. Roast at 425°F for 1 hour until golden and internal temp reaches 165°F.', NULL, 75),
('Thai Chicken Curry', 'Sauté chicken with curry paste. Add coconut milk, bell peppers, and bamboo shoots. Simmer until chicken is cooked. Serve over jasmine rice with fresh basil.', NULL, 30),
('Caprese Salad', 'Slice fresh mozzarella and tomatoes. Arrange alternating on plate. Drizzle with olive oil and balsamic vinegar. Top with fresh basil leaves and sea salt.', NULL, 10),
('Beef Stroganoff', 'Sauté beef strips until browned. Remove and cook mushrooms and onions. Add beef stock and sour cream. Return beef to pan. Serve over egg noodles.', NULL, 30),
('Vegetable Stir-Fry', 'Heat oil in wok. Stir-fry broccoli, bell peppers, carrots, and snap peas. Add garlic, ginger, and soy sauce. Toss until vegetables are tender-crisp.', NULL, 15),
('Chicken Fajitas', 'Marinate chicken strips in lime juice and spices. Sauté with bell peppers and onions. Serve in warm tortillas with guacamole, sour cream, and salsa.', NULL, 25),
('Spaghetti Carbonara', 'Cook spaghetti. Fry bacon until crispy. Whisk eggs with parmesan. Toss hot pasta with bacon, then egg mixture. Season with black pepper.', NULL, 20),
('Justin''s Famous Salad', 'Combine cucumbers, tomatoes, red onion, olives, and feta. Dress with olive oil, lemon juice, and oregano. Serve with pita bread.', NULL, 10),
('Pork Chops with Apples', 'Season pork chops and sear until golden. Remove and sauté sliced apples with butter and brown sugar. Return pork to pan and finish cooking.', NULL, 25),
('Minestrone Soup', 'Sauté onions, carrots, and celery. Add tomatoes, beans, pasta, and vegetable stock. Simmer until pasta is tender. Stir in spinach and serve with parmesan.', NULL, 35),
('Teriyaki Chicken Bowl', 'Marinate chicken in teriyaki sauce. Grill until cooked through. Serve over rice with steamed broccoli and sesame seeds.', NULL, 30),
('Classic Burger', 'Form ground beef into patties. Season with salt and pepper. Grill to desired doneness. Serve on toasted buns with lettuce, tomato, onion, and condiments.', NULL, 15),
('Chicken Quesadillas', 'Fill tortillas with shredded chicken, cheese, and peppers. Cook in skillet until golden and cheese melts. Cut into wedges and serve with salsa and sour cream.', NULL, 15),
('Pad Thai', 'Soak rice noodles. Stir-fry shrimp, scrambled eggs, and bean sprouts. Toss with noodles, fish sauce, tamarind, and peanuts. Garnish with lime and cilantro.', NULL, 25),
('BBQ Chicken Pizza', 'Spread BBQ sauce on pizza dough. Top with cooked chicken, red onion, cilantro, and mozzarella. Bake at 475°F until crust is golden.', NULL, 20),
('Berry Pancakes for Breakfast', 'Whisk together flour, sugar, baking powder, salt, eggs, and milk until smooth. Gently fold in fresh blueberries and strawberries. Heat griddle over medium heat and lightly butter. Pour 1/4 cup batter for each pancake. Cook until bubbles form on surface, then flip and cook until golden brown. Serve warm with maple syrup and extra berries.', NULL, 20);

-- Recipe Ingredients

-- Classic Chicken Parmesan
INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity) VALUES
(1, (SELECT id FROM ingredients WHERE name = 'Chicken Breast'), '4 pieces'),
(1, (SELECT id FROM ingredients WHERE name = 'Flour'), '1 cup'),
(1, (SELECT id FROM ingredients WHERE name = 'Eggs'), '2 whole'),
(1, (SELECT id FROM ingredients WHERE name = 'Marinara Sauce'), '2 cups'),
(1, (SELECT id FROM ingredients WHERE name = 'Mozzarella Cheese'), '1 cup'),
(1, (SELECT id FROM ingredients WHERE name = 'Parmesan Cheese'), '0.5 cup'),
(1, (SELECT id FROM ingredients WHERE name = 'Olive Oil'), '0.25 cup');

-- Creamy Tuscan Chicken
INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity) VALUES
(2, (SELECT id FROM ingredients WHERE name = 'Chicken Breast'), '4 pieces'),
(2, (SELECT id FROM ingredients WHERE name = 'Heavy Cream'), '1 cup'),
(2, (SELECT id FROM ingredients WHERE name = 'Spinach'), '2 cups'),
(2, (SELECT id FROM ingredients WHERE name = 'Garlic'), '4 cloves'),
(2, (SELECT id FROM ingredients WHERE name = 'Parmesan Cheese'), '0.5 cup'),
(2, (SELECT id FROM ingredients WHERE name = 'Olive Oil'), '2 tbsp'),
(2, (SELECT id FROM ingredients WHERE name = 'Salt'), '1 tsp'),
(2, (SELECT id FROM ingredients WHERE name = 'Black Pepper'), '0.5 tsp');

-- Garlic Butter Shrimp Pasta
INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity) VALUES
(3, (SELECT id FROM ingredients WHERE name = 'Shrimp'), '1 lb'),
(3, (SELECT id FROM ingredients WHERE name = 'Pasta'), '1 lb'),
(3, (SELECT id FROM ingredients WHERE name = 'Butter'), '4 tbsp'),
(3, (SELECT id FROM ingredients WHERE name = 'Garlic'), '6 cloves'),
(3, (SELECT id FROM ingredients WHERE name = 'White Wine'), '0.5 cup'),
(3, (SELECT id FROM ingredients WHERE name = 'Parmesan Cheese'), '0.5 cup'),
(3, (SELECT id FROM ingredients WHERE name = 'Lemon'), '1 whole');

-- Honey Garlic Salmon
INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity) VALUES
(4, (SELECT id FROM ingredients WHERE name = 'Salmon'), '4 fillets'),
(4, (SELECT id FROM ingredients WHERE name = 'Honey'), '0.25 cup'),
(4, (SELECT id FROM ingredients WHERE name = 'Soy Sauce'), '3 tbsp'),
(4, (SELECT id FROM ingredients WHERE name = 'Garlic'), '4 cloves'),
(4, (SELECT id FROM ingredients WHERE name = 'Ginger'), '1 tsp');

-- Beef Tacos
INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity) VALUES
(5, (SELECT id FROM ingredients WHERE name = 'Ground Beef'), '1 lb'),
(5, (SELECT id FROM ingredients WHERE name = 'Taco Seasoning'), '2 tbsp'),
(5, (SELECT id FROM ingredients WHERE name = 'Tortillas'), '8 pieces'),
(5, (SELECT id FROM ingredients WHERE name = 'Lettuce'), '2 cups'),
(5, (SELECT id FROM ingredients WHERE name = 'Cheddar Cheese'), '1 cup'),
(5, (SELECT id FROM ingredients WHERE name = 'Tomato'), '2 whole'),
(5, (SELECT id FROM ingredients WHERE name = 'Sour Cream'), '0.5 cup'),
(5, (SELECT id FROM ingredients WHERE name = 'Salsa'), '1 cup');

-- Chicken Stir-Fry
INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity) VALUES
(6, (SELECT id FROM ingredients WHERE name = 'Chicken Breast'), '1 lb'),
(6, (SELECT id FROM ingredients WHERE name = 'Bell Pepper'), '2 whole'),
(6, (SELECT id FROM ingredients WHERE name = 'Broccoli'), '2 cups'),
(6, (SELECT id FROM ingredients WHERE name = 'Carrots'), '2 whole'),
(6, (SELECT id FROM ingredients WHERE name = 'Soy Sauce'), '0.25 cup'),
(6, (SELECT id FROM ingredients WHERE name = 'Garlic'), '3 cloves'),
(6, (SELECT id FROM ingredients WHERE name = 'Ginger'), '1 tbsp'),
(6, (SELECT id FROM ingredients WHERE name = 'Rice'), '2 cups');

-- Baked Ziti
INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity) VALUES
(7, (SELECT id FROM ingredients WHERE name = 'Penne Pasta'), '1 lb'),
(7, (SELECT id FROM ingredients WHERE name = 'Marinara Sauce'), '3 cups'),
(7, (SELECT id FROM ingredients WHERE name = 'Italian Sausage'), '1 lb'),
(7, (SELECT id FROM ingredients WHERE name = 'Mozzarella Cheese'), '2 cups'),
(7, (SELECT id FROM ingredients WHERE name = 'Parmesan Cheese'), '0.5 cup');

-- Chicken Caesar Salad
INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity) VALUES
(8, (SELECT id FROM ingredients WHERE name = 'Chicken Breast'), '2 pieces'),
(8, (SELECT id FROM ingredients WHERE name = 'Lettuce'), '1 head'),
(8, (SELECT id FROM ingredients WHERE name = 'Parmesan Cheese'), '0.5 cup'),
(8, (SELECT id FROM ingredients WHERE name = 'Bread'), '2 cups');

-- Mushroom Risotto
INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity) VALUES
(9, (SELECT id FROM ingredients WHERE name = 'Rice'), '2 cups'),
(9, (SELECT id FROM ingredients WHERE name = 'Mushrooms'), '8 oz'),
(9, (SELECT id FROM ingredients WHERE name = 'Onion'), '1 whole'),
(9, (SELECT id FROM ingredients WHERE name = 'Chicken Stock'), '6 cups'),
(9, (SELECT id FROM ingredients WHERE name = 'Butter'), '4 tbsp'),
(9, (SELECT id FROM ingredients WHERE name = 'Parmesan Cheese'), '1 cup'),
(9, (SELECT id FROM ingredients WHERE name = 'White Wine'), '0.5 cup');

-- Lemon Herb Roasted Chicken
INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity) VALUES
(10, (SELECT id FROM ingredients WHERE name = 'Chicken Breast'), '1 whole'),
(10, (SELECT id FROM ingredients WHERE name = 'Lemon'), '2 whole'),
(10, (SELECT id FROM ingredients WHERE name = 'Garlic'), '6 cloves'),
(10, (SELECT id FROM ingredients WHERE name = 'Rosemary'), '3 sprigs'),
(10, (SELECT id FROM ingredients WHERE name = 'Thyme'), '3 sprigs'),
(10, (SELECT id FROM ingredients WHERE name = 'Olive Oil'), '0.25 cup'),
(10, (SELECT id FROM ingredients WHERE name = 'Salt'), '2 tsp'),
(10, (SELECT id FROM ingredients WHERE name = 'Black Pepper'), '1 tsp');

-- Thai Chicken Curry
INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity) VALUES
(11, (SELECT id FROM ingredients WHERE name = 'Chicken Thighs'), '1.5 lbs'),
(11, (SELECT id FROM ingredients WHERE name = 'Coconut Milk'), '1 can'),
(11, (SELECT id FROM ingredients WHERE name = 'Curry Powder'), '3 tbsp'),
(11, (SELECT id FROM ingredients WHERE name = 'Bell Pepper'), '2 whole'),
(11, (SELECT id FROM ingredients WHERE name = 'Basil'), '0.5 cup'),
(11, (SELECT id FROM ingredients WHERE name = 'Rice'), '2 cups');

-- Caprese Salad
INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity) VALUES
(12, (SELECT id FROM ingredients WHERE name = 'Mozzarella Cheese'), '8 oz'),
(12, (SELECT id FROM ingredients WHERE name = 'Tomato'), '4 whole'),
(12, (SELECT id FROM ingredients WHERE name = 'Basil'), '0.25 cup'),
(12, (SELECT id FROM ingredients WHERE name = 'Olive Oil'), '3 tbsp'),
(12, (SELECT id FROM ingredients WHERE name = 'Balsamic Vinegar'), '2 tbsp'),
(12, (SELECT id FROM ingredients WHERE name = 'Salt'), '0.5 tsp');

-- Beef Stroganoff
INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity) VALUES
(13, (SELECT id FROM ingredients WHERE name = 'Ground Beef'), '1 lb'),
(13, (SELECT id FROM ingredients WHERE name = 'Mushrooms'), '8 oz'),
(13, (SELECT id FROM ingredients WHERE name = 'Onion'), '1 whole'),
(13, (SELECT id FROM ingredients WHERE name = 'Sour Cream'), '1 cup'),
(13, (SELECT id FROM ingredients WHERE name = 'Butter'), '3 tbsp'),
(13, (SELECT id FROM ingredients WHERE name = 'Pasta'), '12 oz');

-- Vegetable Stir-Fry
INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity) VALUES
(14, (SELECT id FROM ingredients WHERE name = 'Broccoli'), '2 cups'),
(14, (SELECT id FROM ingredients WHERE name = 'Bell Pepper'), '2 whole'),
(14, (SELECT id FROM ingredients WHERE name = 'Carrots'), '2 whole'),
(14, (SELECT id FROM ingredients WHERE name = 'Soy Sauce'), '0.25 cup'),
(14, (SELECT id FROM ingredients WHERE name = 'Garlic'), '3 cloves'),
(14, (SELECT id FROM ingredients WHERE name = 'Ginger'), '1 tbsp'),
(14, (SELECT id FROM ingredients WHERE name = 'Olive Oil'), '2 tbsp');

-- Chicken Fajitas
INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity) VALUES
(15, (SELECT id FROM ingredients WHERE name = 'Chicken Breast'), '1 lb'),
(15, (SELECT id FROM ingredients WHERE name = 'Bell Pepper'), '3 whole'),
(15, (SELECT id FROM ingredients WHERE name = 'Onion'), '1 whole'),
(15, (SELECT id FROM ingredients WHERE name = 'Tortillas'), '8 pieces'),
(15, (SELECT id FROM ingredients WHERE name = 'Lime'), '2 whole'),
(15, (SELECT id FROM ingredients WHERE name = 'Avocado'), '1 whole'),
(15, (SELECT id FROM ingredients WHERE name = 'Sour Cream'), '0.5 cup'),
(15, (SELECT id FROM ingredients WHERE name = 'Salsa'), '1 cup');

-- Spaghetti Carbonara
INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity) VALUES
(16, (SELECT id FROM ingredients WHERE name = 'Pasta'), '1 lb'),
(16, (SELECT id FROM ingredients WHERE name = 'Bacon'), '8 slices'),
(16, (SELECT id FROM ingredients WHERE name = 'Eggs'), '4 whole'),
(16, (SELECT id FROM ingredients WHERE name = 'Parmesan Cheese'), '1 cup'),
(16, (SELECT id FROM ingredients WHERE name = 'Black Pepper'), '1 tsp');

-- Greek Salad
INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity) VALUES
(17, (SELECT id FROM ingredients WHERE name = 'Tomato'), '3 whole'),
(17, (SELECT id FROM ingredients WHERE name = 'Red Onion'), '0.5 whole'),
(17, (SELECT id FROM ingredients WHERE name = 'Feta Cheese'), '1 cup'),
(17, (SELECT id FROM ingredients WHERE name = 'Olive Oil'), '0.25 cup'),
(17, (SELECT id FROM ingredients WHERE name = 'Lemon'), '1 whole');

-- Pork Chops with Apples
INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity) VALUES
(18, (SELECT id FROM ingredients WHERE name = 'Pork Chops'), '4 pieces'),
(18, (SELECT id FROM ingredients WHERE name = 'Apple'), '2 whole'),
(18, (SELECT id FROM ingredients WHERE name = 'Butter'), '3 tbsp'),
(18, (SELECT id FROM ingredients WHERE name = 'Brown Sugar'), '2 tbsp'),
(18, (SELECT id FROM ingredients WHERE name = 'Sage'), '1 tbsp');

-- Minestrone Soup
INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity) VALUES
(19, (SELECT id FROM ingredients WHERE name = 'Onion'), '1 whole'),
(19, (SELECT id FROM ingredients WHERE name = 'Carrots'), '2 whole'),
(19, (SELECT id FROM ingredients WHERE name = 'Celery'), '2 stalks'),
(19, (SELECT id FROM ingredients WHERE name = 'Tomato'), '2 whole'),
(19, (SELECT id FROM ingredients WHERE name = 'Chickpeas'), '1 can'),
(19, (SELECT id FROM ingredients WHERE name = 'Pasta'), '1 cup'),
(19, (SELECT id FROM ingredients WHERE name = 'Spinach'), '2 cups'),
(19, (SELECT id FROM ingredients WHERE name = 'Parmesan Cheese'), '0.5 cup');

-- Teriyaki Chicken Bowl
INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity) VALUES
(20, (SELECT id FROM ingredients WHERE name = 'Chicken Thighs'), '1 lb'),
(20, (SELECT id FROM ingredients WHERE name = 'Soy Sauce'), '0.25 cup'),
(20, (SELECT id FROM ingredients WHERE name = 'Brown Sugar'), '2 tbsp'),
(20, (SELECT id FROM ingredients WHERE name = 'Ginger'), '1 tbsp'),
(20, (SELECT id FROM ingredients WHERE name = 'Garlic'), '3 cloves'),
(20, (SELECT id FROM ingredients WHERE name = 'Rice'), '2 cups'),
(20, (SELECT id FROM ingredients WHERE name = 'Broccoli'), '2 cups');

-- Classic Burger
INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity) VALUES
(21, (SELECT id FROM ingredients WHERE name = 'Ground Beef'), '1.5 lbs'),
(21, (SELECT id FROM ingredients WHERE name = 'Bread'), '4 buns'),
(21, (SELECT id FROM ingredients WHERE name = 'Lettuce'), '4 leaves'),
(21, (SELECT id FROM ingredients WHERE name = 'Tomato'), '1 whole'),
(21, (SELECT id FROM ingredients WHERE name = 'Onion'), '1 whole'),
(21, (SELECT id FROM ingredients WHERE name = 'Cheddar Cheese'), '4 slices'),
(21, (SELECT id FROM ingredients WHERE name = 'Mayo'), '0.25 cup'),
(21, (SELECT id FROM ingredients WHERE name = 'Mustard'), '2 tbsp');

-- Chicken Quesadillas
INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity) VALUES
(22, (SELECT id FROM ingredients WHERE name = 'Chicken Breast'), '2 cups'),
(22, (SELECT id FROM ingredients WHERE name = 'Tortillas'), '6 pieces'),
(22, (SELECT id FROM ingredients WHERE name = 'Cheddar Cheese'), '2 cups'),
(22, (SELECT id FROM ingredients WHERE name = 'Bell Pepper'), '1 whole'),
(22, (SELECT id FROM ingredients WHERE name = 'Salsa'), '1 cup'),
(22, (SELECT id FROM ingredients WHERE name = 'Sour Cream'), '0.5 cup');

-- Pad Thai
INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity) VALUES
(23, (SELECT id FROM ingredients WHERE name = 'Shrimp'), '1 lb'),
(23, (SELECT id FROM ingredients WHERE name = 'Rice'), '8 oz'),
(23, (SELECT id FROM ingredients WHERE name = 'Eggs'), '2 whole'),
(23, (SELECT id FROM ingredients WHERE name = 'Soy Sauce'), '3 tbsp'),
(23, (SELECT id FROM ingredients WHERE name = 'Lime'), '2 whole'),
(23, (SELECT id FROM ingredients WHERE name = 'Cilantro'), '0.5 cup');

-- BBQ Chicken Pizza
INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity) VALUES
(24, (SELECT id FROM ingredients WHERE name = 'Chicken Breast'), '2 cups'),
(24, (SELECT id FROM ingredients WHERE name = 'Mozzarella Cheese'), '2 cups'),
(24, (SELECT id FROM ingredients WHERE name = 'Red Onion'), '0.5 whole'),
(24, (SELECT id FROM ingredients WHERE name = 'Cilantro'), '0.25 cup');

-- Berry Pancakes for Breakfast
INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity) VALUES
(25, (SELECT id FROM ingredients WHERE name = 'Flour'), '2 cups'),
(25, (SELECT id FROM ingredients WHERE name = 'Sugar'), '2 tbsp'),
(25, (SELECT id FROM ingredients WHERE name = 'Baking Powder'), '2 tsp'),
(25, (SELECT id FROM ingredients WHERE name = 'Salt'), '0.5 tsp'),
(25, (SELECT id FROM ingredients WHERE name = 'Eggs'), '2 whole'),
(25, (SELECT id FROM ingredients WHERE name = 'Milk'), '1.5 cups'),
(25, (SELECT id FROM ingredients WHERE name = 'Butter'), '3 tbsp');