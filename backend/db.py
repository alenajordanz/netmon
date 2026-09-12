import sqlite3
from datetime import datetime

DB_PATH = "netmon.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS devices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mac_address TEXT UNIQUE NOT NULL,
            ip_address TEXT,
            vendor TEXT,
            first_seen TEXT,
            last_seen TEXT
        )
    """)
    conn.commit()
    conn.close()

def upsert_device(mac, ip, vendor):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    now = datetime.now().isoformat()
    cursor.execute("SELECT id FROM devices WHERE mac_address = ?", (mac,))
    existing = cursor.fetchone()
    if existing:
        cursor.execute(
            "UPDATE devices SET ip_address = ?, vendor = ?, last_seen = ? WHERE mac_address = ?",
            (ip, vendor, now, mac)
        )
    else:
        cursor.execute(
            "INSERT INTO devices (mac_address, ip_address, vendor, first_seen, last_seen) VALUES (?, ?, ?, ?, ?)",
            (mac, ip, vendor, now, now)
        )
    conn.commit()
    conn.close()

def get_all_devices():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT mac_address, ip_address, vendor, first_seen, last_seen FROM devices")
    rows = cursor.fetchall()
    conn.close()
    return rows

if __name__ == "__main__":
    init_db()
    print("Database initialized.")
