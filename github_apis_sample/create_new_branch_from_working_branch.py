import time
import requests
import json
import sys

sys.path.append("/home/xuananh/repo/python-note")
from subprocess_sample.subprocess_sample import run_command_print_output

gh_token = open("/home/xuananh/Dropbox/Work/Other/credentials_bk/github_basic-token-PhungXuanAnh.txt", "r").read()


def create_pull_request(owner, repo, base_branch, working_branch):
    """
        Reference: https://docs.github.com/en/rest/pulls/pulls?apiVersion=2022-11-28#create-a-pull-request
        curl -L \
            -X POST \
            -H "Accept: application/vnd.github+json" \
            -H "Authorization: Bearer <YOUR-TOKEN>"\
            -H "X-GitHub-Api-Version: 2022-11-28" \
            https://api.github.com/repos/OWNER/REPO/pulls \
            -d '{"title":"Amazing new feature","body":"Please pull these awesome changes in!","head":"octocat:new-feature","base":"master"}'
    """
    resp = requests.post(
        url=f"https://api.github.com/repos/{owner}/{repo}/pulls",
        headers={
            "Authorization": f"Bearer {gh_token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
        json={
            "title": f"Temporary PR for {working_branch}",
            "body": "Please pull these awesome changes in!",
            "head": working_branch,
            "base": base_branch,
        },
    )
    response = resp.json()
    pr_number = response.get('number')
    if pr_number:
        print(f" ==============> pull request id: {pr_number}")
        print(f" ==============> pull request url: {response.get('html_url')}")
    else:
        print("Create PR failed: ", json.dumps(response, indent=4, sort_keys=True))
    return response


def create_new_branch(repository_dir, base_branch, working_branch):
    """
    base_branch: is branch from which we create working_branch
    """

    new_branch_name = f"{working_branch}_{int(time.time())}"
    command = (
        f"cd {repository_dir} && "
        f"git checkout {base_branch} && "
        f"git pull xuananh {base_branch} && "
        f"git checkout -b {new_branch_name} && "
        f"git push xuananh {new_branch_name}"
    )
    return_code = run_command_print_output(command)
    if return_code != 0:
        print("Error while creating new branch")
        sys.exit()
    else:
        print(" ==============> new branch name: ", new_branch_name)
        return new_branch_name


def get_pr(owner, repo, pr_number):
    """
        Reference: https://docs.github.com/en/rest/pulls/pulls?apiVersion=2022-11-28#get-a-pull-request
        curl -L \
            -H "Accept: application/vnd.github+json" \
            -H "Authorization: Bearer <YOUR-TOKEN>"\
            -H "X-GitHub-Api-Version: 2022-11-28" \
            https://api.github.com/repos/OWNER/REPO/pulls/PULL_NUMBER
    """
    resp = requests.get(
        url=f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}",
        headers={
            "Authorization": f"Bearer {gh_token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    resp = resp.json()
    # print(json.dumps(resp, indent=4, sort_keys=True))
    return resp


def is_mergeable(owner, repo, pr_number):
    pr = get_pr(owner, repo, pr_number)
    return pr.get('mergeable')
    
    
def merge_pr(owner, repo, pr_number):
    """
        Reference: https://docs.github.com/en/rest/pulls/pulls?apiVersion=2022-11-28#merge-a-pull-request
        curl -L \
            -X PUT \
            -H "Accept: application/vnd.github+json" \
            -H "Authorization: Bearer <YOUR-TOKEN>"\
            -H "X-GitHub-Api-Version: 2022-11-28" \
            https://api.github.com/repos/OWNER/REPO/pulls/PULL_NUMBER/merge \
            -d '{"commit_title":"Expand enum","commit_message":"Add a new value to the merge_method enum"}'
    """
    resp = requests.put(
        url=f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/merge",
        headers={
            "Authorization": f"Bearer {gh_token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
        json={
            "commit_title": "Update code",
            "commit_message": "Update new code",
            "merge_method": "squash"
        },
    )
    response = resp.json()
    print(json.dumps(response, indent=4, sort_keys=True))
    return response

def pull_new_branch_after_merge(repository_dir, new_branch_name):
    command = (
        f"cd {repository_dir} && "
        f"git checkout {new_branch_name} && "
        f"git pull xuananh {new_branch_name}"
    )
    return_code = run_command_print_output(command)
    if return_code != 0:
        print("EEEEEEEEEEEEEEEError while pull branch")
        sys.exit()
    else:
        print(f"Completed to create new working branch: {new_branch_name}")

    
def create_new_branch_spectre_dashboard_repo(working_branch, main_branch):
    """
        Create new branch name_main_timestamp from main branch same as working branch
        push new branch name_main_timestamp to PhungXuanAnh/reponame
        create new PR from working branch to name_main_timestamp
            https://docs.github.com/en/rest/pulls/pulls?apiVersion=2022-11-28#create-a-pull-request
        Check Conflict 
            https://docs.github.com/en/rest/pulls/pulls?apiVersion=2022-11-28#get-a-pull-request
            If not conflict Accept PR and to merge squashed PR
            Else stop and do other steps manually
        Push name_main_timestamp to all remote
        print branch name name_main_timestamp
        Create PR manually
    """
    repository_dir = "/home/xuananh/repo/Spectre.Dashboard.Backend"
    new_branch_name = create_new_branch(repository_dir, main_branch, working_branch)

    owner = "PhungXuanAnh"
    repo = "Spectre.Dashboard.Backend"
    pr = create_pull_request(owner, repo, base_branch=new_branch_name, working_branch=working_branch)
    
    pr_number = pr.get("number")
    if is_mergeable(owner, repo, pr_number):
        merge_pr(owner, repo, pr_number)
        pull_new_branch_after_merge(repository_dir, new_branch_name)
    else:
        print(f"Cannot merge pull request: {pr_number}")

if __name__ == "__main__":
    working_branch = 'working-feature1-abc'
    main_branch = 'feature1'
    create_new_branch_spectre_dashboard_repo(working_branch, main_branch)
