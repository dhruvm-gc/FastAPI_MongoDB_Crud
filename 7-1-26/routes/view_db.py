from fastapi import APIRouter
from database import collection

router = APIRouter(prefix="/db", tags=["Vector Database"])

@router.get("/view")
def view_database():
    data = collection.get(include=["documents", "embeddings"])

    result = []
    for i in range(len(data["ids"])):
        embedding = data["embeddings"][i]
        safe_embedding = [float(x) for x in embedding[:10]]

        result.append({
            "id": data["ids"][i],
            "document": data["documents"][i],
            "embedding_preview": safe_embedding,
            "embedding_length": len(embedding)
        })

    return {
        "total_documents": len(result),
        "data": result
    }
