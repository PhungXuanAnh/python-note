import json

from copy_comments_from_a_merge_request_to_another import (
    create_new_sonaqube_comment_in_MR,
)
from sonaqube import extract_issue_data, search_issues_by_severity

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
create_new_sonaqube_comment_in_MR(sonaqube_data=result, des_project_id=58408953, des_merge_request_id=6)
