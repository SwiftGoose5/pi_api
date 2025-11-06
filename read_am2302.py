import time
import sqlite3
import Adafruit_DHT
from database import add_reading

# Sensor setup
SENSOR = Adafruit_DHT.AM2302
PIN = 17

DB_PATH = "/home/pi/Documents/api_project/data.db"
INTERVAL = 60  # seconds

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
            except sqlite3.OperationalError:
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
            f = round(temperature * 9/5 + 32, 1)
            h = round(humidity, 1)
            print(f"SUCCESS - Temp: {f}°F | Humidity: {h}%")
            add_reading("am2302_temperature", f)
            add_reading("am2302_humidity", h)
        else:
            print("FAILED - No data returned from sensor")

        time.sleep(INTERVAL)

except KeyboardInterrupt:
    print("\nStopping sensor readings...")
except Exception as e:
    print(f"Error: {e}")
