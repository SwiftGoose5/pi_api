import os
import time
import sqlite3
import Adafruit_DHT
from database import add_reading

# Sensor setup
SENSOR = Adafruit_DHT.AM2302
PIN = 17

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

print("Starting AM2302 sensor readings...")
print(f"Sensor type: AM2302, Pin: GPIO{PIN}")

try:
    while True:
        print("Attempting to read sensor...")
        humidity, temperature = Adafruit_DHT.read_retry(SENSOR, PIN, retries=15, delay_seconds=INTERVAL)

        if humidity is not None and temperature is not None:
            temp_c = round(temperature, 1)
            hum = round(humidity, 1)
            print(f"SUCCESS - Temp: {temp_c}°C | Humidity: {hum}%")
            add_reading("am2302_temperature", temp_c)
            add_reading("am2302_humidity", hum)
        else:
            print("FAILED - No data returned from sensor")

        time.sleep(INTERVAL)

