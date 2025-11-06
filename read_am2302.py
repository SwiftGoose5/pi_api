import time
import Adafruit_DHT
from database import init_db, add_reading

# Sensor setup
SENSOR = Adafruit_DHT.AM2302
PIN = 17
INTERVAL = 10

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
            add_reading("AM2302 °F", f)
            add_reading("AM2302 %H", h)
        else:
            print("FAILED - No data returned from sensor")

        time.sleep(INTERVAL)

except KeyboardInterrupt:
    print("\nStopping sensor readings...")
except Exception as e:
    print(f"Error: {e}")
