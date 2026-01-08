from fastapi import FastAPI
from database import collection, FACEBOOK_POLICIES
from embeddings import embed_text
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
    title="Ollama with VectorDB",
    lifespan=lifespan
)

app.include_router(view_db_router)

@app.get("/")
def root():
    return {"status": "running"}

@app.get("/search")
def search_policy(query: str):
    query_embedding = embed_text(query)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=1)
    return {"query": query, "matches": results["documents"]}
    
