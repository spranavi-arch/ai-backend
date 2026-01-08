from sqlalchemy.orm import Session
from app.models.document import Document

def create_document(db, document):
    original_filename = (
        document.original_filename
        if getattr(document, "original_filename", None)
        else f"{document.title}.txt"
    )

    db_document = Document(
        title=document.title,
        content=document.content,
        original_filename=original_filename,
        user_id=document.user_id,
    )

    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document


def get_documents_by_user(db: Session, user_id: int):
    return db.query(Document).filter(Document.user_id == user_id).all()