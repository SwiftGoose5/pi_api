import sqlite3
from datetime import datetime
import pytz

DB_PATH = "/home/elliot/Documents/api_project/data.db"
local_tz = pytz.timezone("America/New_York")

def init_db():
    """Create tables if they don't exist"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create sensor_readings table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sensor_readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sensor_type TEXT NOT NULL,
            value REAL NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)
    
    conn.commit()
    conn.close()
    print("Database initialized!")

def add_reading(sensor_type: str, value: float):
    """Insert a sensor reading"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Use LOCAL time
    local_time = datetime.now(local_tz)
    timestamp = local_time.strftime("%Y-%m-%dT%H:%M:%S.%f")
    
    cursor.execute("""
        INSERT INTO sensor_readings (sensor_type, value, timestamp)
        VALUES (?, ?, ?)
    """, (sensor_type, value, timestamp))
    
    conn.commit()
    conn.close()

def get_single_reading(sensor_type: str):
    """Get single reading for a sensor"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    limit = 1
    
    cursor.execute("""
        SELECT sensor_type, value, timestamp
        FROM sensor_readings
        WHERE sensor_type = ?
        ORDER BY timestamp DESC
        LIMIT ?
    """, (sensor_type, limit))
    
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return {"sensor": row[0], "value": row[1], "timestamp": row[2]}
    else:
        return None

def get_recent_readings(sensor_type: str, limit: int = 10) -> list[dict]:
    """Get recent readings for a sensor (latest first)"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT value, timestamp
        FROM sensor_readings
        WHERE sensor_type = ?
        ORDER BY timestamp DESC
        LIMIT ?
    """, (sensor_type, limit))
    
    results = cursor.fetchall()
    conn.close()
    
    return [
        {"value": round(r[0], 1), "timestamp": r[1]}
        for r in results
    ]

if __name__ == "__main__":
    init_db()