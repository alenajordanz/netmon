# NetMon — Network Device Discovery Tool

A lightweight tool that scans your local network, identifies connected devices, and displays them in a simple web dashboard. Built as a way to repurpose an old desktop into a useful home network utility.

## What it does

- Scans the local network using ARP requests to discover active devices
- Identifies each device's manufacturer using MAC address (OUI) lookups
- Stores device history (first seen / last seen) in a local SQLite database
- Exposes a REST API to query discovered devices
- Displays results in a clean, styled web dashboard with a manual scan trigger

## Tech Stack

- **Python** — core scanning and API logic
- **Scapy** — ARP-based network scanning
- **FastAPI** — REST API layer
- **SQLite** — lightweight local storage
- **HTML/CSS/JavaScript** — frontend dashboard
- **Docker + Docker Compose** — containerized deployment

## How it works

1. The scanner sends ARP requests across the local subnet (e.g. `192.168.1.0/24`)
2. Responding devices are matched against a MAC vendor database to identify manufacturers
3. Results are stored in SQLite, tracking when each device was first and last seen
4. The FastAPI backend exposes this data via `/devices` (GET) and triggers new scans via `/scan` (POST)
5. A simple frontend dashboard displays the device list and lets you trigger scans manually

## Running it

```bash
docker compose up --build -d
```

The dashboard will be available at `http://<your-server-ip>:8000/`

**Note:** Because ARP scanning requires direct access to the host's network interface, this runs with `network_mode: host` in Docker Compose.

## Project Status

This is an early-stage personal project. Current scope is limited to device discovery (IP, MAC, vendor, and timestamps). Planned future additions include:

- Alerting via Discord/webhook when new devices join the network
- Basic anomaly/intrusion detection

## Why I built this

I wanted a hands-on way to learn network scanning fundamentals, containerization, and API design — while repurposing an old OptiPlex desktop instead of letting it sit unused.
