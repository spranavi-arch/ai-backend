from sqlalchemy.orm import Session
from app.models.document import Document

def create_document(db: Session, data):
    doc = Document(
        title=data.title,
        content=data.content,
        user_id=data.user_id
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc


def get_documents_by_user(db: Session, user_id: int):
    return db.query(Document).filter(Document.user_id == user_id).all()
