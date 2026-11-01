import os, smtplib
from email.message import EmailMessage
from pathlib import Path

username = os.environ["MAIL_USERNAME"]
password = os.environ["MAIL_PASSWORD"]
recipient = os.environ["REPORT_EMAIL"]
report = Path("testreport.json").read_text(encoding="utf-8")

msg = EmailMessage()
msg["Subject"] = "CSC418 automated test report"
msg["From"] = username
msg["To"] = recipient
msg.set_content("The CI workflow completed. The actual pytest report is attached.\\n\\n" + report[:12000])
msg.add_attachment(report, filename="testreport.json", subtype="json")

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
    smtp.login(username, password)
    smtp.send_message(msg)
print("Email report sent.")
