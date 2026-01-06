from uuid import UUID, uuid4


class User:
    def __init__(self, name: str, email: str):
        if not name:
            raise ValueError("User name cannot be empty")
        if "@" not in email:
            raise ValueError("Invalid email address")

        self._id: UUID = uuid4()
        self._name = name
        self._email = email

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def email(self) -> str:
        return self._email

    def __repr__(self) -> str:
        return f"User(id={self._id}, name={self._name})"
