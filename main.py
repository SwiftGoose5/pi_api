from fastapi import FastAPI, Security, HTTPException
from fastapi.security import APIKeyHeader
import subprocess
import os
from database import init_db, add_reading, get_recent_readings

app = FastAPI()

# Initialize DB on startup
@app.on_event("startup")
def startup():
    init_db()

API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY environment variable not set!")

api_key_header = APIKeyHeader(name="X-API-Key")

def verify_api_key(key: str = Security(api_key_header)):
    if key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")
    return key

@app.get("/temperature")
def get_temp():
    with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
        temp_millidegrees = int(f.read().strip())
    temp_celsius = temp_millidegrees / 1000.0
    
    add_reading("temperature", temp_celsius)
    
    return {"temperature_celsius": temp_celsius}

@app.get("/uptime")
def get_uptime():
    result = subprocess.run(['uptime', '-p'], capture_output=True, text=True)
    temp_str = result.stdout.strip()
    temp_value = temp_str.split('up')[1]
    return {"uptime": temp_value}

@app.get("/temperature/history")
def get_temp_history(limit: int = 10):
    readings = get_recent_readings("temperature", limit)
    return {"readings": readings}

@app.post("/log")
def log_message(message: str, api_key: str = Security(verify_api_key)):
    add_reading("log_message", 0.0)  # We'll improve this later
    return {"status": "logged", "message": message}