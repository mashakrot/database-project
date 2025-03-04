from flask import Flask, jsonify
import psycopg2  # PostgreSQL adapter for Python
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def connect_db():
    try:
        # Connect to your PostgreSQL database
        conn = psycopg2.connect(
            dbname="Project",  # Replace with your DB name
            user="postgres",   # Replace with your username
            password="hello1234",  # Replace with your password
            host="localhost",  # Use your DB host if it's different
            port="5432"  # Default PostgreSQL port
        )
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None

def get_inventory():
    conn = connect_db()
    if not conn:
        return None
    
    cur = conn.cursor()
    cur.execute("SELECT * FROM inventory")  # Adjust the query as needed
    inventory = cur.fetchall()  # Fetch all rows from the result
    
    conn.close()
    
    return inventory  # Return the inventory data

@app.route('/get_inventory', methods=['POST'])  # Adjust the route to '/inventory'
def handle_get_inventory():
    # Call the get_inventory function to fetch inventory data
    inventory = get_inventory()

    if inventory:
        # Return the inventory data as JSON
        return jsonify({"status": "success", "inventory": inventory})
    else:
        # Return an error if no inventory is found or there was an issue
        return jsonify({"status": "error", "message": "No inventory found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
