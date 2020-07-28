import sqlite3

conn = sqlite3.connect('db/user_status.db')
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS  users 
    (user_id TEXT, isvote INT)
    """)

usrid = "502121096271757333"

a = cursor.execute(f"SELECT isvote FROM users WHERE user_id={usrid}")
if "0" in str(a.fetchone()):
	print(123)

conn.commit()