import sqlite3

conn = sqlite3.connect("data.db")
cur = conn.cursor()
cur.execute("DELETE FROM sensor_readings WHERE sensor_type = 'temperature'")
print(f"Deleted {cur.rowcount} old 'temperature' rows.")
conn.commit()
conn.close()