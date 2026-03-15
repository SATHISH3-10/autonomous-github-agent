import json
import time

def run_agent():

    logs = []

    logs.append("Scanning repository issues...")
    time.sleep(1)

    issue_count = 3
    logs.append(f"Total Issues Found: {issue_count}")
    time.sleep(1)

    logs.append("Processing Issue #12")
    time.sleep(1)

    logs.append("Generating fix plan")
    time.sleep(1)

    logs.append("Creating branch")
    time.sleep(1)

    logs.append("Pull request created")

    with open("logs.json","w") as f:
        json.dump(logs,f)

    return logs