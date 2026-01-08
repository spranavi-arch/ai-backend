from fastapi import FastAPI
from app.api.routes import users, documents, upload, search,index
from app.core.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Backend API")

app.include_router(users.router)
app.include_router(documents.router)
app.include_router(upload.router)

app.include_router(documents.router, tags=["Documents"])
#app.include_router(search.router, tags=["Search"])
app.include_router(index.router) 
app.include_router(search.router)