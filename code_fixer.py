import requests
import base64
from config import GITHUB_TOKEN, OWNER, REPO

headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

def apply_fix(issue_number, branch_name):
    """
    Applies fix to README.md on the specified branch.
    Creates branch if it does not exist.
    """

    file_path = "README.md"

    # Get latest commit SHA of main branch
    url_ref = f"https://api.github.com/repos/{OWNER}/{REPO}/git/ref/heads/main"
    ref_res = requests.get(url_ref, headers=headers).json()
    main_sha = ref_res["object"]["sha"]

    # Create branch
    url_branch = f"https://api.github.com/repos/{OWNER}/{REPO}/git/refs"
    branch_data = {
        "ref": f"refs/heads/{branch_name}",
        "sha": main_sha
    }
    branch_res = requests.post(url_branch, json=branch_data, headers=headers)
    if branch_res.status_code in [201, 422]:  # 422 if branch exists
        print(f"Branch created: {branch_name}")
    else:
        print("Branch creation failed:", branch_res.json())

    # Get latest file version
    url_file = f"https://api.github.com/repos/{OWNER}/{REPO}/contents/{file_path}?ref=main"
    file_res = requests.get(url_file, headers=headers).json()

    content = base64.b64decode(file_res["content"]).decode()
    sha = file_res["sha"]

    # Update file content
    new_content = content + f"\n\nFix applied automatically for issue #{issue_number}\n"
    encoded = base64.b64encode(new_content.encode()).decode()

    commit_data = {
        "message": f"Auto fix for issue #{issue_number}",
        "content": encoded,
        "sha": sha,
        "branch": branch_name
    }

    commit_url = f"https://api.github.com/repos/{OWNER}/{REPO}/contents/{file_path}"
    commit_res = requests.put(commit_url, json=commit_data, headers=headers)

    if commit_res.status_code in [200, 201]:
        print("Code fix committed successfully!")
    else:
        print("GitHub API error:", commit_res.json())