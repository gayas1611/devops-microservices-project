from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('orders.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/orders', methods=['GET'])
def get_orders():
    conn = get_db_connection()
    orders = conn.execute('SELECT * FROM orders').fetchall()
    conn.close()
    return jsonify([dict(order) for order in orders])

@app.route('/orders', methods=['POST'])
def create_order():
    order = request.json
    conn = get_db_connection()
    conn.execute('INSERT INTO orders (user_id, product_id, quantity) VALUES (?, ?, ?)',
                 (order['user_id'], order['product_id'], order['quantity']))
    conn.commit()
    conn.close()
    return jsonify(order), 201

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)