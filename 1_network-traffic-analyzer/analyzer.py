from scapy.all import sniff, IP, TCP
from collections import defaultdict
import time
from datetime import datetime

scan_tracker = defaultdict(lambda: defaultdict(set))
THRESHOLD = 10 
VERBOSE = False

def process_packet(packet):
    if IP in packet and TCP in packet:
        print(f"{packet[IP].src} -> {packet[IP].dst} | Protocol: {packet[IP].proto}")
    
        if packet[TCP].flags == 'S':
            if VERBOSE:
                print(f"  SYN detected: {packet[IP].src} -> {packet[IP].dst}:{packet[TCP].dport}")
            
            src = packet[IP].src
            dst = packet[IP].dst
            dport = packet[TCP].dport

            scan_tracker[src][dst].add(dport)

            if len(scan_tracker[src][dst]) > THRESHOLD:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"[{timestamp}] PORT SCAN DETECTED: {src} -> {dst} | {len(scan_tracker[src][dst])} ports hit")
                
                with open("alerts.log", "a") as f:
                    f.write(f"[{timestamp}] PORT SCAN DETECTED: {src} -> {dst}\n")

                scan_tracker[src][dst].clear()
                
sniff(prn=process_packet, count=200)