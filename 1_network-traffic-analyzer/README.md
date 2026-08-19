# Network Traffic Analyzer

A Python-based network traffic analyzer that captures live packets and detects 
port scan activity in real time.

## What it does

- Captures live network traffic using Scapy
- Identifies TCP SYN packets — the building block of port scans
- Alerts when a single source IP hits more than 10 unique destination ports
- Logs all alerts with timestamps to `alerts.log`
- Distinguishes between normal outbound traffic and inbound scanning activity

## How port scan detection works

A port scan works by sending TCP SYN packets to many different ports on a target 
machine — the same first step used in tools like nmap to discover open services. 
This tool tracks how many unique destination ports each source IP has attempted 
to connect to within a session. When that count exceeds the threshold (default: 10), 
an alert fires and is written to the log file.

Normal traffic doesn't trigger this — a browser opening an HTTPS connection sends 
a SYN to port 443 repeatedly, but always the same port. A scanner hits hundreds 
of different ports in rapid succession.

## Demo

Tested against a real nmap SYN scan (`nmap -sS`) from a second device on the 
local network:
```
[2026-07-26 18:16:59] PORT SCAN DETECTED: 192.168.x.y -> 192.168.x.z
[2026-07-26 18:17:00] PORT SCAN DETECTED: 192.168.x.y -> 192.168.x.z
[2026-07-26 18:17:01] PORT SCAN DETECTED: 192.168.x.y -> 192.168.x.z
```
## Requirements

- Python 3.x
- Scapy: `pip install scapy`
- Npcap (Windows): download from npcap.com
- Run as Administrator (required for raw packet capture)

## Usage

```powershell
python analyzer.py
```

Set `VERBOSE = True` in the script to see individual SYN packets as they're detected.

## Note

This tool performs active packet capture while running; it does not run as a 
background service or persist between sessions. This is intentional for a learning 
context, rather than service/daemon implementation.
A production implementation would run as a persistent background 
service, log to a central SIEM, and integrate with alerting systems.

## Configuration

| Parameter | Default | Description |
|---|---|---|
| THRESHOLD | 10 | Number of unique ports before alert fires |
| VERBOSE | False | Print individual SYN packets |

## Author

Pavle Pavlović

Computer Technician

Electrical and Computer Engineering Student

University of Belgrade, School of Electrical Engineering
