import json
import sys

from copy_comments_from_a_merge_request_to_another import (
    create_new_comment_from_sonaqube_duplication,
    create_new_comment_from_sonaqube_issue,
)
from list_diff_merge_request import get_list_changed_files_in_merge_request
from sonaqube import (
    extract_issue_data,
    get_duplicated_blocks,
    search_issues_by_severity,
)


def comment_from_issue(project_id, merge_request_id, changed_files):
    data = search_issues_by_severity()
    if not data:
        return
    # print(json.dumps(data, indent=4, sort_keys=True))
    result = extract_issue_data(data)
    # print(json.dumps(result, indent=4, sort_keys=True))
    # result = [
    #     {
    #         "file_path": "apps/backoffice/transfer/tables.py",
    #         "lines": [313, 395, 408],
    #         "message": "Define a constant instead of duplicating this literal `<a href=`{}`>{}</a>` 3 times.",
    #     }
    # ]
    error_files = []
    for _file in result:
        if _file["file_path"] in changed_files:
            error_files.append(_file)
    if not error_files:
        return

    create_new_comment_from_sonaqube_issue(
        sonaqube_data=error_files, des_project_id=project_id, des_merge_request_id=merge_request_id
    )


def comment_from_duplications(project_id, merge_request_id, changed_files):
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
    duplicated_files = []
    for _file in result:
        if _file["file_path"] in changed_files:
            duplicated_files.append(_file)

    if not duplicated_files:
        return

    create_new_comment_from_sonaqube_duplication(
        sonaqube_duplications=duplicated_files,
        des_project_id=project_id,
        des_merge_request_id=merge_request_id,
    )


if __name__ == '__main__':
    # project_id = 58408953
    # merge_request_id = 6
    project_id, merge_request_id = sys.argv[1:]
    print(
        f"Copy sona error message to project_id: {project_id} and merge_request_id: {merge_request_id}"
    )
    # changed_files = get_list_changed_files_in_merge_request(
    #     "https://gitlab.com", project_id, merge_request_id
    # )
    changed_files = ["apps/backoffice/box_office/views.py"]
    comment_from_issue(project_id, merge_request_id, changed_files)
    comment_from_duplications(project_id, merge_request_id, changed_files)

    # using selenium to comment automatically
    # create new user-profile, login to gitlab/github account
    # open selenium re-use the user-profile
    # gitlab, find the line number error from sonaqube, if there's no line number, then ignore the error else
    #    hover the mouse over that line number to show comment button
    #    click to comment button to add new comment
    #   choose the line number in the comment box
    #   add new comment content to the comment box
    #   click to button: Add comment now
    #   in the right column and and comment to it
