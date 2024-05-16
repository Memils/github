import sqlite3

conn = sqlite3.connect('restaurant_menus.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Restaurant (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Dish (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    description REAL NOT NULL,
    price REAL NOT NULL,
    restaurant_id INTEGER,
    FOREIGN KEY (restaurant_id) REFERENCES Restaurant(id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    password TEXT NOT NULL, 
    restaurant_id INTEGER,
    FOREIGN KEY (restaurant_id) REFERENCES Restaurant(id)            
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Customers (
    id INTEGER PRIMARY KEY, 
    mailaddress TEXT NOT NULL,
    password TEXT NOT NULL
)
''')

restaurants = [
    ('Beste Bakeri AS',),
    ('Little Eataly',),
    ('Egon Rime',)
]
cursor.executemany('INSERT INTO Restaurant (name) VALUES (?)', restaurants)
conn.commit()

restaurant_a_dishes = [
    ('Pasta Bolognese',"a",15.99, 1),
    ('Pizza Bolognese',"a",12.50, 1),
    ('Focacia Bolognese',"a",18.75, 1),
    ('Caesar Bolognese',"a",10.25, 1),
    ('Burger Bolognese',"a",14.99, 1)
]
cursor.executemany('INSERT INTO Dish (name, description, price, restaurant_id) VALUES (?, ?, ?, ?)', restaurant_a_dishes)

restaurant_b_dishes = [
    ('Sushi Platter',"a",24.99, 2),
    ('Teriyaki Chicken',"a",16.50, 2),
    ('Vegetable Tempura',"a",11.75, 2),
    ('Ramen Soup',"a",13.25, 2),
    ('Beef Teriyaki',"a",19.99, 2)
]
cursor.executemany('INSERT INTO Dish (name, description, price, restaurant_id) VALUES (?, ?, ?, ?)', restaurant_b_dishes)

restaurant_c_dishes = [
    ('Spaghetti Vituro',"a",14.99, 3),
    ('Chicken Parmesan',"a",17.50, 3),
    ('Garlic Bread',"a",6.75, 3),
    ('Caprese Salad',"a",9.25, 3),
    ('Tiramisu',"a",8.99, 3)
]
cursor.executemany('INSERT INTO Dish (name, description, price, restaurant_id) VALUES (?, ?, ?, ?)', restaurant_c_dishes)
conn.commit()
users = [
    ('eier1', 'passord1', 1),
    ('eier2', 'passord2', 2),
    ('eier3', 'passord3', 3)
]

customers = [
    ('placeholder@gmail.com', 'placeholder')
]
cursor.executemany('INSERT INTO Users (username, password, restaurant_id) VALUES (?, ?, ?)', users)
cursor.executemany('INSERT INTO Customers (mailaddress, password) VALUES (?, ?)', customers)
conn.commit()
conn.close()