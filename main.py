'use strict';
import psycopg2

DB_NAME = "Project"
DB_USER = "postgres"
DB_PASSWORD = "hello1234"
DB_HOST = "localhost"
DB_PORT = "5432"


# connecting to the database
def connect_db():
    try:
        conn = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
        print("connection done")
        return conn
    
    
    except Exception as e:
        print("Error connecting to database:", e)
        return None
# connecting to the database END

# ADMIN PAGE - viewing, changing and deleting user info
def get_user_info(userid):
    conn = connect_db()
    if not conn:
        return
    
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE userid = %s", (userid,))
    user = cur.fetchone()
    
    conn.close()
    
    if user:
        print(f"user found: {user}")
    else:
        print("user not found.")
     
def insert_user(userid, name, email, telephonenumber, author):
    conn = connect_db()
    if not conn:
        return
    cur = conn.cursor()
    

    cur.execute("SELECT * FROM users WHERE userid = %s", (userid,))
    if cur.fetchone():

        print("user number already exists. Try again")
        conn.close()
        return
    
    cur.execute("""
        INSERT INTO users (userid, name, email, telephonenumber, author) 
        VALUES (%s, %s, %s, %s, %s)
    """, (userid, name, email, telephonenumber, author))

    
    conn.commit()

    print("We added user successfully")
    conn.close()

def update_user(userid, new_sname, new_sage, new_sgender, new_sdept):
    conn = connect_db()
    if not conn:
        return
    cur = conn.cursor()
    
    
    cur.execute("SELECT * FROM users WHERE userid = %s", (userid,))

    user = cur.fetchone()
    
    if not user:
        print("user not found")
        conn.close()
        return
    
    print(f"Current user Data: {user}")
    
    cur.execute("""
        UPDATE users 
        SET name = %s, email = %s, telephonenumber = %s, author = %s 
        WHERE userid = %s
    """, (new_sname, new_sage, new_sgender, new_sdept, userid)) 
    
    conn.commit()
    
    print("user updated successfully!")
    conn.close()
    
def delete_user(userid):
    conn = connect_db()
    if not conn:
        return
    cur = conn.cursor()
    
    # delete from staff assignments
    """ cur.execute("SELECT * FROM sc WHERE userid = %s", (userid,))
    if cur.fetchone():
        print("user is enrolled in courses. Deleting enrollments first...")
        cur.execute("DELETE FROM sc WHERE userid = %s", (userid,)) """
    
    cur.execute("DELETE FROM users WHERE userid = %s", (userid,))
    conn.commit()
    print("user deleted successfully!")
    conn.close()
# ADMIN PAGE - viewing, changing and deleting user info END


# HOST PAGE - viewing, changing and deleting user info END

# HOST PAGE - viewing, changing and deleting user info END



# STAFF PAGE - viewing, changing and deleting user info END
# STAFF PAGE - viewing, changing and deleting user info END





# CHEF PAGE - viewing, changing and deleting user info END
# Should be able to look up inventory, display items at a low reorder level differently, get contact information of suppliers
def find_supplier(itemname):
    conn = connect_db()
    if not conn:
        return
    
    cur = conn.cursor()
    cur.execute("SELECT suppliername, suppliers.telephonenumber, suppliers.email FROM suppliers WHERE supplierid = (SELECT supplierid FROM inventory WHERE itemname = %s)", (itemname,))
    supplier = cur.fetchone()
    
    conn.close()
    
    if supplier:
        print(f"supplier found: {supplier}")
    else:
        print("supplier not found.")

def find_supplier(itemid):
    conn = connect_db()
    if not conn:
        return
    
    cur = conn.cursor()
    cur.execute("SELECT suppliername, suppliers.telephonenumber, suppliers.email FROM suppliers WHERE supplierid = (SELECT supplierid FROM inventory WHERE itemid = %s)", (itemid,))
    supplier = cur.fetchone()
    
    conn.close()
    
    if supplier:
        print(f"supplier found: {supplier}")
    else:
        print("supplier not found.")

def order_item(itemid, q_order):
    conn = connect_db()
    if not conn:
        return
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM inventory WHERE itemid = %s", (itemid,))

    item = cur.fetchone()
    
    if not item:
        print("item not found")
        conn.close()
        return
    
    print(f"Current item Data: {item}")

    new_q = item[2] + int(q_order)

    print(f"New quantity: {new_q}")
    
    cur.execute("""
        UPDATE inventory 
        SET quantity = %s 
        WHERE itemid = %s
    """, (new_q, itemid)) 
    
    conn.commit()
    
    print("Quantity updated successfully!")
    conn.close()

def order_item(itemname, q_order):
    conn = connect_db()
    if not conn:
        return
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM inventory WHERE itemname = %s", (itemname,))

    item = cur.fetchone()
    
    if not item:
        print("item not found")
        conn.close()
        return
    
    print(f"Current item Data: {item}")

    new_q = item[2] + int(q_order)

    print(f"New quantity: {new_q}")
    
    cur.execute("""
        UPDATE inventory 
        SET quantity = %s 
        WHERE itemname = %s
    """, (new_q, itemname)) 
    
    conn.commit()
    
    print("Quantity updated successfully!")
    conn.close()

def at_reorder_level():
    conn = connect_db()
    if not conn:
        return
    
    cur = conn.cursor()
    cur.execute("SELECT suppliername, suppliers.telephonenumber, suppliers.email FROM suppliers WHERE supplierid = (SELECT supplierid FROM inventory WHERE itemid = %s)", (itemid,))
    supplier = cur.fetchone()
    
    conn.close()
    
    if supplier:
        print(f"supplier found: {supplier}")
    else:
        print("supplier not found.")


# CHEF PAGE - viewing, changing and deleting user info END









# FUNCTIONS FOR FETCHING ALL TABLE DATA   
def get_roles():
    conn = connect_db()
    if not conn:
        return
    
    cur = conn.cursor()
    cur.execute("SELECT * FROM roles")
    roles = cur.fetchall()
    
    conn.close()
    
    if roles:
        print(f"user found: {roles}")
    else:
        print("user not found.")

def get_users():
    conn = connect_db()
    if not conn:
        return
    
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    
    conn.close()
    
    if users:
        print(f"user found: {users}")
    else:
        print("user not found.")

def get_inventory():
    conn = connect_db()
    if not conn:
        return
    
    cur = conn.cursor()
    cur.execute("SELECT * FROM inventory")
    inventory = cur.fetchall()
    
    conn.close()
    
    if inventory:
        print(f"user found: {inventory}")
    else:
        print("user not found.")

def get_reservations():
    conn = connect_db()
    if not conn:
        return
    
    cur = conn.cursor()
    cur.execute("SELECT * FROM reservations")
    reservations = cur.fetchall()
    
    conn.close()
    
    if reservations:
        print(f"user found: {reservations}")
    else:
        print("user not found.")

def get_suppliers():
    conn = connect_db()
    if not conn:
        return
    
    cur = conn.cursor()
    cur.execute("SELECT * FROM suppliers")
    suppliers = cur.fetchall()
    
    conn.close()
    
    if suppliers:
        print(f"user found: {suppliers}")
    else:
        print("user not found.")
    
def get_tables():
    conn = connect_db()
    if not conn:
        return
    
    cur = conn.cursor()
    cur.execute("SELECT * FROM tables")
    tables = cur.fetchall()
    
    conn.close()
    
    if tables:
        print(f"user found: {tables}")
    else:
        print("user not found.")

def get_staffassignments():
    conn = connect_db()
    if not conn:
        return
    
    cur = conn.cursor()
    cur.execute("SELECT * FROM staffassignments")
    staffassignments = cur.fetchall()
    
    conn.close()
    
    if staffassignments:
        print(f"user found: {staffassignments}")
    else:
        print("user not found.")

def get_schedules():
    conn = connect_db()
    if not conn:
        return
    
    cur = conn.cursor()
    cur.execute("SELECT * FROM schedules")
    schedules = cur.fetchall()
    
    conn.close()
    
    if schedules:
        print(f"user found: {schedules}")
    else:
        print("user not found.")
# FUNCTIONS FOR FETCHING ALL TABLE DATA END
























if __name__ == "__main__":
    while True:
        # TEST RUNS

        # get_roles()
        get_inventory()
        # get_users()
        # get_reservations()
        # get_suppliers()
        # get_tables()
        # get_staffassignments()
        # get_schedules()

        # TEST RUNS

        print("\n1. Get user info")
        print("2. Insert new user")
        print("3. Update user info")
        print("4. Delete user")
        print("6. Find suplier by item name")
        print("7. Find suplier by item id")
        print("8. Order item by item id")
        print("9. Order item by item name")
        print("5. Exit")
        
        choice = input("Choose a number of function from  1 to 7: ")
        
        
        if choice == "1":
            userid = input("Enter user number: ")
            
            get_user_info(userid)

        elif choice == "2":
            userid = input("Enter user number: ")
            name = input("Enter user name: ")
            email = input("Enter user email: ")
            telephonenumber = input("Enter user phone number: ")
            author = input("Enter user authorization level (Staff or Admin): ")
            
            insert_user(userid, name, email, telephonenumber, author)

        elif choice == "3":
            userid = input("Enter user number to update: ")
            new_name = input("Enter new name: ")
            new_email = input("Enter new email: ")
            new_telephonenumber = input("Enter new phone number: ")
            new_author = input("Enter new user authorization level (Staff or Admin): ")
            
            update_user(userid, new_name, new_email, new_telephonenumber, new_author)

        elif choice == "4":
            userid = input("Enter user number to delete: ")
            
            delete_user(userid)

        elif choice == "6":
            itemname = input("Enter item name to find supplier: ")
            
            find_supplier(itemname)
        
        elif choice == "7":
            itemid = input("Enter item id to find supplier: ")
            
            find_supplier(itemid)

        elif choice == "8":
            itemid = input("Enter item number: ")
            q_order = input("Enter quantity to order: ")
            
            order_item(itemid, q_order)
        
        elif choice == "9":
            itemname = input("Enter item name: ")
            q_order = input("Enter quantity to order: ")
            
            order_item(itemname, q_order)


        elif choice == "5":
            print("Exiting program...")
            break

        else:
            print("Invalid choice. Please enter a number between 1-5.")

