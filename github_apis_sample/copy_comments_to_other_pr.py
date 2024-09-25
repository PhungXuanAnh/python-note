import json

import requests


def get_pr_comments(owner, repo, pr_id, gh_token):
    """
        Reference: https://docs.github.com/en/rest/pulls/comments?apiVersion=2022-11-28#list-review-comments-on-a-pull-request
        curl -L \
            -H "Accept: application/vnd.github+json" \
            -H "Authorization: Bearer ghp_asfdsafsadfadfadfsafafaf"\
            -H "X-GitHub-Api-Version: 2022-11-28" \
            https://api.github.com/repos/{owner}/{repo}/pulls/1319/comments
    """
    resp = requests.get(
        url=f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_id}/comments",
        headers={
            "Authorization": f"Bearer {gh_token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    if resp.status_code != 200:
        print(json.dumps(resp.json(), indent=4, sort_keys=True))
        return []
    # c = resp.json()[0]
    # print(c["body"])
    # print(c["commit_id"])
    # print(c["path"])
    # print(c["start_line"])
    # print(c["start_side"])
    # print(c["line"])
    # print(c["side"])

    # remove mentioned name
    for c in resp.json():
        if c["html_url"] == "https://github.com/{owner}/{repo}/pull/1319#discussion_r1154053261":
            print(c["body"].replace("@", "_@_"))
    return resp.json()


def create_comment(gh_token, owner, repo, pr_id, body, commit_id, path, line, side, **kwargs):
    """
        curl -L \
            -X POST \
            -H "Accept: application/vnd.github+json" \
            -H "Authorization: Bearer <YOUR-TOKEN>"\
            -H "X-GitHub-Api-Version: 2022-11-28" \
            https://api.github.com/repos/OWNER/REPO/pulls/PULL_NUMBER/comments \
            -d '{"body":"Great stuff!","commit_id":"6dcb09b5b57875f334f61aebed695e2e4193db5e","path":"file1.txt","start_line":1,"start_side":"RIGHT","line":2,"side":"RIGHT"}'

    """
    resp = requests.post(
        url=f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_id}/comments",
        headers={
            "Authorization": f"Bearer {gh_token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
        json={
            "body": body.replace("@", "_@_"),  # NOTE: replace @ to avoid tag a github account
            "commit_id": commit_id,
            "path": path,
            "line": line,
            "side": side,
        },
    )

    if resp.status_code != 200:
        # print(json.dumps(json.loads(resp.json()["message"]), indent=4, sort_keys=True))
        print("aaaaaaaaaaaa", resp.status_code)
        print(resp.json())
    else:
        pass
        # print(json.dumps(resp.json(), indent=4, sort_keys=True))


def move_comments_from_a_PR_to_other_PR():
    for c in get_pr_comments(SOURCE_OWNER, SOURCE_REPO, SOURCE_PR_ID, SOURCE_GH_TOKEN):
        create_comment(
            DEST_GH_TOKEN,
            DEST_OWNER,
            DEST_REPO,
            DEST_PR_ID,
            c["body"],
            c["commit_id"],
            c["path"],
            c["line"],
            c["side"],
        )


if __name__ == "__main__":
    SOURCE_GH_TOKEN = open(
        "/home/xuananh/Dropbox/Work/Other/credentials_bk/github_basic-token-PhungXuanAnh.txt", "r"
    ).read()
    SOURCE_OWNER = "alexyjs"
    # FE
    # SOURCE_REPO = "fleet-client"
    # SOURCE_PR_ID = 1
    # BE
    SOURCE_REPO = "fleet-core"
    SOURCE_PR_ID = 4

    DEST_GH_TOKEN = SOURCE_GH_TOKEN
    DEST_OWNER = "PhungXuanAnh"
    # FE
    # DEST_REPO = "pine-fleet-client"
    # DEST_PR_ID = 3
    # BE
    DEST_REPO = "pine-fleet-core"
    DEST_PR_ID = 5

    move_comments_from_a_PR_to_other_PR()
    # get_pr_comments(SOURCE_OWNER, SOURCE_REPO, SOURCE_PR_ID, SOURCE_GH_TOKEN)
