import os
import time
import sqlite3
from database import add_reading

DB_PATH = "/home/elliot/Documents/api_project/data.db"
INTERVAL = 60

# Test database connection first
def wait_for_db(timeout=60):
    print("Waiting for database to be initialized...")
    for _ in range(timeout):
        if os.path.exists(DB_PATH):
            try:
                conn = sqlite3.connect(DB_PATH, timeout=1.0)
                conn.close()
                print("Database ready.")
                return True
            except sqlite3.OperationalError as e:
                print(f"DB connect error: {e}")
                pass
        time.sleep(1)
    print("Timeout: Database not available.")
    return False

# At start of script
if not wait_for_db():
    exit(1)

def get_cpu_temp_c():
    with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
        temp_millidegrees = int(f.read().strip())
    temp_c = temp_millidegrees / 1000.0
    return temp_c

if __name__ == "__main__":
    print("Starting CPU temperature logger...")
    while True:
        try:
            temp_c = get_cpu_temp_c()
            print(f"CPU Temp: {temp_c}°C")
            add_reading("cpu_temperature", temp_c)
        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()
        time.sleep(INTERVAL)