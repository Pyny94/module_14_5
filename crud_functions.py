import sqlite3

def initiate_db():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INT NOT NULL
    )'''
                   )

    cursor.execute('''CREATE TABLE IF NOT EXISTS Users(
              id INTEGER PRIMARY KEY,
              username TEXT NOT NULL,
              email TEXT NOT NULL,
              age INT NOT NULL,
              balance INT NOT NULL
              )'''
                   )

   # cursor.execute('INSERT INTO Users (title, description, price) VALUES (?, ?, ?)',
   #                 ('Продукт1', 'Описание1', '100'))
   #  cursor.execute('INSERT INTO Products (title, description, price) VALUES (?, ?, ?)',
   #                  ('Продукт2', 'Описание2', '200'))
   #  cursor.execute('INSERT INTO Products (title, description, price) VALUES (?, ?, ?)',
   #                 ('Продукт3', 'Описание3', '300'))
   # cursor.execute('INSERT INTO Products (title, description, price) VALUES (?, ?, ?)',
   #                  ('Продукт4', 'Описание4', '400'))

    connection.commit()
    connection.close()


def add_product(product_data):
    conn = sqlite3.connect('products')
    c = conn.cursor()
    c.execute('''INSERT INTO Products (title, description, price) VALUES (?, ?, ?)''', product_data)
    conn.commit()
    conn.close()

def get_all_products():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM Products')
    result = cursor.fetchall()

    connection.commit()
    connection.close()

    return result

def add_user(username, email, age):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)",
                       (username, email, age, 1000))
        conn.commit()
        conn.close()


def is_included(username):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM Users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()
    return bool(result)


