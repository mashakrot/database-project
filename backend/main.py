import os
import jwt
from dotenv import load_dotenv
from datetime import datetime, timedelta
import bcrypt
from fastapi import FastAPI, APIRouter, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
from pydantic import BaseModel
from flask_cors import CORS

load_dotenv()

DB_NAME= "restaurant_db"
DB_USER="postgres"
DB_PASSWORD=1234
DB_HOST="localhost"
DB_PORT=5432
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=60
SECRET_KEY="SECRET_KEY"

app = FastAPI()
CORS(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




def connect_db():
    try:
        conn = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
        return conn
    except Exception as e:
        print("Database connection error:", e)
        return None

# Models
class LoginRequest(BaseModel):
    email: str
    password: str

class UserCreate(BaseModel):
    userid: int
    name: str
    email: str
    password: str
    telephonenumber: str
    author: str

class ReservationCreate(BaseModel):
    table_id: int
    customer_name: str
    telephone: str
    time_slot: str

class InventoryUpdate(BaseModel):
    item_id: int
    quantity: int


# TODO: check naming in database


# TODO:  there was also a phone number 
@app.post("/register")
def register_user(user: UserCreate):
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE email = %s", (user.email,))
    if cur.fetchone():
        raise HTTPException(status_code=400, detail="Email already registered")

    cur.execute("SELECT * FROM users WHERE telephonenumber = %s", (user.telephonenumber,))
    if cur.fetchone():
        raise HTTPException(status_code=400, detail="Phone number already registered")

    cur.execute("SELECT COALESCE(MAX(userid), 1000) + 1 FROM users")
    new_userid = cur.fetchone()[0]

    cur.execute("""
        INSERT INTO users (userid, name, email, password, telephonenumber, author) 
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (new_userid, user.name, user.email, user.password, user.telephonenumber, user.author))

    conn.commit()
    conn.close()

    return {"message": "User registered successfully", "userid": new_userid}



# Authentication
@app.post("/login")
def login_user(user: LoginRequest):
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("SELECT user_id, name, role, password FROM users WHERE email = %s", (user.email,))
    db_user = cur.fetchone()

    if not db_user or db_user[3] != user.password:  # ⚠️ No hashing check
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {"message": "Login successful", "user": {"id": db_user[0], "name": db_user[1], "role": db_user[2]}}


# Maybe use this and remove login, register to seperate file auth.py
# app.include_router(auth_router)


# TODO: remember last id for situations where we delete user and 

# User Management
@app.post("/users")
def create_user(user: UserCreate):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (userid, name, email, telephonenumber, author) VALUES (%s, %s, %s, %s, %s)", 
                (user.userid, user.name, user.email, user.telephonenumber, user.author))
    conn.commit()
    conn.close()
    return {"message": "User created successfully"}

@app.delete("/users/{userid}")
def delete_user(userid: int):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE userid = %s", (userid,))
    conn.commit()
    conn.close()
    return {"message": "User deleted successfully"}

# Reservations
@app.get("/reservations")
def get_reservations():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM reservations")
    reservations = cur.fetchall()
    conn.close()
    return [{"id": r[0], "customer_name": r[2], "table_id": r[1], "time_slot": r[5]} for r in reservations]

@app.post("/reservations")
def create_reservation(reservation: ReservationCreate):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO reservations (table_id, customer_name, telephone, time_slot) VALUES (%s, %s, %s, %s)", 
                (reservation.table_id, reservation.customer_name, reservation.telephone, reservation.time_slot))
    conn.commit()
    conn.close()
    return {"message": "Reservation created successfully"}

# Inventory
@app.put("/inventory")
def update_inventory(data: InventoryUpdate):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("UPDATE inventory SET quantity = %s WHERE item_id = %s", (data.quantity, data.item_id))
    conn.commit()
    conn.close()
    return {"message": "Inventory updated"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
