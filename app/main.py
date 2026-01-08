from fastapi import FastAPI
from app.api.routes import users, documents, upload
from app.core.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Backend Internship API")

app.include_router(users.router)
app.include_router(documents.router)
app.include_router(upload.router)
