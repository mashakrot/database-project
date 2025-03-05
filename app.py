from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import psycopg2

app = FastAPI()

# Database connection
def get_db():
    return psycopg2.connect(
        dbname="restaurant_schedule",
        user="your_user",
        password="your_password",
        host="localhost",
        port="5432"
    )

# Authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@app.get("/schedule")
async def get_schedule(token: str = Depends(oauth2_scheme)):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT shift_date, start_time, end_time FROM schedules")
    schedule = cur.fetchall()
    cur.close()
    conn.close()
    return [{"date": row[0], "start": row[1], "end": row[2]} for row in schedule]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
