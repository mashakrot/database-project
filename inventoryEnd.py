from flask import Flask, jsonify, request
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

def get_supplier_by_itemname_or_id(item_value, search_type):
    conn = connect_db()
    if not conn:
        return None

    cur = conn.cursor()

    if search_type == "id":
        # Query based on itemid
        cur.execute("""
            SELECT suppliername, suppliers.telephonenumber, suppliers.email 
            FROM suppliers 
            WHERE supplierid = (SELECT supplierid FROM inventory WHERE itemid = %s)
        """, (item_value,))

    else:
        # Query based on itemname
        cur.execute("""
            SELECT suppliername, suppliers.telephonenumber, suppliers.email 
            FROM suppliers 
            WHERE supplierid = (SELECT supplierid FROM inventory WHERE itemname = %s)
        """, (item_value,))

    supplier = cur.fetchone()
    conn.close()


    if supplier:
        print("Supplier found:", supplier)
    else:
        print("No supplier found.")




    return supplier  # Return the supplier data

@app.route('/get_supplier_by_itemname', methods=['POST', 'GET'])  # ✅ Allow GET for debugging
def handle_get_supplier_by_itemname():
    if request.method == "GET":
        return jsonify({"status": "error", "message": "Use POST to fetch supplier data"}), 405

    data = request.get_json()
    item_value = data.get("itemid") or data.get("itemname")
    search_type = "id" if data.get("itemid") else "name"
    print(f"Searching for supplier by {search_type}: {item_value}")

    supplier = get_supplier_by_itemname_or_id(item_value, search_type)

    if supplier:
        return jsonify({"status": "success", "supplier": supplier})
    else:
        return jsonify({"status": "error", "message": "No supplier found"}), 404
    




if __name__ == '__main__':
    app.run(debug=True)
