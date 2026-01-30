from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List

from email_address import EmailAddress
from status_enums import Status


@dataclass
class Email:
    subject: str
    body: str
    sender: EmailAddress
    recipients: List[EmailAddress]
    date: Optional[datetime]
    short_body: Optional[str]
    status: Status

    def __post_init__(self):
        if isinstance(self.recipients, EmailAddress):
            self.recipients = [self.recipients]
        for r in self.recipients:
            if not isinstance(r, EmailAddress):
                raise ValueError('Email must be EmailAddress')

    def prepare(self):
        self.subject = self.subject.strip()
        self.body = self.body.strip()
        if self.subject and self.body and self.sender and self.recipients:
            self.status = Status.READY
        else:
            self.status = Status.INVALID
        return self.add_short_body()

    def add_short_body(self):
        if len(self.body) <= 50:
            self.short_body = self.body
        else:
            self.short_body = self.body[:47] + "..."

    def __repr__(self):
        recipients_masked = ', '.join([r.masked for r in self.recipients])
        return (
            f"Email: {self.sender.masked}, "
            f"to: {recipients_masked}, "
            f"subject: {self.subject!r}, "
            f"status: {self.status}"
        )
