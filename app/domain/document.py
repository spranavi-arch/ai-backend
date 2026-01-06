from uuid import UUID, uuid4
from datetime import datetime, timezone


class Document:
    def __init__(self, title: str, content: str, owner_id: UUID):
        if not title:
            raise ValueError("Document title cannot be empty")

        self._id: UUID = uuid4()
        self._title = title
        self._content = content
        self._owner_id = owner_id
        self._created_at = datetime.now(timezone.utc)

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def title(self) -> str:
        return self._title

    @property
    def content(self) -> str:
        return self._content

    @property
    def owner_id(self) -> UUID:
        return self._owner_id

    @property
    def created_at(self) -> datetime:
        return self._created_at

    def update_content(self, new_content: str) -> None:
        if not new_content:
            raise ValueError("Document content cannot be empty")
        self._content = new_content

    def __repr__(self) -> str:
        return f"Document(id={self._id}, title={self._title})"
