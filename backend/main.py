from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from db import get_all_devices, init_db
from scanner import scan_network

app = FastAPI(title="NetMon API")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.on_event("startup")
def startup():
    init_db()

@app.get("/")
def root():
    return FileResponse("static/index.html")

@app.get("/devices")
def list_devices():
    rows = get_all_devices()
    return [
        {
            "mac_address": r[0],
            "ip_address": r[1],
            "vendor": r[2],
            "first_seen": r[3],
            "last_seen": r[4]
        }
        for r in rows
    ]

@app.post("/scan")
def trigger_scan():
    devices = scan_network()
    return {"found": len(devices), "devices": devices}
