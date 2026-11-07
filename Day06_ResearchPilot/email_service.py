import os
import smtplib
import ssl

from email.message import EmailMessage
from dotenv import load_dotenv

from email_template import create_email_template

load_dotenv()

def send_report_email(report, recipient=None):
    """Send a research report through Gmail SMTP."""

    sender = os.getenv("GMAIL_ADDRESS")
    app_password = os.getenv("GMAIL_APP_PASSWORD")

    if not sender or not app_password:
        raise ValueError(
            "Gmail credentials are missing in the .env file."
        )

    if not recipient:
        raise ValueError("Recipient email address is required.")

    # Create email message
    message = EmailMessage()

    message["Subject"] = (
        f"ResearchPilot Report - {report.research_question}"
    )

    message["From"] = sender
    message["To"] = recipient

    # Plain-text fallback
    plain_text = f"""
ResearchPilot Research Report

Research Question:
{report.research_question}

Summary:
{report.summary}

Key Findings:
"""

    for finding in report.key_findings:
        plain_text += f"\n- {finding}"

    plain_text += "\n\nSources:\n"

    for source in report.sources:
        plain_text += (
            f"\n- {source.title}\n"
            f"  {source.url}\n"
            f"  {source.snippet}\n"
        )

    message.set_content(plain_text)

    # HTML version
    html_content = create_email_template(report)

    message.add_alternative(
        html_content,
        subtype="html"
    )

    # Connect to Gmail SMTP
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(
        "smtp.gmail.com",
        465,
        context=context
    ) as server:

        server.login(sender, app_password)

        server.send_message(message)

    return True
