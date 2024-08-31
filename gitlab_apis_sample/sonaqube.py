#!/home/xuananh/.pyenv/shims/python
import json

import requests


def search_issues_by_severity():
    """
        Reference: https://next.sonarqube.com/sonarqube/web_api/api/issues/search
        
        Example:
        curl --location 'http://localhost:9000/api/issues/search?impactSeverities=HIGH&issueStatuses=CONFIRMED%2COPEN&id=django_project' \
            --header 'Authorization: Bearer squ_0ab1b83ad4d850d2bdbea4d77daa3b4360033266' | jq
    """
    data = []
    for page in range(1, 5):
        resp = requests.get(
            url=f"http://localhost:9000/api/issues/search?impactSeverities=HIGH&issueStatuses=CONFIRMED%2COPEN&id=django_project&p={page}",
            headers={
                "Authorization": "Bearer squ_0ab1b83ad4d850d2bdbea4d77daa3b4360033266",
            },
            timeout=60,
        )
        res = resp.json()
        if not res or not res.get('issues'):
            break
        else:
            data += res["issues"]
    return data


def extract_issue_data(data):
    extracted_data = []
    for item in data:
        issue = {
            # file_path's format: "django_project:apps/backoffice/transfer/tables.py"
            "file_path": item["component"].split(":")[1],
            "lines": [item["textRange"]["startLine"]],
            "message": item["message"].replace('"', '`').replace("'", '`'),
        }
        for value in item['flows']:
            issue["lines"].append(value["locations"][0]["textRange"]["startLine"])
        extracted_data.append(issue)
    return extracted_data

if __name__ == '__main__':
    data = search_issues_by_severity()
    # print(json.dumps(data, indent=4, sort_keys=True))
    result = extract_issue_data(data)
    print(json.dumps(result, indent=4, sort_keys=True))
