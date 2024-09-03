#!/home/xuananh/.pyenv/shims/python
import hashlib
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


def get_merget_request_comments(domain, access_token, project_id, merge_request_id):
    """
        Reference: https://docs.gitlab.com/ee/api/discussions.html#list-project-merge-request-discussion-items
        
        NOTE: By default, GET requests return 20 results at a time because the API results are paginated. Max is 100
            reference: 
                https://docs.gitlab.com/ee/api/discussions.html#discussions-pagination
                https://gitlab.com/gitlab-org/gitlab/-/issues/290255
            
        Example:
        curl --header "PRIVATE-TOKEN: my_token_1234" \
            "https://git.hk.asiaticketing.com/api/v4/projects/147/merge_requests/2251/discussions?per_page=100&page=1" | jq
            
    """
    PAGE_SIZE = 100

    comments = []
    for page in range(1, 10):
        resp = requests.get(
            url=f"{domain}/api/v4/projects/{project_id}/merge_requests/{merge_request_id}/discussions?per_page={PAGE_SIZE}&page={page}",
            headers={
                "Authorization": f"Bearer {access_token}",
            },
            timeout=60,
        )
        data = resp.json()
        if not data:
            break
        else:
            comments += data
        print(json.dumps(resp.json(), indent=4, sort_keys=True))
    # ----------- remove mentioned name if need
    # for c in resp.json():
    #     if (
    #         c["html_url"]
    #         == "https://github.com/ablr-com/ablr_django/pull/1319#discussion_r1154053261"
    #     ):
    #         print(c["body"].replace("@", "_@_"))
    return comments


def get_pull_request_comments_from_source_MR(project_id, merge_request_id):
    return get_merget_request_comments(SOURCE_DOMAIN, TTK_PERSONAL_ACCESS_TOKEN, project_id, merge_request_id)

def get_latest_merge_request_version_des_MR(project_id, merge_request_id):
    """
        curl --header "PRIVATE-TOKEN: my_token_1234" \
                "https://gitlab.com/api/v4/projects/51890249/merge_requests/1/versions" | jq
    """
    PAGE_SIZE = 100
    page = 1
    resp = requests.get(
        url=f"{DESTINATION_DOMAIN}/api/v4/projects/{project_id}/merge_requests/{merge_request_id}/versions?per_page={PAGE_SIZE}&page={page}",
        headers={
            "Authorization": f"Bearer {DESTINATION_GL_TOKEN}",
        },
        timeout=60,
    )

    if resp.status_code != 200:
        print(f"===============> create comment with failed status code: {resp.status_code}")
        print(resp.json())
        raise Exception("cannot get merge request version")
        # print(json.dumps(json.loads(resp.json()["message"]), indent=4, sort_keys=True))
    else:
        results = resp.json()
        # print("merge request version: ", json.dumps(results, indent=4, sort_keys=True))
        return results


def create_comments_in_multiple_lines(project_id, merge_request_id, latest_MR_version, **kargs):
    """
        reference: https://docs.gitlab.com/ee/api/discussions.html#create-a-new-thread-in-the-merge-request-diff
        
        step 1: get latest merge request version: NOTE: this information is got outside of this function to avoid calling api multiple times
            curl --header "PRIVATE-TOKEN: my_token_1234" \
                "https://gitlab.com/api/v4/projects/51890249/merge_requests/1/versions" | jq
            
            sample: 
            {
                "id": 870881248,
                "head_commit_sha": "5f4d4aa2909e31f7c0ece841562f7e27b599b360",
                "base_commit_sha": "64b7ffc4e1291c5e22830e8bd891b9deaec7d7d7",
                "start_commit_sha": "64b7ffc4e1291c5e22830e8bd891b9deaec7d7d7",
                "created_at": "2023-12-13T06:55:59.305Z",
                "merge_request_id": 262434375,
                "state": "collected",
                "real_size": "27",
                "patch_id_sha": "60a5db52158f6ad885d35bcbeed14132895c9e37",
            }
  
        step 2: create new comment with base_sha, head_sha, start_sha get from step 1, don't get from comment_note
            curl --request POST --header "PRIVATE-TOKEN: my_token_1234"\
                --form 'position[position_type]=text'\
                --form 'position[base_sha]=bba4e8beb3a3b516a28f791e1bcf031980c61ea7'\
                --form 'position[head_sha]=99797adc6bf64ebfca33a2356a3cca213a0716a9'\
                --form 'position[start_sha]=0714b52646921952a91b75a139dd94b37e9566dc'\
                --form 'position[new_path]=apps/backoffice/event/summaries/price/tests/test_views.py'\
                --form 'position[old_path]=apps/backoffice/event/summaries/price/tests/test_views.py'\
                --form 'body=test comment body'\
                --form 'position[line_range][start][line_code]=10'\
                --form 'position[line_range][start][type]=new'\
                --form 'position[line_range][end][line_code]=82'\
                --form 'position[line_range][end][type]=new'\
                "https://gitlab.com/api/v4/projects/51890249/merge_requests/1/discussions"
    """

    # print("creating comment: ", json.dumps(comment_note, indent=4, sort_keys=True))

    data = {
        "body": kargs["body"].replace("@", "_@_"),  # NOTE: replace @ to avoid tag a github account
        "position[base_sha]": latest_MR_version["base_commit_sha"],
        "position[head_sha]": latest_MR_version["head_commit_sha"],
        "position[start_sha]": latest_MR_version["start_commit_sha"],
        "position[new_path]": kargs["new_path"],
        "position[old_path]": kargs["old_path"],
        "position[position_type]": kargs["position_type"],
        "position[line_range][start][line_code]": kargs["start_line_code"],
        "position[line_range][start][type]": "new",
        "position[line_range][end][line_code]": kargs["end_line_code"],
        "position[line_range][end][type]": "new",
        "position[new_line]": kargs["new_line"],
        # "position[old_line]": 0,
    }
    print(json.dumps(data, indent=4, sort_keys=True))
    resp = requests.post(
        url=f"{DESTINATION_DOMAIN}/api/v4/projects/{project_id}/merge_requests/{merge_request_id}/discussions",
        headers={
            "Authorization": f"Bearer {XUANANH_PERSONAL_ACCESS_TOKEN}",
        },
        data=data,
        timeout=60,
    )

    if resp.status_code != 201:
        print(f"===============> create comment with failed status code: {resp.status_code}")
        print(resp.json())
        # print(json.dumps(json.loads(resp.json()["message"]), indent=4, sort_keys=True))
    else:
        print(
            "created new comment with response: ", json.dumps(resp.json(), indent=4, sort_keys=True)
        )
    return resp


def create_comments_in_single_line(project_id, merge_request_id, latest_MR_version, **kargs):
    """
        reference: https://docs.gitlab.com/ee/api/discussions.html#create-a-new-thread-in-the-merge-request-diff
        
        step 1: get latest merge request version: NOTE: this information is got outside of this function to avoid calling api multiple times
            curl --header "PRIVATE-TOKEN: my_token_1234" \
                "https://gitlab.com/api/v4/projects/51890249/merge_requests/1/versions" | jq
            
            sample: 
            {
                "id": 870881248,
                "head_commit_sha": "5f4d4aa2909e31f7c0ece841562f7e27b599b360",
                "base_commit_sha": "64b7ffc4e1291c5e22830e8bd891b9deaec7d7d7",
                "start_commit_sha": "64b7ffc4e1291c5e22830e8bd891b9deaec7d7d7",
                "created_at": "2023-12-13T06:55:59.305Z",
                "merge_request_id": 262434375,
                "state": "collected",
                "real_size": "27",
                "patch_id_sha": "60a5db52158f6ad885d35bcbeed14132895c9e37",
            }
  
        step 2: create new comment with base_sha, head_sha, start_sha get from step 1, don't get from comment_note
            curl --request POST --header "PRIVATE-TOKEN: my_token_1234"\
                --form 'position[position_type]=text'\
                --form 'position[base_sha]=bba4e8beb3a3b516a28f791e1bcf031980c61ea7'\
                --form 'position[head_sha]=99797adc6bf64ebfca33a2356a3cca213a0716a9'\
                --form 'position[start_sha]=0714b52646921952a91b75a139dd94b37e9566dc'\
                --form 'position[new_path]=apps/backoffice/event/summaries/price/tests/test_views.py'\
                --form 'position[old_path]=apps/backoffice/event/summaries/price/tests/test_views.py'\
                --form 'position[new_line]=82'\
                --form 'body=test comment body'\
                "https://gitlab.com/api/v4/projects/51890249/merge_requests/1/discussions"
    """

    # print("creating comment: ", json.dumps(comment_note, indent=4, sort_keys=True))

    data = {
        "body": kargs["body"].replace("@", "_@_"),  # NOTE: replace @ to avoid tag a github account
        "position[base_sha]": latest_MR_version["base_commit_sha"],
        "position[head_sha]": latest_MR_version["head_commit_sha"],
        "position[start_sha]": latest_MR_version["start_commit_sha"],
        "position[new_path]": kargs["new_path"],
        "position[old_path]": kargs["old_path"],
        "position[position_type]": kargs["position_type"],
        "position[new_line]": kargs["new_line"],
    }
    print('Creating comment with payload', json.dumps(data, indent=4, sort_keys=True))
    resp = requests.post(
        url=f"{DESTINATION_DOMAIN}/api/v4/projects/{project_id}/merge_requests/{merge_request_id}/discussions",
        headers={
            "Authorization": f"Bearer {XUANANH_PERSONAL_ACCESS_TOKEN}",
        },
        data=data,
        timeout=60,
    )

    if resp.status_code != 201:
        print(f"===============> create comment with failed status code: {resp.status_code}")
        print(resp.json())
        # print(json.dumps(json.loads(resp.json()["message"]), indent=4, sort_keys=True))
    else:
        print(
            "created new comment with response: ", json.dumps(resp.json(), indent=4, sort_keys=True)
        )
    return resp


def create_new_comment_from_sonaqube_issue(sonaqube_data, des_project_id, des_merge_request_id):
    count = 0
    des_latest_version = get_latest_merge_request_version_des_MR(
        des_project_id, des_merge_request_id
    )[0]
    for value in sonaqube_data:
        for line in value["lines"]:
            resp = create_comments_in_single_line(
                des_project_id,
                des_merge_request_id,
                des_latest_version,
                body=value["message"],
                new_path=value["file_path"],
                old_path=value["file_path"],
                position_type="text",
                new_line=line,
            )
            # if resp.status_code == 201:
            #     break
        count = count + 1

    print(f"created {count} comments in total {len(sonaqube_data)}")


def sha1_hash(toHash):
        try:
            messageDigest = hashlib.sha1()
            stringM = str(toHash)
            byteM = bytes(stringM, encoding='utf')
            messageDigest.update(byteM)
            return messageDigest.hexdigest()
        except TypeError:
            raise "String to hash was not compatible"


def create_new_comment_from_sonaqube_duplication(sonaqube_duplications, des_project_id, des_merge_request_id):
    merge_request_versions = get_latest_merge_request_version_des_MR(
        des_project_id, des_merge_request_id
    )[0]
    for value in sonaqube_duplications:
        # https://docs.gitlab.com/ee/api/discussions.html#line-code
        # sha1_of_file = sha1_hash(value["file_path"])
        resp = create_comments_in_single_line(
            des_project_id,
            des_merge_request_id,
            merge_request_versions,
            body=value["message"],
            new_path=value["file_path"],
            old_path=value["file_path"],
            position_type="text",
            # start_line_code=f'{sha1_of_file}_0_{value["duplicated_range"][0]}',
            # end_line_code=f'{sha1_of_file}_0_{value["duplicated_range"][1]}',
            # start_new_line=value["duplicated_range"][0],
            # end_new_line=value["duplicated_range"][1],
            new_line=value["duplicated_range"][0],
        )
        # if resp.status_code == 201:
        #     break


def move_comments_from_a_PR_to_other_PR(
    src_project_id, src_merge_request_id, des_project_id, des_merge_request_id
):
    count = 0
    comments = get_pull_request_comments_from_source_MR(src_project_id, src_merge_request_id)
    des_latest_version = get_latest_merge_request_version_des_MR(
        des_project_id, des_merge_request_id
    )[0]
    for comment in comments:
        comment_note = comment["notes"][0]
        if (
            comment_note["type"] == "DiffNote" and not comment_note["resolved"]
        ):  # TODO: handle "type": "DiscussionNote", see sample_comments.json for more detail
            create_comments_in_single_line(
                des_project_id,
                des_merge_request_id,
                des_latest_version,
                body=comment_note["body"],
                new_path=comment_note["position"]["new_path"],
                old_path=comment_note["position"]["old_path"],
                position_type=comment_note["position"]["position_type"],
                new_line=comment_note["position"]["new_line"],
            )
            count = count + 1

    print(f"created {count} comments in total {len(comments)}")


if __name__ == "__main__":
    ## ================================== testing ==============================================

    # comments = get_pull_request_comments_from_source_MR(project_id=147, merge_request_id=2251)
    # print(json.dumps(comments, indent=4, sort_keys=True))
    # print(len(comments))

    comment_note_test = {
        "body": 'Please use indentation for HTML/markups so that it would be easier to read/visualize compared to flat nesting:\n\n```html\nbody = u"""\n    <tbody>\n        <tr class="even">\n            <td><a href="/hosts/1/event/1/price-models/1/">{}</a></td>\n            <td>{} - {}</td>\n            <td>{}</td>\n            <td></td>\n            <td>all</td>\n            <td></td>\n            <td>{}</td>\n            <td>{}</td>\n            <td>{}</td>\n            <td></td>\n            <td>100.00</td>\n            <td>10.00</td>\n            <td>{}</td>\n        </tr>\n        <tr class="odd">\n            <td><a href="/hosts/1/event/1/price-models/2/">{}</a></td>\n            <td>{} - {}</td>\n            <td>{}</td>\n            <td></td>\n            <td>all</td>\n            <td></td>\n            <td>{}</td>\n            <td>{}</td>\n            <td>{}</td>\n            <td></td>\n            <td>100.00</td>\n            <td>15.00</td>\n            <td>{}</td>\n        </tr>\n    </tbody>\n""".format(\n```',
        "position": {
            "base_sha": "bba4e8beb3a3b516a28f791e1bcf031980c61ea7",
            "head_sha": "99797adc6bf64ebfca33a2356a3cca213a0716a9",
            "line_range": {
                "end": {
                    "line_code": "7fbf1210f09b27cd04c0c3a1fdbc379488493d27_0_82",
                    "new_line": 82,
                    "old_line": None,
                    "type": "new",
                },
                "start": {
                    "line_code": "7fbf1210f09b27cd04c0c3a1fdbc379488493d27_0_82",
                    "new_line": 82,
                    "old_line": None,
                    "type": "new",
                },
            },
            "new_line": 82,
            "new_path": "apps/backoffice/event/summaries/price/tests/test_views.py",
            "old_line": None,
            "old_path": "apps/backoffice/event/summaries/price/tests/test_views.py",
            "position_type": "text",
            "start_sha": "0714b52646921952a91b75a139dd94b37e9566dc",
        },
    }
    # create_comments_in_destination_MR(
    #     project_id=51890249, merge_request_id=1, comment_note=comment_note
    # )

    # latest_version = get_latest_merge_request_version_des_MR(
    #     project_id=51890249, merge_request_id=1
    # )
    # print(json.dumps(latest_version, indent=4, sort_keys=True))

    # print(sha1_hash("apps/backoffice/box_office/views.py"))

    get_merget_request_comments(DESTINATION_DOMAIN, DESTINATION_GL_TOKEN, 58408953, 6)

    ## ================================== actual run ==============================================

    src_project_id = 147  # ttk gitlab
    src_merge_request_id = 2757
    des_project_id = 58408953  # XuanAnh gitlab
    des_merge_request_id = 4

    # move_comments_from_a_PR_to_other_PR(
    #     src_project_id, src_merge_request_id, des_project_id, des_merge_request_id
    # )
