"""
    to get jenkins token, Click to your profile -> Configure -> API Token -> Add new token
"""

import requests


def get_jenkins_job_info(job_url, jenkins_user, jenkins_token) -> dict:
    """
        curl -u "[username|email]:[token]" \
            -s "{JOB_URL}/api/json" \
            | jq
        Sample job url: https://jenkins.showheroes.com/job/pipeline-multibranch-viralize-web/job/PR-5273/9
    """

    resp = requests.get(
        url=job_url + "/api/json",
        auth=(jenkins_user, jenkins_token),
    )
    if resp.status_code != 200:
        print(resp.json())
        return {}
    return resp.json()


def get_jenkins_job_test_report(job_url, jenkins_user, jenkins_token) -> dict:
    """
        curl -u "[username|email]:[token]" \
            -s "{JOB_URL}/testReport/api/json" \
            | jq
        Sample job url: https://jenkins.showheroes.com/job/pipeline-multibranch-viralize-web/job/PR-5273/9
    """

    resp = requests.get(
        url=job_url + "/testReport/api/json",
        auth=(jenkins_user, jenkins_token),
    )
    if resp.status_code != 200:
        print(resp.text)
        return {}
    return resp.json()


if __name__ == "__main__":
    import json
    jenkins_user, jenkins_token = (
        open("/home/xuananh/Dropbox/Work/showheroes/jenkins_account.txt", "r")
        .read()
        .splitlines()
    )
    job_url = "https://jenkins.showheroes.com/job/pipeline-multibranch-viralize-web/job/PR-5273/5"
    # print(get_jenkins_job_info(job_url, jenkins_user, jenkins_token))
    resp = get_jenkins_job_test_report(job_url, jenkins_user, jenkins_token)
    print(json.dumps(resp, indent=4))