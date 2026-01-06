from typing import Dict, List
from uuid import UUID

from app.domain.document import Document


class DocumentStore:
    """
    In-memory document store.
    Acts as a repository layer.
    """

    def __init__(self):
        self._documents: Dict[UUID, Document] = {}

    def add_document(self, document: Document) -> None:
        if document.id in self._documents:
            raise ValueError("Document already exists")
        self._documents[document.id] = document

    def get_document(self, document_id: UUID) -> Document:
        document = self._documents.get(document_id)
        if not document:
            raise KeyError("Document not found")
        return document

    def get_documents_by_user(self, user_id: UUID) -> List[Document]:
        return [
            doc for doc in self._documents.values()
            if doc.owner_id == user_id
        ]

    def delete_document(self, document_id: UUID) -> None:
        if document_id not in self._documents:
            raise KeyError("Document not found")
        del self._documents[document_id]

    def count(self) -> int:
        return len(self._documents)
