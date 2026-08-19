# Windows Log Analyzer

A learning project demonstrating Windows Security Event Log analysis in Python. 
Parses exported XML log files and applies detection rules for common attack 
patterns. Implemented from scratch to understand the underlying mechanics.

## What it detects

| Event ID | Event Name | Detection Logic |
|---|---|---|
| 4625 | Failed Logon | Alerts when same username exceeds threshold of failed logins within time window |
| 4740 | Account Lockout | Any single lockout event is immediately flagged |

## How detection works

### Brute Force (4625)
Each failed login attempt is recorded with a timestamp per username. If the same 
username accumulates more than THRESHOLD failed logins within TIME_WINDOW seconds, 
a brute force alert fires. This distinguishes normal occasional typos from 
automated password guessing attacks.

### Account Lockout (4740)
Any single Event ID 4740 is immediately suspicious; Windows locks an account due to too many failed attempts.

## Requirements

- Python 3.x
- Windows Security Event Log exported as XML (via Event Viewer)

## Usage
`python3 log_analyzer.py security_log.xml lockout_log.xml`

Multiple log files can be passed as arguments and are processed sequentially.
Alerts are printed to stdout and saved to `alerts.log`.

## Note

This tool processes exported XML log files (via Windows Event Viewer) rather than 
reading live logs directly. It keeps the focus on detection logic rather than Windows API integration. A production 
implementation would use `pywin32` to read the Security log in real time.

## Configuration

| Parameter | Default | Description |
|---|---|---|
| THRESHOLD | 5 | Number of failed logins before brute force alert fires |
| TIME_WINDOW | 60 | Time window in seconds within which failures are counted |
| VERBOSE | False | When True, prints each parsed event to stdout |

## Tested against

Generated real Windows Security events on a local machine:
- 25 failed login attempts against a test account (Event ID 4625)
- 1 account lockout event after threshold exceeded (Event ID 4740)

## Author

Pavle Pavlović — Electrical & Computer Engineering Student, University of Belgrade
