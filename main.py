from fastapi import FastAPI
from fastapi import Security, HTTPException
from fastapi.security import APIKeyHeader
import subprocess
import os 

app = FastAPI()

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
    return {"temperature_celsius": temp_celsius}


@app.get("/uptime")
def get_uptime():
    result = subprocess.run(['uptime', '-p'], capture_output=True, text=True)
    temp_str = result.stdout.strip()
    temp_value = temp_str.split('up')[1]
    return {"uptime": temp_value}

@app.post("/log")
def log_message(message: str, key: str = Security(api_key_header)):
    with open("api_log.txt", "a") as f:
        f.write(f"{message}\n")
    return {"status": "logged", "message": message}
