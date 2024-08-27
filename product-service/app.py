from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('products.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/products', methods=['GET'])
def get_products():
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM products').fetchall()
    conn.close()
    return jsonify([dict(product) for product in products])

@app.route('/products', methods=['POST'])
def create_product():
    product = request.json
    conn = get_db_connection()
    conn.execute('INSERT INTO products (name, price) VALUES (?, ?)',
                 (product['name'], product['price']))
    conn.commit()
    conn.close()
    return jsonify(product), 201

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)