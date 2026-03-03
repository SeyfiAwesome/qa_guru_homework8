class EmailAddress:
    def __init__(self, raw_email: str):
        self._address = self._normalize_address(raw_email)

        if not self._check_correct_email():
            raise ValueError("Invalid email address")

    def _normalize_address(self, raw_email: str) -> str:
        return raw_email.strip().lower()

    def _check_correct_email(self) -> bool:
        if "@" not in self._address:
            return False

        valid_endings = (".com", ".ru", ".net")
        return self._address.endswith(valid_endings)

    @property
    def address(self) -> str:
        return self._address

    @property
    def masked(self) -> str:
        login, domain = self._address.split("@")
        return f"{login[:2]}***@{domain}"

    def __str__(self) -> str:
        return self._address
