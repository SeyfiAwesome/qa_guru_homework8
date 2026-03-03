from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Union

from src.email_address import EmailAddress
from src.status import Status
from src.utils import clean_text


@dataclass
class Email:
    subject: str
    body: str
    sender: EmailAddress
    recipients: Union[EmailAddress, List[EmailAddress]]
    date: Optional[datetime] = None
    short_body: Optional[str] = None
    status: Status = Status.DRAFT

    def __post_init__(self):
        if isinstance(self.recipients, EmailAddress):
            self.recipients = [self.recipients]

    def get_recipients_str(self) -> str:
        return ", ".join(str(r) for r in self.recipients)

    def clean_data(self):
        self.subject = clean_text(self.subject)
        self.body = clean_text(self.body)
        return self

    def add_short_body(self, n: int = 10):
        if not self.body:
            self.short_body = None
        elif len(self.body) <= n:
            self.short_body = self.body
        else:
            self.short_body = self.body[:n] + "..."

    def is_valid_fields(self) -> bool:
        return bool(self.subject and self.body)

    def prepare(self):
        # Очищаем текст
        self.clean_data()

        # Добавляем короткую версию body
        self.add_short_body()

        # Проверяем все поля
        if (self.subject and self.body and self.sender and self.recipients):
            self.status = Status.READY
        else:
            self.status = Status.INVALID

    def __str__(self) -> str:
        recipients_str = self.get_recipients_str()
        body_display = self.short_body if self.short_body else self.body

        return (
            f"Status: {self.status}\n"
            f"Кому: {recipients_str}\n"
            f"От: {self.sender.masked}\n"
            f"Тема: {self.subject}, дата {self.date}\n"
            f"{body_display}"
        )
