import requests
import json

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
DESTINATION_DOMAIN = "https://gitlab.com"


def get_pull_request_comments_from_source_MR(project_id, merge_request_id):
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
            url=f"{SOURCE_DOMAIN}/api/v4/projects/{project_id}/merge_requests/{merge_request_id}/discussions?per_page={PAGE_SIZE}&page={page}",
            headers={
                "Authorization": f"Bearer {TTK_PERSONAL_ACCESS_TOKEN}",
            },
            timeout=60,
        )
        data = resp.json()
        if not data:
            break
        else:
            comments += data
        # print(json.dumps(resp.json(), indent=4, sort_keys=True))
    # ----------- remove mentioned name if need
    # for c in resp.json():
    #     if (
    #         c["html_url"]
    #         == "https://github.com/ablr-com/ablr_django/pull/1319#discussion_r1154053261"
    #     ):
    #         print(c["body"].replace("@", "_@_"))
    return comments


def create_comments_in_destination_MR(project_id, merge_request_id, comment_note):
    """
        reference: https://docs.gitlab.com/ee/api/discussions.html#create-a-new-thread-in-the-merge-request-diff
        
        curl --header "PRIVATE-TOKEN: my_token_1234" \
            "https://gitlab.com/api/v4/projects/51890249/merge_requests/1/versions" | jq
  
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

    resp = requests.post(
        url=f"{DESTINATION_DOMAIN}/api/v4/projects/{project_id}/merge_requests/{merge_request_id}/discussions?body=this-is-XuanAnh-comment",
        headers={
            "Authorization": f"Bearer {XUANANH_PERSONAL_ACCESS_TOKEN}",
        },
        data={
            "body": comment_note["body"].replace(
                "@", "_@_"
            ),  # NOTE: replace @ to avoid tag a github account
            "position[base_sha]": comment_note["position"]["base_sha"],
            "position[head_sha]": comment_note["position"]["head_sha"],
            "position[start_sha]": comment_note["position"]["start_sha"],
            "position[new_path]": comment_note["position"]["new_path"],
            "position[old_path]": comment_note["position"]["old_path"],
            "position[position_type]": comment_note["position"]["position_type"],
            "position[new_line]": comment_note["position"]["new_line"],
        },
        timeout=60,
    )

    if resp.status_code != 201:
        print(f"===============> create comment with failed status code: {resp.status_code}")
        print(resp.json())
        # print(json.dumps(json.loads(resp.json()["message"]), indent=4, sort_keys=True))
    else:
        print(json.dumps(resp.json(), indent=4, sort_keys=True))


def move_comments_from_a_PR_to_other_PR(
    src_project_id, src_merge_request_id, des_project_id, des_merge_request_id
):
    for comment in get_pull_request_comments_from_source_MR(src_project_id, src_merge_request_id):
        comment_note = comment["notes"][0]
        if (
            comment_note["type"] == "DiffNote"
        ):  # TODO: handle "type": "DiscussionNote", see sample_comments.json for more detail
            create_comments_in_destination_MR(
                des_project_id, des_merge_request_id, comment["notes"][0]
            )


if __name__ == "__main__":
    # get_pull_request_comments_from_source_MR(project_id=147, merge_request_id=2251)

    # comment_note = {
    #     "body": 'Please use indentation for HTML/markups so that it would be easier to read/visualize compared to flat nesting:\n\n```html\nbody = u"""\n    <tbody>\n        <tr class="even">\n            <td><a href="/hosts/1/event/1/price-models/1/">{}</a></td>\n            <td>{} - {}</td>\n            <td>{}</td>\n            <td></td>\n            <td>all</td>\n            <td></td>\n            <td>{}</td>\n            <td>{}</td>\n            <td>{}</td>\n            <td></td>\n            <td>100.00</td>\n            <td>10.00</td>\n            <td>{}</td>\n        </tr>\n        <tr class="odd">\n            <td><a href="/hosts/1/event/1/price-models/2/">{}</a></td>\n            <td>{} - {}</td>\n            <td>{}</td>\n            <td></td>\n            <td>all</td>\n            <td></td>\n            <td>{}</td>\n            <td>{}</td>\n            <td>{}</td>\n            <td></td>\n            <td>100.00</td>\n            <td>15.00</td>\n            <td>{}</td>\n        </tr>\n    </tbody>\n""".format(\n```',
    #     "position": {
    #         "base_sha": "bba4e8beb3a3b516a28f791e1bcf031980c61ea7",
    #         "head_sha": "99797adc6bf64ebfca33a2356a3cca213a0716a9",
    #         "line_range": {
    #             "end": {
    #                 "line_code": "7fbf1210f09b27cd04c0c3a1fdbc379488493d27_0_82",
    #                 "new_line": 82,
    #                 "old_line": None,
    #                 "type": "new",
    #             },
    #             "start": {
    #                 "line_code": "7fbf1210f09b27cd04c0c3a1fdbc379488493d27_0_82",
    #                 "new_line": 82,
    #                 "old_line": None,
    #                 "type": "new",
    #             },
    #         },
    #         "new_line": 82,
    #         "new_path": "apps/backoffice/event/summaries/price/tests/test_views.py",
    #         "old_line": None,
    #         "old_path": "apps/backoffice/event/summaries/price/tests/test_views.py",
    #         "position_type": "text",
    #         "start_sha": "0714b52646921952a91b75a139dd94b37e9566dc",
    #     },
    # }
    # create_comments_in_destination_MR(project_id=51890249, merge_request_id=1, comment_note)

    src_project_id = 147
    src_merge_request_id = 2251
    des_project_id = 51890249
    des_merge_request_id = 1

    move_comments_from_a_PR_to_other_PR(
        src_project_id, src_merge_request_id, des_project_id, des_merge_request_id
    )
