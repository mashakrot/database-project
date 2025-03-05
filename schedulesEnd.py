from flask import Flask, jsonify, request
import psycopg2 
from flask_cors import CORS
from datetime import time

app = Flask(__name__)
CORS(app)

def connect_db():
    try:
        conn = psycopg2.connect(
            dbname="restaurant_schedule",
            user="your_user",
            password="your_password",
            host="localhost",
            port="5432"
        )
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None

# Function to get staff schedules from the database
def get_schedules():
    conn = connect_db()
    if not conn:
        return None
    
    cur = conn.cursor()
    cur.execute("SELECT * FROM schedules")
    schedules = cur.fetchall() 
    
    conn.close()
    
    schedules_list = []
    for schedule in schedules:
        schedules_list.append({
            "scheduleid": schedule[0],
            "userid": schedule[1],
            "shiftdate": schedule[2],
            "timeslot": schedule[3].strftime('%H:%M:%S') if isinstance(schedule[3], time) else schedule[3],
            "approvalstatus": schedule[4]
        })
    
    return schedules_list


@app.route('/get_schedules', methods=['POST'])
def handle_get_schedules():
    schedules = get_schedules()
    if schedules:
        return jsonify({"status": "success", "schedules": schedules})
    else:
        return jsonify({"status": "error", "message": "No schedules found"}), 404



# TODO: check if this post routes are working in schedules 
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
        """
        
        cur.execute(insert_query, (userid, shiftdate, timestart, timeend, approvalstatus))
        
        conn.commit()
        
        if cur.rowcount > 0:
            response = {"status": "success", "message": "Shift added successfully"}
        else:
            response = {"status": "error", "message": "Failed to add shift"}
        
        cur.close()
        conn.close()
        
        return jsonify(response)
    
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
    
    
    
@app.route('/change_shift_status', methods=['POST'])
def change_shift_status():
    data = request.get_json()
    
    scheduleid = data.get('scheduleid')
    approvalstatus = data.get('approvalstatus') 
    userid = data.get('userid')

    try:
        conn = connect_db()
        cur = conn.cursor()
        
        cur.execute("SELECT author FROM users WHERE userid = %s", (userid,))
        user = cur.fetchone()
        
        if user and user[0] == 'admin': 
            update_query = """
            UPDATE schedules
            SET approvalstatus = %s
            WHERE scheduleid = %s
            """
            
            cur.execute(update_query, (approvalstatus, scheduleid))
            
            conn.commit()
            
            if cur.rowcount > 0:
                response = {"status": "success", "message": f"Shift status updated to {approvalstatus}"}
            else:
                response = {"status": "error", "message": "Shift not found"}
        else:
            response = {"status": "error", "message": "User is not authorized to change the shift status"}

        cur.close()
        conn.close()

        return jsonify(response)

    except Exception as e:
        print(f"Error changing shift status: {e}")
        return jsonify({"status": "error", "message": "Error changing shift status"})


if __name__ == '__main__':
    app.run(debug=True)
