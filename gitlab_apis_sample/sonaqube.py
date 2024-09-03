#!/home/xuananh/.pyenv/shims/python
import json

import requests


def search_issues_by_severity():
    """
        Reference: https://next.sonarqube.com/sonarqube/web_api/api/issues/search
        
        Example:
        curl --location 'http://localhost:9000/api/issues/search?impactSeverities=HIGH&issueStatuses=CONFIRMED%2COPEN&id=django_project' \
            --header 'Authorization: Bearer squ_0ab1b83ad4d850d2bdbea4d77daa3b4360033266' | jq
            
        curl 'http://localhost:9000/api/issues/search?issueStatuses=OPEN%2CCONFIRMED&additionalFields=_all&components=ticketing-v2%3Abackoffice%2Ftransfer%2Ftables.py&s=FILE_LINE&p=1&ps=500' \
            -H 'Accept: application/json' \
            -H 'Cookie: csrftoken=wys0NSLZiB5nW1F6Omi85i14g8ZAATIu34HPer4mL3XfAcwDqj8wHyMv196fVf32; XSRF-TOKEN=ko9afcfablgp9vmtc8bqi2sip1; JWT-SESSION=eyJhbGciOiJIUzI1NiJ9.eyJsYXN0UmVmcmVzaFRpbWUiOjE3MjUyNDU3Njk2MjgsInhzcmZUb2tlbiI6ImtvOWFmY2ZhYmxncDl2bXRjOGJxaTJzaXAxIiwianRpIjoiM2QzOTYyNTUtOWVhOC00NjViLWExYWQtMGIwYzIyMDJlZDJhIiwic3ViIjoiNTQyYmIzY2ItYjNjYi00MmIzLWJmNzUtZmM2OGVmMzhkMjY0IiwiaWF0IjoxNzI1MjQ1NDYwLCJleHAiOjE3MjU1MDQ5Njl9.8dS0rQepahabQuEXsQugC7oJjPpMA7xIGVNyuKaVOMM' \
            -H 'Referer: http://localhost:9000/component_measures?id=ticketing-v2&metric=new_maintainability_issues&view=list&selected=ticketing-v2%3Abackoffice%2Ftransfer%2Ftables.py' \
            -H 'X-XSRF-TOKEN: ko9afcfablgp9vmtc8bqi2sip1'
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


def show_duplications(project_key, file_path):
    """
        Reference: https://next.sonarqube.com/sonarqube/web_api/api/duplications/show
        
        Example:
        curl --location 'http://localhost:9000/api/duplications/show?key=ticketing-v2%3Abackoffice%2Ftransfer%2Ftables.py' \
            --header 'Authorization: Bearer squ_0ab1b83ad4d850d2bdbea4d77daa3b4360033266' | jq
            
        or don't need to encoder url
        
        curl --location 'http://localhost:9000/api/duplications/show?key=ticketing-v2:backoffice/transfer/tables.py' \
            --header 'Authorization: Bearer squ_0ab1b83ad4d850d2bdbea4d77daa3b4360033266' | jq
    """
    _file_path = file_path.replace("/", "%2F")
    key = f"{project_key}%3A{_file_path}"
    resp = requests.get(
        url=f"http://localhost:9000/api/duplications/show?key={key}",
        headers={
            "Authorization": "Bearer squ_0ab1b83ad4d850d2bdbea4d77daa3b4360033266",
        },
        timeout=60,
    )
    return resp.json()


def get_sources_lines(project_key, file_path):
    """
        Reference: https://next.sonarqube.com/sonarqube/web_api/api/duplications/show
        
        Example:
        curl --location 'http://localhost:9000/api/sources/lines?key=ticketing-v2%3Abackoffice%2Ftransfer%2Ftables.py&from=1' \
            --header 'Authorization: Bearer squ_0ab1b83ad4d850d2bdbea4d77daa3b4360033266' | jq
            
        or don't need to encoder url
        
        curl --location 'http://localhost:9000/api/sources/lines?key=ticketing-v2:backoffice/transfer/tables.py&from=1' \
            --header 'Authorization: Bearer squ_0ab1b83ad4d850d2bdbea4d77daa3b4360033266' | jq
    """
    _file_path = file_path.replace("/", "%2F")
    key = f"{project_key}%3A{_file_path}"
    resp = requests.get(
        url=f"http://localhost:9000/api/sources/lines?key={key}&from=1",
        headers={
            "Authorization": "Bearer squ_0ab1b83ad4d850d2bdbea4d77daa3b4360033266",
        },
        timeout=60,
    )
    return resp.json()


def get_duplicated_blocks_1(project_key, file_path):
    """get duplicated blocks inside a file, each block container sequence duplicated lines

    Args:
        project_key (_type_): _description_
        file_path (_type_): _description_
    """
    duplicated_blocks = []
    result = get_sources_lines(project_key, file_path)

    duplicated_block = []
    for value in result['sources']:
        if value['duplicated']:
            duplicated_block.append(value["line"])
        elif duplicated_block:
            duplicated_blocks.append(duplicated_block)
            duplicated_block = []
        # if current line is not duplicated and duplicated_block is empty,
        # so don't do anything

    return duplicated_blocks


def get_duplicated_blocks(project_key, file_path) -> list:
    def _get_file_path_and_block(duplication_block, files):
        file_path = files[duplication_block["_ref"]]["name"]
        duplicated_range = [
            duplication_block["from"],
            duplication_block["from"] + duplication_block["size"] - 1,
        ]
        return file_path, duplicated_range

    result = show_duplications(project_key, file_path)
    duplications = result["duplications"]
    files = result['files']
    duplicated_data = []
    for blocks in duplications:
        current_file_block = blocks["blocks"][0]
        duplicated_files_blocks = blocks['blocks'][1:]

        current_file_path, current_duplicated_range = _get_file_path_and_block(current_file_block, files)
        message = ''
        for block in duplicated_files_blocks:
            file_path, duplicated_range = _get_file_path_and_block(block, files)
            message += f"Lines {current_duplicated_range}: Duplicated by: {file_path} in lines: {duplicated_range}"

        duplicated_data.append(
            {
                "file_path": current_file_path,
                "duplicated_range": current_duplicated_range,
                "message": message,
            }
        )
    return duplicated_data


if __name__ == '__main__':
    # result = search_issues_by_severity()
    # print(json.dumps(data, indent=4, sort_keys=True))
    # result = extract_issue_data(result)
    # result = show_duplications(
    #     project_key="ticketing-v2",
    #     file_path="backoffice/transfer/tables.py"
    # )
    # result = get_sources_lines(
    #     project_key="ticketing-v2", file_path="backoffice/transfer/tables.py"
    # )
    result = get_duplicated_blocks(
        project_key="ticketing-v2", file_path="backoffice/transfer/tables.py"
    )
    print(json.dumps(result, indent=4, sort_keys=True))
