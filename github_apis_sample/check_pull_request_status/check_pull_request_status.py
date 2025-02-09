"""
    to run this script in the server
    1. clone project
    2. create a virtual environment
    3. install requirements: make install-all-requirements
    4. create a env_file with this content: (refer their values in the env.sh file in this repo)
        export SH_JENKINS_EMAIL="fake.email@email.com"
        export SH_JENKINS_TOKEN="fakejenkinstoken1234567890"
        export GMAIL_USER="fakeemail@gmail.com"
        export GMAIL_APP_PW="fakeapppassword123456"
        export GH_TOKEN_PXA="ghp_fakeGitHubToken1234567890"
        export PYTHONPATH="/home/ubuntu/.tmp/python-note"

    5. create a script file named: 
        vim check_pull_request_status.sh 
        with this content:
            #!/bin/bash
            source /home/ubuntu/.tmp/python-note/env_file
            cd /home/ubuntu/.tmp/python-note/
            .venv/bin/python github_apis_sample/check_pull_request_status.py
    6. make the script executable: chmod +x check_pull_request_status.sh
    7. Create a JSON file named repositories.json with the list of repositories:
        See the the below sample or copy from this file: 
        ln -sf Work/Other/backuped-files/list_repositories_to_check_status.json \
            github_apis_sample/check_pull_request_status/list_repositories_to_check_status.json
        [
            {
                "owner": "another_owner",
                "repo": "another_repo",
                "user": "AnotherUser"
            }
            // Add more repositories as needed
        ]
    8. create a cron job to run this script every 10 minutes:
        crontab -e
        */10 * * * * /home/ubuntu/.tmp/python-note/check_pull_request_status.sh > /tmp/check_pull_request_status.log 2>&1
"""

import json
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from github_apis_sample.common import (
    get_commit_status,
    get_latest_commit,
    list_pull_requests,
)
from jenkins_utils.jenkins_utils import get_jenkins_job_test_report
from logging_sample.logging_dictConfig import console_logger


def send_html_email(subject, test_reports: list):
    """
    sample test_reports = [
        {
            "className": "viralize_web.api_adsources.tests.test_serializers.AdSourceSerializerSaveBOTC",
            "errorStackTrace": 'Traceback (most recent call last):\n  File "/app/viralize_web/api_adsources/tests/test_serializers.py", line 108, in test_prebid_warnings_schain\n    self.assertTrue(ser.is_valid())\n  File "/usr/local/lib/python3.9/site-packages/rest_framework/serializers.py", line 227, in is_valid\n    self._validated_data = self.run_validation(self.initial_data)\n  File "/usr/local/lib/python3.9/site-packages/rest_framework/serializers.py", line 430, in run_validation\n    assert value is not None, \'.validate() should return the validated data\'\nAssertionError: .validate() should return the validated data\n',
        },
        {
            "className": "viralize_web.api_sites.tests.test_website_api.SitesCheckNotActive",
            "errorStackTrace": 'Traceback (most recent call last):\n  File "/app/viralize_web/api_sites/tests/test_website_api.py", line 143, in test_check_suspend_sites_with_valid_input\n    self.assertEqual(response.json(), [2, 3, 4])\nAssertionError: Lists differ: [1, 2, 3, 4] != [2, 3, 4]\n\nFirst differing element 0:\n1\n2\n\nFirst list contains 1 additional elements.\nFirst extra element 3:\n4\n\n- [1, 2, 3, 4]\n?  ---\n\n+ [2, 3, 4]\n',
        },
        {
            "className": "VideoAdSource/VideoAdSourceClone renders the adsource info from api and suggested name",
            "errorStackTrace": "FetchError: invalid json response body at  reason: Unexpected end of JSON input\n    at /app/components/node_modules/node-fetch/lib/index.js:272:32\n    at processTicksAndRejections (node:internal/process/task_queues:95:5)",
        },
    ]
    """
    gmail_user = os.environ.get("GMAIL_USER")
    gmail_app_password = os.environ.get("GMAIL_APP_PW")
    sent_from = gmail_user
    sent_to = ["phungxuananh1991+python_app@gmail.com"]

    # Load the HTML template from an external file.
    with open(
        "github_apis_sample/check_pull_request_status/email_template.html", "r"
    ) as template_file:
        html_template = template_file.read()

    # Define the recipient's name and format it in bold with red color.
    recipient_name = "guys"
    formatted_name = f'<strong style="color:red;">{recipient_name}</strong>'

    # Generate table rows for each test report
    report_rows = ""
    for report in test_reports:
        row = f"""
        <tr>
            <td>{report['className']}</td>
            <td><pre>{report['errorStackTrace']}</pre></td>
        </tr>
        """
        report_rows += row

    # Replace placeholders in the HTML template with generated content.
    html_content = html_template.replace("{{name}}", formatted_name)
    html_content = html_content.replace("{{report_rows}}", report_rows)

    # Create a plain text version for clients that don't support HTML.
    plain_text = f"Hi {recipient_name},\n\n"
    plain_text += subject + ":\n"
    for report in test_reports:
        plain_text += (
            f"Class Name: {report['className']}\nError: {report['errorStackTrace']}\n\n"
        )

    # Create the MIME message container with multipart/alternative.
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = sent_from
    msg["To"] = ", ".join(sent_to)

    # Attach both plain text and HTML parts.
    # Including part1, the plain text alternative, is not strictly required
    # if all your recipients support HTML emails. However, it is a good practice
    # to include a plain text version to ensure maximum compatibility with email
    # clients that may not render HTML properly.
    part1 = MIMEText(plain_text, "plain")
    part2 = MIMEText(html_content, "html")
    msg.attach(part1)
    msg.attach(part2)

    # Connect securely to Gmail's SMTP server and send the email.
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.ehlo()
    server.login(gmail_user, gmail_app_password)
    server.sendmail(sent_from, sent_to, msg.as_string())
    server.close()
    console_logger.debug("Email sent with subject: %s", subject)


def check_to_send_email(
    owner, repo, pr, lastest_commit_id, commit_status_updated_at, failed_tests_report
):
    """
    Get all failed pull requests from a json file
        path: /tmp/github-failed-pull-requests.json
        sample content:
            {
                "showheroes/viralize-web/pull/5262": {
                    "last_commit_id": "status updated at",
                },
            }
    if the pull request is not in the file, add it to the file and send an email to report failed tests
    if the pull request is in the file, check if the last_commit_id is different from the one in the file
        if different, update the last_commit_id and commit_status_updated_at in the file and send an email to report failed tests
        if the same, check if the commit_status_updated_at is different from the one in the file,
            if different, send an email to report failed tests and update the commit_status_updated_at in the file
    """
    pr_url = f"{owner}/{repo}/pull/{pr['number']}"
    subject = f"Branch failed unknown reason: {pr['source_branch']}"
    if failed_tests_report:
        subject = f"Branch failed tests: {pr['source_branch']}"
    with open("/tmp/github-failed-pull-requests.json", "r+") as f:
        failed_pull_requests = json.loads(f.read())
        failed_pr = failed_pull_requests.get(pr_url, {})
        if (
            not failed_pr
            or failed_pr.get("last_commit_id") != lastest_commit_id
            or failed_pr.get("commit_status_updated_at") != commit_status_updated_at
        ):
            failed_pull_requests[pr_url] = {
                "last_commit_id": lastest_commit_id,
                "commit_status_updated_at": commit_status_updated_at,
            }
            f.seek(0)
            f.write(json.dumps(failed_pull_requests, indent=4, sort_keys=True))
            f.truncate()
            send_html_email(subject, failed_tests_report)


def handle_fixed_pull_request(owner, repo, pr):
    """
    Get all failed pull requests from a json file: /tmp/github-failed-pull-requests.json
        if the pull request is not in the file, return
        if the pull request is in the file, remove it from the file and then send an email to report the PR is fixed
    """
    with open("/tmp/github-failed-pull-requests.json", "r+") as f:
        failed_pull_requests = json.loads(f.read())
        pr_url = f"{owner}/{repo}/pull/{pr['number']}"
        if pr_url in failed_pull_requests:
            del failed_pull_requests[pr_url]
            f.seek(0)
            f.write(json.dumps(failed_pull_requests, indent=4, sort_keys=True))
            f.truncate()
            subject = f"Branch fixed: {pr['source_branch']}"
            send_html_email(subject, [])


def handle_failed_pull_request(
    owner, repo, pr, status, jenkins_user, jenkins_token, commit_sha
):
    jenkins_failed_job_url = ""
    for status in status["statuses"]:
        if status["state"] == "error":
            jenkins_failed_job_url = status["target_url"].removesuffix(
                "display/redirect"
            )
            break

    failed_tests_report = []
    if jenkins_failed_job_url:
        test_report = get_jenkins_job_test_report(
            jenkins_failed_job_url, jenkins_user, jenkins_token
        )
        if test_report:
            # NOTE: refer to sample test report response in jenkins_utils/sample_response/test-report.json
            for report in test_report["suites"]:
                for case in report["cases"]:
                    if case["status"] == "FAILED":
                        failed_tests_report.append(
                            {
                                "className": case["className"],
                                "errorStackTrace": case["errorStackTrace"],
                            }
                        )

    if status.get("updated_at"):
        last_commit_updated_at = status["updated_at"]
    else:
        last_commit_updated_at = status["statuses"][0]["updated_at"]
    check_to_send_email(
        owner,
        repo,
        pr,
        commit_sha,
        last_commit_updated_at,
        failed_tests_report,
    )


def check_pull_request_status(owner, repo, pr, gh_token):
    latest_commit = get_latest_commit(owner, repo, pr["number"], gh_token)
    if not latest_commit:
        return None
    commit_sha = latest_commit["sha"]
    status = get_commit_status(owner, repo, commit_sha, gh_token)
    state = status.get("state", "")

    if state == "pending":
        return
    if state == "success":
        handle_fixed_pull_request(owner, repo, pr)
        return
    if state == "failure":
        handle_failed_pull_request(
            owner, repo, pr, status, JENKINS_USER, JENKINS_TOKEN, commit_sha
        )


def get_pull_requests_of_user(owner, repo, gh_token, user):
    pull_requests = []
    for pr in list_pull_requests(owner, repo, gh_token):
        if pr["user"]["login"] == user:
            pull_requests.append(
                {
                    "number": pr["number"],
                    "source_branch": pr["head"]["ref"],
                }
            )
    return pull_requests


def remove_unused_pull_request(owner, repo, pull_requests):
    currrent_pull_requests = [
        f"{owner}/{repo}/pull/{pr['number']}" for pr in pull_requests
    ]
    with open("/tmp/github-failed-pull-requests.json", "r+") as f:
        failed_pull_requests = {}
        data = f.read()
        failed_pull_requests = json.loads(data) if data else {}
        for pr_url in list(failed_pull_requests.keys()):
            if pr_url not in currrent_pull_requests:
                del failed_pull_requests[pr_url]
        f.seek(0)
        f.write(json.dumps(failed_pull_requests, indent=4, sort_keys=True))
        f.truncate()


def main():
    file_name = "/tmp/github-failed-pull-requests.json"

    if not os.path.exists(file_name):
        # Create the file and write some initial content
        with open(file_name, "w") as file:
            file.write("{}")

    # Load the list of repositories from the JSON file
    with open(
        "github_apis_sample/check_pull_request_status/list_repositories_to_check_status.json",
        "r",
    ) as file:
        repositories = json.load(file)

    for repo_info in repositories:
        owner = repo_info["owner"]
        repo = repo_info["repo"]
        user = repo_info["user"]

        pull_requests = get_pull_requests_of_user(owner, repo, GH_TOKEN, user)
        for pr in pull_requests:
            console_logger.debug("Checking PR: %s", pr["number"])
            check_pull_request_status(owner, repo, pr, GH_TOKEN)

        remove_unused_pull_request(owner, repo, pull_requests)


if __name__ == "__main__":
    GH_TOKEN = os.environ.get("GH_TOKEN_PXA")
    JENKINS_USER = os.environ.get("SH_JENKINS_EMAIL")
    JENKINS_TOKEN = os.environ.get("SH_JENKINS_TOKEN")

    main()
