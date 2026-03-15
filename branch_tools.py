import requests
from config import GITHUB_TOKEN, OWNER, REPO

headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

def create_branch(branch_name):

    # Get latest commit SHA from main
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/git/ref/heads/main"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Failed to fetch main branch")
        return None

    sha = response.json()["object"]["sha"]

    # Create new branch
    data = {
        "ref": f"refs/heads/{branch_name}",
        "sha": sha
    }

    url = f"https://api.github.com/repos/{OWNER}/{REPO}/git/refs"
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 201:
        print("Branch created:", branch_name)
        return branch_name
    else:
        print("Branch creation failed:", response.json())
        return None