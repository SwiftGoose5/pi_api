from fastapi import FastAPI, Security, HTTPException, Request
from fastapi.security import APIKeyHeader
import subprocess
import os
import logging
from database import init_db, add_reading, get_latest_reading, get_readings

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI()

# Log all incoming requests
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"{request.method} {request.url.path} - Client: {request.client.host}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response

# Initialize DB on startup
@app.on_event("startup")
def startup():
    # This runs when Docker container starts
    if not os.path.exists("/app/data.db"):
        print("Database not found — initializing...")
        init_db()  # creates table + schema
    else:
        print("Database found — ready to serve.")

API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY environment variable not set!")

api_key_header = APIKeyHeader(name="X-API-Key")

def verify_api_key(key: str = Security(api_key_header)):
    if key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")
    return key

@app.get("/uptime")
def get_uptime():
    result = subprocess.run(['uptime', '-p'], capture_output=True, text=True)
    temp_str = result.stdout.strip()
    temp_value = temp_str.split('up')[1]
    return {"uptime": temp_value}

@app.get("/cpu-temperature")
def get_cpu_temperature():
    reading = get_latest_reading("cpu_temperature")

    if not reading:
        return {"error": "No CPU temperature reading"}
    
    c = reading["value"]
    f = round(c * 9/5 + 32, 1)

    return {
        "sensor": reading["sensor"],
        "temperature_c": c,
        "temperature_f": f,
        "timestamp": reading["timestamp"]
    }

@app.get("/cpu-temperature/history")
def get_cpu_temperature_history(unit: str = "f", limit: int = 10):
    unit = unit.lower()
    if unit not in ("c", "f"): 
        raise HTTPException(400, "unit must be 'c' or 'f'")
    
    if limit < 1 or limit > 100:
        limit = 10

    readings = get_readings("cpu_temperature", unit, limit)

    if not readings:
        return {"error": "No temperature readings found"}

    return {
        "sensor": "cpu_temperature",
        "unit": "°C" if unit == "c" else "°F",
        "count": len(readings),
        "readings": readings
    }

@app.get("/am2302/temperature/")
def get_am2302_temperature():
    reading = get_latest_reading("am2302_temperature")

    if not reading:
        return {"error": "No temperature reading found"}
    
    c = reading["value"]
    f = round(c * 9/5 + 32, 1)
    
    return {
        "sensor": reading["sensor"],
        "temperature_c": c,
        "temperature_f": f,
        "timestamp": reading["timestamp"]
    }

@app.get("/am2302/temperature/history")
def get_am2302_temperature_history(unit: str = "f", limit: int = 10):
    unit = unit.lower()
    if unit not in ("c", "f"): 
        raise HTTPException(400, "unit must be 'c' or 'f'")
    
    if limit < 1 or limit > 100:
        limit = 10  # clamp to safe range

    readings = get_readings("am2302_temperature", unit, limit)

    if not readings:
        return {"error": "No temperature readings found"}
    
    return {
        "sensor": "am2302_temperature",
        "unit": "°C" if unit == "c" else "°F",
        "count": len(readings),
        "readings": readings
    }

@app.get("/am2302/humidity/")
def get_am2302_humidity():
    reading = get_latest_reading("am2302_humidity")

    if not reading:
        return {"error": "No humidity reading found"}
    
    humidity = reading["value"]
    
    return {
        "sensor": reading["sensor"],
        "humidity": humidity,
        "timestamp": reading["timestamp"]
    }

@app.post("/log")
def log_message(message: str, api_key: str = Security(verify_api_key)):
    add_reading("log_message", 0.0)  # We'll improve this later
    return {"status": "logged", "message": message}