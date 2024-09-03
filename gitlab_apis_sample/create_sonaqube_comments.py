import json

from copy_comments_from_a_merge_request_to_another import (
    create_new_comment_from_sonaqube_duplication,
    create_new_comment_from_sonaqube_issue,
)
from sonaqube import extract_issue_data, get_duplicated_blocks, search_issues_by_severity


def comment_from_issue(project_id, merge_request_id):
    data = search_issues_by_severity()
    # print(json.dumps(data, indent=4, sort_keys=True))
    result = extract_issue_data(data)
    print(json.dumps(result, indent=4, sort_keys=True))

    # result = [
    #     {
    #         "file_path": "apps/backoffice/transfer/tables.py",
    #         "lines": [313, 395, 408],
    #         "message": "Define a constant instead of duplicating this literal `<a href=`{}`>{}</a>` 3 times.",
    #     }
    # ]
    create_new_comment_from_sonaqube_issue(
        sonaqube_data=result, des_project_id=project_id, des_merge_request_id=merge_request_id
    )


def comment_from_duplications(project_id, merge_request_id):
    result = get_duplicated_blocks(
        project_key="ticketing-v2", file_path="backoffice/transfer/tables.py"
    )
    # result = [
    #     {
    #         "duplicated_range": [15, 19],
    #         "file_path": "apps/backoffice/transfer/tables.py",
    #         "message": "Lines [15, 19]: Duplicated in file: backoffice/refund/tables.py in lines: [331, 353]",
    #     },
    #     # {
    #     #     "duplicated_range": [409, 436],
    #     #     "file_path": "apps/backoffice/transfer/tables.py",
    #     #     "message": "Duplicated in file: backoffice/refund/tables.py, lines: [355, 382]",
    #     # },
    # ]
    create_new_comment_from_sonaqube_duplication(
        sonaqube_duplications=result,
        des_project_id=project_id,
        des_merge_request_id=merge_request_id,
    )


if __name__ == '__main__':
    project_id = 58408953
    merge_request_id = 6
    comment_from_issue(project_id, merge_request_id)
    comment_from_duplications(project_id, merge_request_id)
