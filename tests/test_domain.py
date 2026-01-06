import pytest
from app.domain.user import User
from app.domain.document import Document
from app.domain.document_store import DocumentStore


def test_create_user():
    user = User(name="Alice", email="alice@example.com")
    assert user.name == "Alice"
    assert user.email == "alice@example.com"


def test_create_document():
    user = User(name="Bob", email="bob@example.com")
    doc = Document(
        title="Test Doc",
        content="Hello World",
        owner_id=user.id
    )
    assert doc.title == "Test Doc"
    assert doc.owner_id == user.id


def test_document_store_add_and_fetch():
    store = DocumentStore()
    user = User(name="Carol", email="carol@example.com")
    doc = Document("Doc 1", "Content", user.id)

    store.add_document(doc)
    fetched = store.get_document(doc.id)

    assert fetched.id == doc.id


def test_get_documents_by_user():
    store = DocumentStore()
    user1 = User("User1", "u1@test.com")
    user2 = User("User2", "u2@test.com")

    doc1 = Document("Doc1", "A", user1.id)
    doc2 = Document("Doc2", "B", user1.id)
    doc3 = Document("Doc3", "C", user2.id)

    store.add_document(doc1)
    store.add_document(doc2)
    store.add_document(doc3)

    user1_docs = store.get_documents_by_user(user1.id)

    assert len(user1_docs) == 2


def test_delete_document():
    store = DocumentStore()
    user = User("Dave", "dave@test.com")
    doc = Document("Doc", "Content", user.id)

    store.add_document(doc)
    store.delete_document(doc.id)

    assert store.count() == 0
