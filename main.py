'use strict';
import psycopg2

DB_NAME = "student"
DB_USER = "postgres"
DB_PASSWORD = "makro2004"
DB_HOST = "localhost"
DB_PORT = "5432"


def connect_db():
    try:
        conn = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
        print("connection done")
        return conn
    
    
    except Exception as e:
        print("Error connecting to database:", e)
        return None
    

def get_student_info(sno):
    conn = connect_db()
    if not conn:
        return
    
    cur = conn.cursor()
    cur.execute("SELECT * FROM student WHERE sno = %s", (sno,))
    student = cur.fetchone()
    
    conn.close()
    
    if student:
        
        print(f"Student found: {student}")
    else:
        print("Student not found.")
    
    
def insert_student(sno, sname, sage, sgender, sdept):
    conn = connect_db()
    if not conn:
        return
    cur = conn.cursor()
    

    cur.execute("SELECT * FROM student WHERE sno = %s", (sno,))
    if cur.fetchone():

        print("Student number already exists. Try again")
        conn.close()
        return
    
    cur.execute("""
        INSERT INTO student (sno, sname, sage, sgender, sdept) 
        VALUES (%s, %s, %s, %s, %s)
    """, (sno, sname, sage, sgender, sdept))

    
    conn.commit()

    print("We added student successfully")
    conn.close()


def update_student(sno, new_sname, new_sage, new_sgender, new_sdept):
    conn = connect_db()
    if not conn:
        return
    cur = conn.cursor()
    
    
    cur.execute("SELECT * FROM student WHERE sno = %s", (sno,))

    student = cur.fetchone()
    
    if not student:
        print("Student not found")
        conn.close()
        return
    
    print(f"Current Student Data: {student}")
    
    cur.execute("""
        UPDATE student 
        SET sname = %s, sage = %s, sgender = %s, sdept = %s 
        WHERE sno = %s
    """, (new_sname, new_sage, new_sgender, new_sdept, sno)) 
    
    conn.commit()
    
    print("Student updated successfully!")
    conn.close()
    

def delete_student(sno):
    conn = connect_db()
    if not conn:
        return
    cur = conn.cursor()
    
    
    cur.execute("SELECT * FROM sc WHERE sno = %s", (sno,))
    if cur.fetchone():
        print("Student is enrolled in courses. Deleting enrollments first...")
        cur.execute("DELETE FROM sc WHERE sno = %s", (sno,))
    


    cur.execute("DELETE FROM student WHERE sno = %s", (sno,))
    conn.commit()
    print("Student deleted successfully!")
    conn.close()
    
    
if __name__ == "__main__":
    while True:
        print("\n1. Get student info")
        print("2. Insert new student")
        print("3. Update student info")
        print("4. Delete student")
        print("5. Exit")
        
        choice = input("Choose a number of function from  1 to 5: ")
        
        
        if choice == "1":
            sno = input("Enter student number: ")
            
            get_student_info(sno)

        elif choice == "2":
            sno = input("Enter student number: ")
            sname = input("Enter student name: ")
            sage = int(input("Enter student age: "))
            sgender = input("Enter student gender (M/F): ")
            sdept = input("Enter student department: ")
            
            insert_student(sno, sname, sage, sgender, sdept)

        elif choice == "3":
            sno = input("Enter student number to update: ")
            new_sname = input("Enter new name: ")
            new_sage = int(input("Enter new age: "))
            
            new_sgender = input("Enter new gender (M/F): ")
            new_sdept = input("Enter new department: ")
            
            update_student(sno, new_sname, new_sage, new_sgender, new_sdept)

        elif choice == "4":
            sno = input("Enter student number to delete: ")
            
            delete_student(sno)

        elif choice == "5":
            print("Exiting program...")
            break

        else:
            print("Invalid choice. Please enter a number between 1-5.")