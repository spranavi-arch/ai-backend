from sqlalchemy.orm import Session
from app.models.document import Document
from app.models.user import User

def create_document(db: Session, data):
    users = db.query(User).filter(User.id.in_(data.user_ids)).all()

    doc = Document(
        title=data.title,
        content=data.content,
        users=users
    )

    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc


def get_documents_by_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None
    return user.documents
