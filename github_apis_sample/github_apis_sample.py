import requests
import json

gh_token = open("/home/xuananh/Dropbox/Work/Other/credentials_bk/github_basic-token-PhungXuanAnh.txt", 'r').read()

def get_pr_comments(pr_id):
    """
        Reference: https://docs.github.com/en/rest/pulls/comments?apiVersion=2022-11-28#list-review-comments-on-a-pull-request
        curl -L \
            -H "Accept: application/vnd.github+json" \
            -H "Authorization: Bearer ghp_asfdsafsadfadfadfsafafaf"\
            -H "X-GitHub-Api-Version: 2022-11-28" \
            https://api.github.com/repos/ablr-com/ablr_django/pulls/1319/comments
    """
    resp = requests.get(
        url=f"https://api.github.com/repos/ablr-com/ablr_django/pulls/{pr_id}/comments",
        headers={
            "Authorization": f"Bearer {gh_token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    # print(json.dumps(resp.json(), indent=4, sort_keys=True))
    # c = resp.json()[0]
    # print(c["body"])
    # print(c["commit_id"])
    # print(c["path"])
    # print(c["start_line"])
    # print(c["start_side"])
    # print(c["line"])
    # print(c["side"])
    for c in resp.json():
        if c["html_url"] == "https://github.com/ablr-com/ablr_django/pull/1319#discussion_r1154053261":
            print(c["body"].replace("@", "_@_"))
    return resp.json()


def create_comment(new_pr_id, body, commit_id, path, line, side, **kwargs):
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
        url=f"https://api.github.com/repos/PhungXuanAnh/ablr_django/pulls/{new_pr_id}/comments",
        headers={
            "Authorization": f"Bearer {gh_token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
        json={
            "body": body.replace("@", "_@_"), # NOTE: replace @ to avoid tag a github account
            "commit_id": commit_id,
            "path": path,
            "line": line,
            "side": side
        },
    )
    
    if resp.status_code != 200:
        # print(json.dumps(json.loads(resp.json()["message"]), indent=4, sort_keys=True))
        print("aaaaaaaaaaaa")    
        print(resp.json())
    else:
        print(json.dumps(resp.json(), indent=4, sort_keys=True))
        

def move_comments_from_a_PR_to_other_PR(current_pr_id, new_pr_id):
    # get_pr_comments(current_pr_id)
    for c in get_pr_comments(current_pr_id):
        create_comment(new_pr_id, c["body"], c["commit_id"], c["path"], c["line"], c["side"])

if __name__ == "__main__":
    move_comments_from_a_PR_to_other_PR(current_pr_id="", new_pr_id="")
