-- Populate restaurants
INSERT INTO ordering_restaurant (name, address) VALUES ('Italian Bistro', '123 Pasta Lane');
INSERT INTO ordering_restaurant (name, address) VALUES ('Sushi Place', '456 Fish Ave');
INSERT INTO ordering_restaurant (name, address) VALUES ('Burger Joint', '789 Beef Blvd');

-- Populate categories
INSERT INTO ordering_category (name) VALUES ('Italian');
INSERT INTO ordering_category (name) VALUES ('Japanese');
INSERT INTO ordering_category (name) VALUES ('American');

-- Populate dishes
INSERT INTO ordering_dish (name, description, price, category_id, restaurant_id) VALUES ('Spaghetti Carbonara', 'Classic Italian pasta with eggs, cheese, pancetta, and pepper.', 12.50, 1, 1);
INSERT INTO ordering_dish (name, description, price, category_id, restaurant_id) VALUES ('Margherita Pizza', 'Traditional pizza with tomatoes, mozzarella, and basil.', 10.00, 1, 1);
INSERT INTO ordering_dish (name, description, price, category_id, restaurant_id) VALUES ('Sushi Platter', 'Assorted fresh sushi.', 20.00, 2, 2);
INSERT INTO ordering_dish (name, description, price, category_id, restaurant_id) VALUES ('Tempura', 'Lightly battered and fried seafood and vegetables.', 15.00, 2, 2);
INSERT INTO ordering_dish (name, description, price, category_id, restaurant_id) VALUES ('Cheeseburger', 'Grilled beef patty with cheese, lettuce, tomato, and onion.', 8.00, 3, 3);
INSERT INTO ordering_dish (name, description, price, category_id, restaurant_id) VALUES ('BBQ Ribs', 'Slow-cooked ribs with BBQ sauce.', 18.00, 3, 3);
