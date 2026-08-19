import xml.etree.ElementTree as ET
from datetime import datetime
from collections import defaultdict
import sys

THRESHOLD = 5
TIME_WINDOW = 60  # seconds
NS = '{http://schemas.microsoft.com/win/2004/08/events/event}'
VERBOSE = False

login_attempts = defaultdict(list)

for filename in sys.argv[1:]:
    tree = ET.parse(filename)
    root = tree.getroot()

    events = list(root.findall(f'{NS}Event'))
    events.reverse()

    for event in events:
        event_id = event.find(f'{NS}System/{NS}EventID').text
        time_created = event.find(f'{NS}System/{NS}TimeCreated').get('SystemTime')
        computer = event.find(f'{NS}System/{NS}Computer').text
        target_username = event.find(f'{NS}EventData/{NS}Data[@Name="TargetUserName"]').text

        timestamp = datetime.fromisoformat(time_created.replace('Z', '+00:00'))
        

        if event_id == '4740':
            print(f"[{timestamp.strftime('%Y-%m-%d %H:%M:%S')}] ACCOUNT LOCKOUT DETECTED | User: {target_username} | Computer: {computer}")
            with open("alerts.log", "a") as f:
                f.write(f"[{timestamp.strftime('%Y-%m-%d %H:%M:%S')}] ACCOUNT LOCKOUT DETECTED | User: {target_username} | Computer: {computer}\n")

        elif event_id == '4625':
            login_attempts[target_username].append(timestamp)
            login_attempts[target_username] = [t for t in login_attempts[target_username] if (timestamp - t).total_seconds() < TIME_WINDOW]
            if len(login_attempts[target_username]) > THRESHOLD:
                print(f"[{timestamp.strftime('%Y-%m-%d %H:%M:%S')}] BRUTE FORCE DETECTED | User: {target_username} | {len(login_attempts[target_username])} attempts in {TIME_WINDOW}s")
                with open("alerts.log", "a") as f:
                    f.write(f"[{timestamp}] BRUTE FORCE DETECTED | User: {target_username} | {len(login_attempts[target_username])} attempts in {TIME_WINDOW}s\n")  

        if VERBOSE:
            print(f"EventID: {event_id} | TimeCreated: {timestamp} | Computer: {computer} | TargetUserName: {target_username}")