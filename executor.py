# executor.py
import time
from github_tools import create_branch, apply_fix, comment_issue, close_issue
from logger import log_event

MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds

def execute_plan(issue, plan):
    """
    Execute the plan for a given GitHub issue.
    Returns a result dict and the branch name.
    """
    issue_number = issue["number"]
    branch_name = f"agent-fix-issue-{issue_number}"
    result = {"status": "pending"}

    log_event({"event": "execution_started", "issue": issue_number, "branch": branch_name, "status": "pending", "retries": 0})

    # 1️⃣ Create branch with retries
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            create_branch(branch_name)
            log_event({"event": "branch_created", "issue": issue_number, "branch": branch_name, "status": "success", "retries": attempt-1})
            print(f"Branch created: {branch_name}")
            break
        except Exception as e:
            log_event({"event": "branch_creation_failed", "issue": issue_number, "branch": branch_name, "error": str(e), "retries": attempt})
            print(f"Branch creation failed (Attempt {attempt}): {e}")
            time.sleep(RETRY_DELAY)
            if attempt == MAX_RETRIES:
                result["status"] = "failed_branch"
                return result, branch_name  # Stop execution if branch creation fails

    # 2️⃣ Apply each plan step
    for step in plan:
        print(f"Executing step: {step}")
        log_event({"event": "step_started", "issue": issue_number, "step": step})
        # Simulate execution (replace with actual code logic if needed)
        time.sleep(0.5)
        log_event({"event": "step_completed", "issue": issue_number, "step": step})

    # 3️⃣ Apply fix with retries
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            apply_fix(issue_number, branch_name)
            log_event({"event": "fix_applied", "issue": issue_number, "branch": branch_name, "status": "success", "retries": attempt-1})
            print("Code fix committed successfully!")
            break
        except Exception as e:
            log_event({"event": "fix_failed", "issue": issue_number, "branch": branch_name, "error": str(e), "retries": attempt})
            print(f"Fix commit failed (Attempt {attempt}): {e}")
            time.sleep(RETRY_DELAY)
            if attempt == MAX_RETRIES:
                result["status"] = "failed_fix"
                return result, branch_name

    # 4️⃣ Comment and close issue
    try:
        comment_issue(issue_number, f"Fix applied automatically on branch `{branch_name}`")
        log_event({"event": "comment_added", "issue": issue_number, "branch": branch_name})
        close_issue(issue_number)
        log_event({"event": "issue_closed", "issue": issue_number, "branch": branch_name})
        print(f"Issue {issue_number} closed successfully!")
    except Exception as e:
        log_event({"event": "comment_close_failed", "issue": issue_number, "error": str(e)})

    result["status"] = "fix_generated"
    return result, branch_name