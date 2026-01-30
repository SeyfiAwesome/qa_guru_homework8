class EmailAddress:
    def __init__(self, raw_email: str):
        normalized = raw_email.strip().lower()
        if "@" not in normalized:
            raise ValueError('Email is invalid')
        if not normalized.endswith(('.com', '.ru', '.net')):
            raise ValueError('Email is invalid')
        self._value = normalized

    @property
    def value(self):
        return self._value

    @property
    def masked(self):
        login = self._value.split("@")[0]
        domain = self._value.split("@")[1]
        return login[:2] + "***@" + domain
