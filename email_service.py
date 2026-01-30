from datetime import datetime
import copy

from email import Email
from status_enums import Status


class EmailService:

    def send_email(self, email: Email):
        sent_emails = []

        for recipient in email.recipients:
            email_copy = copy.deepcopy(email)
            email_copy.recipients = [recipient]
            email_copy.date = datetime.now()

            if email.status == Status.READY:
                email_copy.status = Status.SENT
            else:
                email_copy.status = Status.FAILED

            sent_emails.append(email_copy)
        return sent_emails

class LoggingEmailService(EmailService):

    def send_email(self, email: Email):
        sent_emails = super().send_email(email)

        with open("send.log", "a", encoding="utf-8") as f:
            for sent in sent_emails:
                f.write(
                    f"{datetime.now()} | "
                    f"From: {sent.sender.masked} | "
                    f"To: {', '.join(r.masked for r in sent.recipients)} | "
                    f"Subject: {sent.subject} | "
                    f"Status: {sent.status}\n"
                )

        return sent_emails