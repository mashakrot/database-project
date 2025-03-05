from flask import Flask, jsonify
import psycopg2  # PostgreSQL adapter for Python
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def connect_db():
    try:
        # Connect to your PostgreSQL database
        conn = psycopg2.connect(
            dbname="restaurant_db",  # Replace with your DB name
            user="postgres",   # Replace with your username
            password="hello1234",  # Replace with your password
            host="localhost",  # Use your DB host if it's different
            port="5432"  # Default PostgreSQL port
        )
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None

def get_reservations():
    conn = connect_db()
    if not conn:
        return
    
    cur = conn.cursor()
    cur.execute("SELECT * FROM reservations")
    reservations = cur.fetchall()
    
    conn.close()
    
    return reservations  # Return the reservations data

@app.route('/get_reservations', methods=['GET'])  
def handle_get_reservations():
    # Call the get_reservations function to fetch reservations data
    reservations = get_reservations()

    if reservations:
        # Return the reservations data as JSON
        return jsonify({"status": "success", "reservations": reservations})
    else:
        # Return an error if no reservations is found or there was an issue
        return jsonify({"status": "error", "message": "No reservations found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
