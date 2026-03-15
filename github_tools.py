import requests
from config import GITHUB_TOKEN, OWNER, REPO
import json
import time

headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

BASE_URL = f"https://api.github.com/repos/{OWNER}/{REPO}"

# ------------------------------
# 1️⃣ Get Issues
# ------------------------------
def get_issues():
    url = f"{BASE_URL}/issues"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Error fetching issues:", response.status_code)
        return []

    issues = response.json()
    real_issues = []

    print("Total Issues Returned:", len(issues))
    print("-"*40)

    for issue in issues:
        is_pr = "pull_request" in issue
        print(f"Number: {issue['number']} | Title: {issue.get('title')} | Is PR: {is_pr}")
        if not is_pr:
            real_issues.append(issue)

    print("-"*40)
    print("Real issues found:", len(real_issues))
    return real_issues

# ------------------------------
# 2️⃣ Create Branch
# ------------------------------
def create_branch(branch_name):
    # Get SHA of main branch
    url = f"{BASE_URL}/git/ref/heads/main"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    sha = response.json()["object"]["sha"]

    # Create branch
    data = {"ref": f"refs/heads/{branch_name}", "sha": sha}
    url = f"{BASE_URL}/git/refs"
    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code in [201, 422]:  # 422 = branch exists
        return True
    response.raise_for_status()

# ------------------------------
# 3️⃣ Apply Fix / Commit File
# ------------------------------
def apply_fix(issue_number, branch_name):
    file_path = "README.md"  # Example, modify per your fix logic
    url = f"{BASE_URL}/contents/{file_path}?ref={branch_name}"

    # Get current file SHA
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    sha = resp.json()["sha"]

    content = f"# Auto Fix for Issue #{issue_number}\n"

    data = {
        "message": f"Fix for issue #{issue_number}",
        "content": content.encode("utf-8").decode("utf-8"),
        "branch": branch_name,
        "sha": sha
    }

    response = requests.put(url, headers=headers, data=json.dumps(data))
    response.raise_for_status()
    return True

# ------------------------------
# 4️⃣ Comment on Issue
# ------------------------------
def comment_issue(issue_number, comment):
    url = f"{BASE_URL}/issues/{issue_number}/comments"
    data = {"body": comment}
    response = requests.post(url, headers=headers, data=json.dumps(data))
    response.raise_for_status()
    return True

# ------------------------------
# 5️⃣ Close Issue
# ------------------------------
def close_issue(issue_number):
    url = f"{BASE_URL}/issues/{issue_number}"
    data = {"state": "closed"}
    response = requests.patch(url, headers=headers, data=json.dumps(data))
    response.raise_for_status()
    return True