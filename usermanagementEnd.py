from flask import Flask, jsonify, request
import psycopg2
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Database connection function
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

# Get all users
@app.route('/users', methods=['GET'])
def get_users():
    conn = connect_db()
    if not conn:
        return jsonify({"status": "error", "message": "Database connection failed"}), 500
    
    cur = conn.cursor()
    query = "SELECT userid, name, email, telephonenumber, author FROM users"
    cur.execute(query)
    users = cur.fetchall()

    conn.close()

    users_list = []
    for user in users:
        users_list.append({
            "userid": user[0],
            "name": user[1],
            "email": user[2],
            "telephonenumber": user[3],
            "author": user[4]
        })
    
    return jsonify({"status": "success", "users": users_list})

# Add a user
@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    
    name = data.get('name')
    email = data.get('email')
    telephonenumber = data.get('telephonenumber')
    author = data.get('author', 'Staff')  # Default to 'Staff' if not provided

    try:
        conn = connect_db()
        cur = conn.cursor()

        insert_query = """
        INSERT INTO users (name, email, telephonenumber, author)
        VALUES (%s, %s, %s, %s)
        RETURNING userid
        """
        cur.execute(insert_query, (name, email, telephonenumber, author))
        user_id = cur.fetchone()[0]

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"status": "success", "message": "User added successfully", "userid": user_id})

    except Exception as e:
        print(f"Error adding user: {e}")
        return jsonify({"status": "error", "message": "Error adding user"})

# Delete a user
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        conn = connect_db()
        cur = conn.cursor()

        delete_query = "DELETE FROM users WHERE userid = %s"
        cur.execute(delete_query, (user_id,))

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"status": "success", "message": "User deleted successfully"})

    except Exception as e:
        print(f"Error deleting user: {e}")
        return jsonify({"status": "error", "message": "Error deleting user"})

if __name__ == '__main__':
    app.run(debug=True)
