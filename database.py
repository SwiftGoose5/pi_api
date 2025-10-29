import sqlite3
from datetime import datetime

DB_PATH = "data.db"

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
    
    cursor.execute("""
        INSERT INTO sensor_readings (sensor_type, value, timestamp)
        VALUES (?, ?, ?)
    """, (sensor_type, value, datetime.now().isoformat()))
    
    conn.commit()
    conn.close()

def get_recent_readings(sensor_type: str, limit: int = 10):
    """Get recent readings for a sensor"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT sensor_type, value, timestamp
        FROM sensor_readings
        WHERE sensor_type = ?
        ORDER BY timestamp DESC
        LIMIT ?
    """, (sensor_type, limit))
    
    results = cursor.fetchall()
    conn.close()
    
    return [{"sensor": r[0], "value": r[1], "timestamp": r[2]} for r in results]

if __name__ == "__main__":
    init_db()