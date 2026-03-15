# main.py
from github_tools import get_issues
from planner import create_plan
from executor import execute_plan
from logger import log_event
from github_submit import create_pull_request
from verifier import verify_fix
import json
import os

print("Agent Starting...")
log_event({"event": "agent_started", "agent": "AUTO_AGENT"})

# --------------------------
# Discover Issues
# --------------------------
issues = get_issues()
real_issues = [i for i in issues if "pull_request" not in i]

print("Real issues found:", len(real_issues))
log_event({"event": "issues_discovered", "count": len(real_issues)})

if len(real_issues) == 0:
    print("No real issues to process. Exiting.")
    exit()

# --------------------------
# Process Each Issue
# --------------------------
for issue in real_issues:
    print("Processing issue:", issue["number"], "-", issue["title"])
    log_event({"event": "issue_selected", "issue_number": issue["number"]})

    plan = create_plan(issue)
    log_event({"event": "plan_created", "issue": issue["number"], "steps": plan})

    result, branch_name = execute_plan(issue, plan)
    log_event({"event": "execution_complete", "issue": issue["number"], "status": result["status"], "branch": branch_name})

    verification = verify_fix(issue["number"])
    log_event({"event": "verification", "issue": issue["number"], "verified": verification["verified"]})

    if verification["verified"]:
        create_pull_request(issue["number"], branch_name)
        log_event({"event": "pull_request_created", "issue": issue["number"], "branch": branch_name})

print("Agent execution completed.")