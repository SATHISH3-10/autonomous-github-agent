# logger.py
import json
import os
from datetime import datetime

LOG_FILE = "logs/agent_log.json"

def log_event(event):
    """
    Logs events with timestamp, retries, status, and errors.
    """
    event["timestamp"] = str(datetime.now())
    if "status" not in event:
        event["status"] = "pending"
    if "retries" not in event:
        event["retries"] = 0
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    if not os.path.exists(LOG_FILE):
        logs = []
    else:
        try:
            with open(LOG_FILE, "r") as f:
                logs = json.load(f)
        except:
            logs = []
    logs.append(event)
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=4)
    print("LOG:", event)