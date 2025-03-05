from flask import Flask, jsonify, request
import psycopg2
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


# Add your database details here
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

# login 
# TODO: check login and adjust frontend

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


# Reservations 

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


# Shcedules 

def get_schedules():
    conn = connect_db()
    if not conn:
        return None
    
    cur = conn.cursor()
    
    # Query to fetch all schedules
    query = "SELECT scheduleid, userid, shiftdate, timestart, timeend, approvalstatus FROM schedules"
    cur.execute(query)
    
    schedules = cur.fetchall()

    conn.close()

    schedules_list = []
    for schedule in schedules:
        schedules_list.append({
            "scheduleid": schedule[0],
            "userid": schedule[1],
            "shiftdate": schedule[2].strftime('%Y-%m-%d') if isinstance(schedule[2], datetime) else schedule[2],
            "timestart": schedule[3].strftime('%H:%M:%S') if isinstance(schedule[3], time) else schedule[3],
            "timeend": schedule[4].strftime('%H:%M:%S') if isinstance(schedule[4], time) else schedule[4],
            "approvalstatus": schedule[5]
        })
    
    return schedules_list


@app.route('/get_schedules', methods=['POST'])
def handle_get_schedules():
    data = request.get_json()
    filters = {
        "shiftdate": data.get("shiftdate"),
        "approvalstatus": data.get("approvalstatus"),
        "userid": data.get("userid")
    }
    
    schedules = get_schedules()
    if schedules:
        return jsonify({"status": "success", "schedules": schedules})
    else:
        return jsonify({"status": "error", "message": "No schedules found"}), 404


@app.route('/add_shift', methods=['POST'])
def add_shift():
    data = request.get_json()

    userid = data.get('userid')
    shiftdate = data['shiftdate']
    timestart = data['timestart']
    timeend = data['timeend']
    approvalstatus = 'Pending'

    try:
        conn = connect_db()
        cur = conn.cursor()

        insert_query = """
        INSERT INTO schedules (userid, shiftdate, timestart, timeend, approvalstatus)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING scheduleid
        """

        cur.execute(insert_query, (userid, shiftdate, timestart, timeend, approvalstatus))
        schedule_id = cur.fetchone()[0]

        conn.commit()

        cur.close()
        conn.close()

        return jsonify({"status": "success", "message": "Shift added successfully", "scheduleid": schedule_id})

    except Exception as e:
        print(f"Error adding shift: {e}")
        return jsonify({"status": "error", "message": "Error adding shift"})


@app.route('/edit_shift', methods=['POST'])
def edit_shift():
    data = request.get_json()
    scheduleid = data['scheduleid']
    shiftdate = data.get('shiftdate')
    timestart = data['timestart']
    timeend = data['timeend']

    try:
        conn = connect_db()
        cur = conn.cursor()

        update_query = """
        UPDATE schedules
        SET shiftdate = %s, timestart = %s, timeend = %s
        WHERE scheduleid = %s
        """
        cur.execute(update_query, (shiftdate, timestart, timeend, scheduleid))

        conn.commit()

        if cur.rowcount > 0:
            response = {"status": "success", "message": "Shift updated successfully"}
        else:
            response = {"status": "error", "message": "Shift not found"}

        cur.close()
        conn.close()

        return jsonify(response)

    except Exception as e:
        print(f"Error updating shift: {e}")
        return jsonify({"status": "error", "message": "Error updating shift"})


@app.route('/get_schedules', methods=['GET'])
def get_schedules():
    conn = connect_db()
    if not conn:
        return jsonify({"status": "error", "message": "Database connection failed"}), 500

    cur = conn.cursor()
    query = "SELECT scheduleid, userid, shiftdate, timestart, timeend, approvalstatus FROM schedules"
    cur.execute(query)
    schedules = cur.fetchall()

    conn.close()

    schedules_list = []
    for schedule in schedules:
        schedules_list.append({
            "scheduleid": schedule[0],
            "userid": schedule[1],
            "shiftdate": schedule[2].strftime('%Y-%m-%d') if isinstance(schedule[2], datetime) else schedule[2],
            "timestart": schedule[3].strftime('%H:%M:%S') if isinstance(schedule[3], time) else schedule[3],
            "timeend": schedule[4].strftime('%H:%M:%S') if isinstance(schedule[4], time) else schedule[4],
            "approvalstatus": schedule[5]
        })
    
    return jsonify({"status": "success", "schedules": schedules_list})

# users

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