import copy
from datetime import datetime
from typing import List

from src.email import Email
from src.status import Status


class EmailService:
    def __init__(self, email: Email):
        self.email = email

    def add_send_date(self) -> str:
        return datetime.now().strftime("%Y-%m-%d")

    def send_email(self) -> List[Email]:
        sent_emails = []

        for recipient in self.email.recipients:
            email_copy = copy.deepcopy(self.email)
            email_copy.recipients = [recipient]
            email_copy.date = datetime.now()

            if self.email.status == Status.READY:
                email_copy.status = Status.SENT
            else:
                email_copy.status = Status.FAILED

            sent_emails.append(email_copy)

        return sent_emails


class LoggingEmailService(EmailService):
    def send_email(self) -> List[Email]:
        sent_emails = super().send_email()

        with open("send.log", "a", encoding="utf-8") as f:
            for sent in sent_emails:
                f.write(
                    f"{sent.date} | "
                    f"From: {sent.sender.masked} | "
                    f"To: {', '.join(r.masked for r in sent.recipients)} | "
                    f"Subject: {sent.subject} | "
                    f"Status: {sent.status}\n"
                )

        return sent_emails