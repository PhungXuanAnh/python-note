import requests


def list_commits_on_pull_request(owner, repo, pr_id, gh_token) -> list:
    """
        Reference: https://docs.github.com/en/rest/pulls/pulls?apiVersion=2022-11-28#list-commits-on-a-pull-request
        curl -L \
            -H "Accept: application/vnd.github+json" \
            -H "Authorization: Bearer <YOUR-TOKEN>" \
            -H "X-GitHub-Api-Version: 2022-11-28" \
            https://api.github.com/repos/OWNER/REPO/pulls/PULL_NUMBER/commits
    """
    resp = requests.get(
        url=f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_id}/commits",
        headers={
            "Authorization": f"Bearer {gh_token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    if resp.status_code != 200:
        print(resp.json())
        return []
    return resp.json()


def get_latest_commit(owner, repo, pr_id, gh_token):
    commits = list_commits_on_pull_request(owner, repo, pr_id, gh_token)
    if not commits:
        return None
    return commits[-1]


def get_commit_status(owner, repo, commit_sha, gh_token) -> dict:
    """
        Reference: https://docs.github.com/en/rest/pulls/pulls?apiVersion=2022-11-28#list-commits-on-a-pull-request
        curl -L \
            -H "Accept: application/vnd.github+json" \
            -H "Authorization: Bearer <YOUR-TOKEN>" \
            -H "X-GitHub-Api-Version: 2022-11-28" \
            https://api.github.com/repos/OWNER/REPO/commits/REF/status
    """
    resp = requests.get(
        url=f"https://api.github.com/repos/{owner}/{repo}/commits/{commit_sha}/status",
        headers={
            "Authorization": f"Bearer {gh_token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    if resp.status_code != 200:
        print(resp.json())
        return {}
    return resp.json()


def list_pull_requests(owner, repo, gh_token) -> list:
    """
        Reference: https://docs.github.com/en/rest/pulls/pulls?apiVersion=2022-11-28#list-pull-requests
        curl -L \
            -H "Accept: application/vnd.github+json" \
            -H "Authorization: Bearer <YOUR-TOKEN>" \
            -H "X-GitHub-Api-Version: 2022-11-28" \
            https://api.github.com/repos/OWNER/REPO/pulls
    """
    resp = requests.get(
        url=f"https://api.github.com/repos/{owner}/{repo}/pulls",
        headers={
            "Authorization": f"Bearer {gh_token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    if resp.status_code != 200:
        print(resp.json())
        return []
    return resp.json()


if __name__ == "__main__":
    import json

    GH_TOKEN = open(
        "/home/xuananh/Dropbox/Work/Other/credentials_bk/github_basic-token-PhungXuanAnh.txt",
        "r",
    ).read()
    resp = list_pull_requests("showheroes", "viralize-web", GH_TOKEN)
    print(json.dumps(resp, indent=4))
