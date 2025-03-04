from flask import Flask, request, jsonify
import psycopg2  # PostgreSQL adapter for Python
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins

def connect_db():
    try:
        conn = psycopg2.connect(
            dbname="restaurant_db",
            user="postgres",
            password="hello1234",
            host="localhost",
            port="5432"
        )
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None

def login(email, password):
    conn = connect_db()
    if not conn:
        return None
    
    cur = conn.cursor()
    cur.execute("SELECT userid, name, password FROM users WHERE email = %s", (email,))
    db_user = cur.fetchone()
    
    cur.close()
    conn.close()
    
    if not db_user or db_user[2] != password:  # Plain-text password (Not secure, consider bcrypt)
        return None  

    return {"userid": db_user[0], "name": db_user[1]}  

@app.route('/login', methods=['POST'])
def handle_login():
    data = request.json  
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"status": "error", "message": "Email and password required"}), 400

    user = login(email, password)  

    if user:
        response = jsonify({"status": "success", "user": user})
    else:
        response = jsonify({"status": "error", "message": "Invalid credentials"}), 401

    response.headers.add("Access-Control-Allow-Origin", "*")  # 🔹 Explicitly allow CORS
    response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
    response.headers.add("Access-Control-Allow-Methods", "POST, GET, OPTIONS")

    return response

if __name__ == '__main__':
    app.run(debug=True)
