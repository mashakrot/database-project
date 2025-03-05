from flask import Flask, jsonify, request
import psycopg2
from flask_cors import CORS
from datetime import time
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Database connection
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

# Function to get staff schedules from the database
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



if __name__ == '__main__':
    app.run(debug=True)
