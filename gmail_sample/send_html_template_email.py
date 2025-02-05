import json
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from json_sample.json_with_comment import JSONWithCommentsDecoder


def send_html_email():
    gmail_user = os.environ.get("GMAIL_USER")
    gmail_app_password = os.environ.get("GMAIL_APP_PW")
    sent_from = gmail_user
    sent_to = ["phungxuananh1991+python_app@gmail.com"]

    # Load the HTML template from an external file.
    with open("email_template.html", "r") as template_file:
        html_template = template_file.read()

    # Arbitrary list of URLs.
    urls = ["http://www.python.org", "http://www.example.com", "http://www.github.com"]

    # Generate HTML list items for each URL.
    list_items = "\n".join([f'<li><a href="{url}">{url}</a></li>' for url in urls])

    # Define the recipient's name and format it in bold with red color using inline CSS.
    recipient_name = "John"
    formatted_name = f'<strong style="color:red;">{recipient_name}</strong>'

    # Replace placeholders in the HTML template with the generated content.
    html_content = html_template.replace("{{url_list}}", list_items)
    html_content = html_content.replace("{{name}}", formatted_name)

    # Create a plain text version for email clients that don't support HTML.
    plain_text = f"Hi {recipient_name},\nHere are your links:\n" + "\n".join(urls)

    # Create the MIME message container with multipart/alternative.
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Your Links"
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


if __name__ == "__main__":
    send_html_email()
