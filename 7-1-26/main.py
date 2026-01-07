from fastapi import FastAPI
import chromadb
import ollama

async def lifespan(app: FastAPI):
    embed_and_store_policies()
    yield

app = FastAPI(title="Ollama + ChromaDB Policy Vector API",
              lifespan=lifespan)


client = chromadb.Client()
collection = client.create_collection(name="facebook_policies")


def embed_text(text: str):
    response = ollama.embeddings(
        model="nomic-embed-text",
        prompt=text
    )
    return response["embedding"]


FACEBOOK_POLICIES = [
    "Facebook Community Standards define what content is allowed or prohibited, including rules on violence, hate speech, and misinformation.",
    "Facebook Data Privacy Policy explains how user data is collected, stored, and used for personalization, security, and advertising purposes.",
    "Facebook Advertising Policy restricts misleading, deceptive, or harmful advertisements and enforces transparency for advertisers.",
    "Facebook Content Moderation Policy governs the removal of content that violates platform rules such as hate speech, nudity, or violent material.",
    "Facebook Intellectual Property Policy requires users to respect copyrights and trademarks and allows removal of infringing content.",
    "Facebook Account Integrity Policy prohibits fake accounts, impersonation, and coordinated inauthentic behavior."
]

def embed_and_store_policies():
    ids = []
    embeddings = []
    documents = []

    for i, policy in enumerate(FACEBOOK_POLICIES):
        embedding = embed_text(policy)

        ids.append(f"fb_policy_{i}")
        embeddings.append(embedding)
        documents.append(policy)

    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=documents
    )

@app.get("/")
def root():
    return {"message": "Facebook Policy Vector DB is running"}

@app.get("/search")
def search_policy(query: str):
    query_embedding = embed_text(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=1
    )

    return {
        "query": query,
        "matches": results["documents"]
    }
