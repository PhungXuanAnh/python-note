import time

import requests

from logging_sample.logging_dictConfig import console_logger


def list_commits_on_pull_request(
    owner, repo, pr_id, gh_token, page=1, per_page=100
) -> list:
    """
        Reference: https://docs.github.com/en/rest/pulls/pulls?apiVersion=2022-11-28#list-commits-on-a-pull-request
        curl -L \
            -H "Accept: application/vnd.github+json" \
            -H "Authorization: Bearer <YOUR-TOKEN>" \
            -H "X-GitHub-Api-Version: 2022-11-28" \
            https://api.github.com/repos/OWNER/REPO/pulls/PULL_NUMBER/commits
    """
    resp = requests.get(
        url=f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_id}/commits?page={page}&per_page={per_page}",
        headers={
            "Authorization": f"Bearer {gh_token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    if resp.status_code != 200:
        console_logger.debug(resp.json())
        return []
    return resp.json()


def get_latest_commit(owner, repo, pr_id, gh_token):
    commits = list_commits_on_pull_request(owner, repo, pr_id, gh_token)
    lastest_commit = None
    page = 1
    while commits:
        lastest_commit = commits[-1]
        commits = list_commits_on_pull_request(
            owner, repo, pr_id, gh_token, page=page + 1
        )
        time.sleep(0.5)
        if page > 10:
            raise Exception(
                "You have more than 10 pages of 1000 commits. It's strange!!!"
            )
    return lastest_commit


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
        console_logger.debug(resp.json())
        return {}
    return resp.json()


def list_pull_requests(owner, repo, gh_token, state=None) -> list:
    """
        Reference: https://docs.github.com/en/rest/pulls/pulls?apiVersion=2022-11-28#list-pull-requests
        curl -L \
            -H "Accept: application/vnd.github+json" \
            -H "Authorization: Bearer <YOUR-TOKEN>" \
            -H "X-GitHub-Api-Version: 2022-11-28" \
            https://api.github.com/repos/OWNER/REPO/pulls
    """
    url = (f"https://api.github.com/repos/{owner}/{repo}/pulls",)
    if state == "open" or state == "closed" or state == "all":
        # by default, the GitHub API lists only open pull requests if no state parameter is specified. 
        # To list all pull requests regardless of their state, you need to add the state parameter 
        # with the value `all`.
        url += f"?state={state}"
    resp = requests.get(
        url=f"https://api.github.com/repos/{owner}/{repo}/pulls",
        headers={
            "Authorization": f"Bearer {gh_token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    if resp.status_code != 200:
        console_logger.debug(f"List pull requests for repo {owner}/{repo} failed: {resp.json()}")
        return []
    return resp.json()


if __name__ == "__main__":
    import json
    import os

    GH_TOKEN = os.environ.get("GH_TOKEN_MAIN")
    # resp = list_pull_requests("showheroes", "viralize-web", GH_TOKEN)
    # resp = get_commit_status(
    #     "showheroes",
    #     "viralize-web",
    #     "1ebcc0417f23426d44dee06106ccf271e243f43c",
    #     GH_TOKEN,
    # )
    # console_logger.debug(json.dumps(resp, indent=4))
    # resp = list_commits_on_pull_request(
    #     "showheroes", "viralize-web", 5283, GH_TOKEN, page=1, per_page=100
    # )
    # console_logger.debug(json.dumps(resp, indent=4, sort_keys=True))
    console_logger.debug(
        get_latest_commit("showheroes", "viralize-web", 5283, GH_TOKEN)
    )
