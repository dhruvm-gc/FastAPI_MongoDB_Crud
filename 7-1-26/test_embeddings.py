import chromadb
import ollama

# ---------------- TEST SETUP ---------------- #

TEST_POLICIES = [
    "Facebook Community Standards define what content is allowed or prohibited.",
    "Facebook Data Privacy Policy explains how user data is collected and used.",
    "Facebook Advertising Policy restricts misleading or harmful advertisements.",
    "Facebook Content Moderation Policy governs removal of violating content.",
    "Facebook Intellectual Property Policy requires respect for copyrights.",
    "Facebook Account Integrity Policy prohibits fake accounts and impersonation."
]

client = chromadb.Client()
collection = client.get_or_create_collection(name="pytest_facebook_policies")

# ---------------- HELPER FUNCTION ---------------- #

def embed_text(text: str):
    response = ollama.embeddings(
        model="nomic-embed-text",
        prompt=text
    )
    return response["embedding"]

# ---------------- PYTEST TESTS ---------------- #

def test_embedding_generation():
    """
    Test that Ollama returns a valid embedding vector
    """
    embedding = embed_text("Test embedding")

    assert embedding is not None
    assert isinstance(embedding, list)
    assert len(embedding) > 0
    assert all(isinstance(x, float) for x in embedding)


def test_store_embeddings_in_chromadb():
    """
    Test that embeddings and documents are stored in ChromaDB
    """
    ids = []
    embeddings = []
    documents = []

    for index, policy in enumerate(TEST_POLICIES):
        embedding = embed_text(policy)

        ids.append(f"policy_{index}")
        embeddings.append(embedding)
        documents.append(policy)

    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=documents
    )

    stored_data = collection.get()

    assert stored_data is not None
    assert "documents" in stored_data
    assert len(stored_data["documents"]) == len(TEST_POLICIES)

    for policy in TEST_POLICIES:
        assert policy in stored_data["documents"]
