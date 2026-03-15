import requests
from config import GITHUB_TOKEN, OWNER, REPO

headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

def comment_issue(issue_number, message):
    """
    Adds a comment to the given GitHub issue.
    """
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/issues/{issue_number}/comments"
    data = {"body": message}
    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 201:
        print("Comment added to issue!")
    else:
        print("Comment failed:", response.json())


def close_issue(issue_number):
    """
    Closes the given GitHub issue.
    """
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/issues/{issue_number}"
    data = {"state": "closed"}
    response = requests.patch(url, json=data, headers=headers)

    if response.status_code == 200:
        print("Issue closed successfully!")
    else:
        print("Closing issue failed:", response.json())