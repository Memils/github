from flask import Flask, jsonify, request
import sqlite3
from flask_cors import CORS
import jwt
from functools import wraps

app = Flask(__name__)
port = 3000
CORS(app)

app.config['SECRET_KEY'] = 'eksamen'

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = data['username']
        except:
            return jsonify({'message': 'Token is invalid'}), 401

        return f(current_user, *args, **kwargs)

    return decorated

@app.route('/Restaurant')
@app.route('/')
def get_restaurants():
    with sqlite3.connect('./restaurant_menus.db', check_same_thread=False) as db:
        cursor = db.cursor()
        cursor.execute('SELECT * FROM Restaurant')
        rows = cursor.fetchall()
    return jsonify(rows)

@app.route('/Dish/<int:restaurantId>')
def get_dishes(restaurantId):
    print(restaurantId)
    with sqlite3.connect('./restaurant_menus.db', check_same_thread=False) as db:
        cursor = db.cursor()
        cursor.execute('SELECT * FROM Dish WHERE restaurant_id = ?', (restaurantId,))
        rows = cursor.fetchall()
    return jsonify(rows)

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    print("Received username:", username)
    print("Received password:", password)

    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    with sqlite3.connect('./restaurant_menus.db', check_same_thread=False) as db:
        cursor = db.cursor()
        cursor.execute('SELECT * FROM Users WHERE username=? AND password=?', (username, password))
        user = cursor.fetchone()

    print("User data:", user)

    if not user:
        return jsonify({'message': 'Invalid username or password'}), 401

    token = jwt.encode({'username': username}, app.config['SECRET_KEY'], algorithm="HS256")

    return jsonify({'token': token}), 200

@app.route('/add_dish', methods=['POST'])
@token_required
def add_dish(current_user):
    data = request.json
    dish_name = data.get('name')
    description = data.get('description')
    price = data.get('price')
    restaurant_id = data.get('restaurant_id')

    if not dish_name or not description or not price or not restaurant_id:
        return jsonify({'message': 'All fields are required'}), 400

    with sqlite3.connect('./restaurant_menus.db', check_same_thread=False) as db:
        cursor = db.cursor()
        cursor.execute('INSERT INTO Dish (name, description, price, restaurant_id) VALUES (?, ?, ?, ?)', (dish_name, description, price, restaurant_id))
        db.commit()

    return jsonify({'message': 'Dish added successfully'}), 200

@app.route('/register', methods=['OPTIONS'])
def options_register():
    response = jsonify({'message': 'CORS request allowed.'})
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods', 'POST')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Allowed', 'POST')
    return response

@app.route('/add_customer', methods=['POST'])
def add_customer():
    try:
        data = request.json
        mailaddress = data.get('mailaddress')
        password = data.get('password')

        if not mailaddress or not password:
            return jsonify({'message': 'Mail address and password are required'}), 400

        with sqlite3.connect('./restaurant_menus.db', check_same_thread=False) as db:
            cursor = db.cursor()
            cursor.execute('INSERT INTO Customers (mailaddress, password) VALUES (?, ?)', (mailaddress, password))
            db.commit()

        return jsonify({'message': 'Customer added successfully'}), 200
    except Exception as e:
        return jsonify({'message': 'An error occurred', 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=port)