from flask import Flask, jsonify, request
import psycopg2
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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

def get_inventory():
    conn = connect_db()
    if not conn:
        return None
    
    cur = conn.cursor()
    cur.execute("SELECT * FROM inventory")
    inventory = cur.fetchall()
    
    conn.close()
    
    return inventory

@app.route('/get_inventory', methods=['POST'])
def handle_get_inventory():
    inventory = get_inventory()

    if inventory:
        return jsonify({"status": "success", "inventory": inventory})
    else:
        return jsonify({"status": "error", "message": "No inventory found"}), 404

def get_supplier_by_itemname_or_id(item_value, search_type):
    conn = connect_db()
    if not conn:
        return None

    cur = conn.cursor()

    if search_type == "id":
        cur.execute("""
            SELECT suppliername, suppliers.telephonenumber, suppliers.email 
            FROM suppliers 
            WHERE supplierid = (SELECT supplierid FROM inventory WHERE itemid = %s)
        """, (item_value,))
    else:
        cur.execute("""
            SELECT suppliername, suppliers.telephonenumber, suppliers.email 
            FROM suppliers 
            WHERE supplierid = (SELECT supplierid FROM inventory WHERE itemname = %s)
        """, (item_value,))

    supplier = cur.fetchone()
    conn.close()

    return supplier

@app.route('/get_supplier_by_itemname', methods=['POST', 'GET'])
def handle_get_supplier_by_itemname():
    if request.method == "GET":
        return jsonify({"status": "error", "message": "Use POST to fetch supplier data"}), 405

    data = request.get_json()
    item_value = data.get("itemid") or data.get("itemname")
    search_type = "id" if data.get("itemid") else "name"

    supplier = get_supplier_by_itemname_or_id(item_value, search_type)

    if supplier:
        return jsonify({"status": "success", "supplier": supplier})
    else:
        return jsonify({"status": "error", "message": "No supplier found"}), 404

@app.route('/update_inventory', methods=['POST'])
def update_inventory():
    data = request.get_json()
    item_name = data.get("itemName")
    ordered_quantity = data.get("orderedQuantity")

    conn = connect_db()
    if not conn:
        return jsonify({"status": "error", "message": "Database connection failed"})

    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM inventory WHERE itemname = %s", (item_name,))
        item = cur.fetchone()

        new_quantity = item[2] + ordered_quantity
        cur.execute("UPDATE inventory SET quantity = %s WHERE itemname = %s", (new_quantity, item_name))

        conn.commit()

        cur.execute("SELECT * FROM inventory ORDER BY itemid;")
        updated_inventory = cur.fetchall()

        return jsonify({"status": "success", "updatedInventory": updated_inventory})

    except Exception as e:
        print(f"Error occurred: {e}")
        conn.rollback()
        return jsonify({"status": "error", "message": "An error occurred while updating the inventory."}), 500

    finally:
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)