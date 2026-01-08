from fastapi import FastAPI
from database import collection, embed_and_store_policies 
from embeddings import embed_text
from routes.view_db import router as view_db_router
import os

async def lifespan(app: FastAPI):
    if not os.getenv("TESTING"):
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
def search_policy(query: str, top_k: int = 3):
    query_embedding = embed_text(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "distances"]
    )

    documents = results["documents"][0]
    distances = results["distances"][0]

    matches = []
    for doc, dist in zip(documents, distances):
        matches.append({
            "document": doc,
            "similarity": round(1 - dist, 4)
        })

    return {
        "query": query,
        "similarity_method": "cosine_similarity",
        "top_k": top_k,
        "results": matches
    }



    
