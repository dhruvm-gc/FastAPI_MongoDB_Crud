from fastapi import FastAPI
from database import collection
from embeddings import embed_text
from data import FACEBOOK_POLICIES
from routes.view_db import router as view_db_router

def embed_and_store_policies():
    if collection.count() > 0:
        return

    ids = []
    embeddings = []
    documents = []

    for i, policy in enumerate(FACEBOOK_POLICIES):
        vec = embed_text(policy)
        ids.append(f"fb_policy_{i}")
        embeddings.append(vec)
        documents.append(policy)

    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=documents
    )

async def lifespan(app: FastAPI):
    embed_and_store_policies()
    yield

app = FastAPI(
    title="Ollama + ChromaDB Policy Vector API",
    lifespan=lifespan
)

app.include_router(view_db_router)

@app.get("/")
def root():
    return {"status": "running"}
