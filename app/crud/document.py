from sqlalchemy.orm import Session
from app.models.document import Document
from app.schemas.document import DocumentCreate

def create_document(db: Session, doc: DocumentCreate):
    document = Document(
        title=doc.title,
        content=doc.content,
        owner_id=doc.owner_id
    )
    db.add(document)
    db.commit()
    db.refresh(document)
    return document

def get_documents_by_user(db: Session, user_id: str):
    return db.query(Document).filter(Document.owner_id == user_id).all()
