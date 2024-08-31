#!/home/xuananh/.pyenv/shims/python
import json

import requests

# pylint: disable=pointless-string-statement
"""
    Example on how to use this access token: https://docs.gitlab.com/ee/api/rest/#personalprojectgroup-access-tokens
    Access this link to get project id: https://gitlab.com/xa1307/ticketing-v2/edit
    To get token Access this link : https://gitlab.com/-/profile/personal_access_tokens
    or reference: https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html
"""

XUANANH_PERSONAL_ACCESS_TOKEN = open(
    "/home/xuananh/Dropbox/Work/ttk/gitlab_tokens/xuananh.txt", "r"
).read()
TTK_PERSONAL_ACCESS_TOKEN = open("/home/xuananh/Dropbox/Work/ttk/gitlab_tokens/ttk.txt", "r").read()

SOURCE_DOMAIN = "https://git.hk.asiaticketing.com"
SOURCE_GL_TOKEN = TTK_PERSONAL_ACCESS_TOKEN

DESTINATION_DOMAIN = "https://gitlab.com"
DESTINATION_GL_TOKEN = XUANANH_PERSONAL_ACCESS_TOKEN


def list_merge_request_diff(domain, project_id, merge_request_id):
    """
        Reference: https://docs.gitlab.com/ee/api/merge_requests.html#get-single-merge-request-changes
        
        NOTE: By default, GET requests return 20 results at a time because the API results are paginated
            
        Example:
        curl --header "PRIVATE-TOKEN: glpat-qSCLkv6JyFVs4V8BBMZV" \
            --url "https://gitlab.com/api/v4/projects/58408953/merge_requests/4/diffs?page=1&per_page=20" | jq
            
    """
    PAGE_SIZE = 20

    changed_files_data = []
    for page in range(1, 10):
        resp = requests.get(
            url=f"{domain}/api/v4/projects/{project_id}/merge_requests/{merge_request_id}/diffs?per_page={PAGE_SIZE}&page={page}",
            headers={
                "Authorization": f"Bearer {XUANANH_PERSONAL_ACCESS_TOKEN}",
            },
            timeout=60,
        )
        data = resp.json()
        if not data:
            break
        else:
            changed_files_data += data
        # print(json.dumps(resp.json(), indent=4, sort_keys=True))
    # ----------- remove mentioned name if need
    # for c in resp.json():
    #     if (
    #         c["html_url"]
    #         == "https://github.com/ablr-com/ablr_django/pull/1319#discussion_r1154053261"
    #     ):
    #         print(c["body"].replace("@", "_@_"))
    return changed_files_data


def get_list_changed_files_in_merge_request(domain, project_id, merge_request_id):
    changed_files = []
    for changed_files_info in list_merge_request_diff(domain, project_id, merge_request_id):
        changed_files.append(changed_files_info['new_path'])
    return changed_files

if __name__ == '__main__':
    des_project_id = 58408953  # XuanAnh gitlab
    des_merge_request_id = 4
    # list_merge_request_diff(DESTINATION_DOMAIN, des_project_id, des_merge_request_id)

    changed_files = get_list_changed_files_in_merge_request(
        DESTINATION_DOMAIN, des_project_id, des_merge_request_id
    )
    print(json.dumps(changed_files, indent=4, sort_keys=True))
