class EmailAddress:
    def __init__(self, raw_email: str):
        normalized = raw_email.strip().lower()

        if "@" not in normalized:
            raise ValueError("Email must contain @")

        if not normalized.endswith((".com", ".ru", ".net")):
            raise ValueError("Email must end with .com, .ru or .net")

        self._value = normalized

    @property
    def value(self) -> str:
        return self._value

    @property
    def masked(self) -> str:
        login, domain = self._value.split("@")
        return f"{login[:2]}***@{domain}"

    def __str__(self) -> str:
        return self._value
