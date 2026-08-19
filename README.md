# SOC Toolkit

A collection of Python-based blue team security tools built as a self-directed 
learning project. Each tool addresses a 
different layer of threat detection; from live network monitoring to log analysis 
to automated threat intelligence enrichment.

## Tools

### [01 — Network Traffic Analyzer](01_network_analyzer/)
Real-time packet capture and port scan detection using Scapy. Monitors live 
network traffic and alerts when a single source IP hits more than 10 unique 
destination ports within a session.

### [02 — Windows Log Analyzer](02_windows_log_analyzer/)
Parses exported Windows Security Event Log XML files and detects brute force 
attacks (Event ID 4625) and account lockouts (Event ID 4740) using time-window 
based analysis.

### [03 — Correlation Engine](03_correlation_engine/) *(in development)*
Reads alert logs produced by Tools 01 and 02 and correlates them to detect 
multi-stage attack chains. For example, a port scan followed by a brute force 
attempt followed by an account lockout.

### [04 — Threat Intelligence Dashboard](04_threat_intelligence/) *(in development)*
Automatically enriches suspicious IP addresses found in alert logs by querying 
public threat intelligence APIs (VirusTotal, AbuseIPDB, Shodan) and producing 
structured investigation reports.

## How the tools connect

Tools 01 and 02 each produce timestamped `alerts.log` files. Tool 03 reads 
those logs and correlates events across both sources within configurable time 
windows. IP addresses extracted from correlated alerts are then passed to Tool 04 
for automated enrichment.

## Requirements

- Python 3.x
- Scapy (`pip install scapy`) — Tool 01 only
- Npcap (Windows) — Tool 01 only
- 
## Author

Pavle Pavlović — Electrical & Computer Engineering Student  
University of Belgrade, School of Electrical Engineering  
