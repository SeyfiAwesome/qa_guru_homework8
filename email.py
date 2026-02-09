from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from email_address import EmailAddress
from status_enum import Status


@dataclass
class Email:
    subject: str
    body: str
    sender: EmailAddress
    recipients: List[EmailAddress]

    date: Optional[datetime] = None
    short_body: Optional[str] = None
    status: Status = Status.DRAFT

    def __post_init__(self):
        if isinstance(self.recipients, EmailAddress):
            self.recipients = [self.recipients]

        if not self.recipients:
            raise ValueError("Recipients cannot be empty")

        for r in self.recipients:
            if not isinstance(r, EmailAddress):
                raise ValueError("Recipients must be EmailAddress objects")

    def prepare(self):
        self.subject = self.subject.strip()
        self.body = self.body.strip()

        self._add_short_body()

        if self.subject and self.body and self.sender and self.recipients:
            self.status = Status.READY
        else:
            self.status = Status.INVALID

    def _add_short_body(self):
        if len(self.body) <= 50:
            self.short_body = self.body
        else:
            self.short_body = self.body[:47] + "..."

    def __repr__(self):
        recipients = ", ".join(r.masked for r in self.recipients)
        return (
            f"Email(from={self.sender.masked}, "
            f"to=[{recipients}], "
            f"subject={self.subject!r}, "
            f"status={self.status})"
        )
