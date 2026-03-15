# github_submit.py
import requests
import time
from config import GITHUB_TOKEN, OWNER, REPO
from logger import log_event

HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds

def create_pull_request(issue_number, branch_name):
    """
    Create a pull request from branch_name to main/master.
    Retries if network/API errors occur.
    """
    pr_url = f"https://api.github.com/repos/{OWNER}/{REPO}/pulls"
    data = {
        "title": f"Auto Fix for Issue #{issue_number}",
        "head": branch_name,
        "base": "main",
        "body": f"Automated fix applied for issue #{issue_number}"
    }

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = requests.post(pr_url, headers=HEADERS, json=data)
            if response.status_code == 201:
                log_event({
                    "event": "pull_request_created",
                    "issue": issue_number,
                    "branch": branch_name,
                    "status": "success",
                    "retries": attempt - 1
                })
                print(f"Pull Request created successfully for issue {issue_number}")
                return True
            elif response.status_code == 422:
                # PR already exists or head invalid
                msg = response.json().get("message", "Unknown error")
                log_event({
                    "event": "pull_request_failed",
                    "issue": issue_number,
                    "branch": branch_name,
                    "status": "failed",
                    "reason": msg,
                    "retries": attempt - 1
                })
                print(f"PR creation failed: {msg}")
                return False
            else:
                raise Exception(f"Unexpected status code: {response.status_code}")
        except Exception as e:
            log_event({
                "event": "pull_request_retry",
                "issue": issue_number,
                "branch": branch_name,
                "attempt": attempt,
                "error": str(e)
            })
            print(f"Retry {attempt}/{MAX_RETRIES} due to error: {e}")
            time.sleep(RETRY_DELAY)

    log_event({
        "event": "pull_request_failed",
        "issue": issue_number,
        "branch": branch_name,
        "status": "failed_after_retries"
    })
    return False


def create_branch(branch_name, base="main"):
    """
    Create a branch from base. Auto-correct if branch exists.
    """
    ref_url = f"https://api.github.com/repos/{OWNER}/{REPO}/git/refs"
    data = {
        "ref": f"refs/heads/{branch_name}",
        "sha": get_latest_commit_sha(base)
    }

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = requests.post(ref_url, headers=HEADERS, json=data)
            if response.status_code == 201:
                log_event({
                    "event": "branch_created",
                    "branch": branch_name,
                    "status": "success",
                    "retries": attempt - 1
                })
                print(f"Branch created: {branch_name}")
                return True
            elif response.status_code == 422 and "Reference already exists" in response.text:
                log_event({
                    "event": "branch_exists",
                    "branch": branch_name,
                    "status": "skipped",
                    "retries": attempt - 1
                })
                print(f"Branch already exists: {branch_name}")
                return True
            else:
                raise Exception(f"Unexpected status code: {response.status_code}")
        except Exception as e:
            log_event({
                "event": "branch_retry",
                "branch": branch_name,
                "attempt": attempt,
                "error": str(e)
            })
            print(f"Retry {attempt}/{MAX_RETRIES} due to error: {e}")
            time.sleep(RETRY_DELAY)

    log_event({
        "event": "branch_failed",
        "branch": branch_name,
        "status": "failed_after_retries"
    })
    return False


def get_latest_commit_sha(branch="main"):
    """Fetch latest commit SHA from a branch"""
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/git/ref/heads/{branch}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()["object"]["sha"]
    else:
        raise Exception(f"Failed to fetch latest commit SHA: {response.status_code}")