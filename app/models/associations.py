from sqlalchemy import Table, Column, Integer, ForeignKey
from app.core.database import Base

document_users = Table(
    "document_users",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("document_id", Integer, ForeignKey("documents.id"), primary_key=True),
)
