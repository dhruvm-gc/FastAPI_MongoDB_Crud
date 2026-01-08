
from unittest.mock import patch

from fastapi.testclient import TestClient
from main import app
from embeddings import embed_text
from database import embed_and_store_policies

client = TestClient(app)
def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "running"}


@patch("main.embed_text")
@patch("main.collection")
def test_search_endpoint(mock_collection, mock_embed):
    mock_embed.return_value = [0.1, 0.2, 0.3]

    mock_collection.query.return_value = {
        "documents": [["Policy A", "Policy B", "Policy C"]],
        "distances": [[0.1, 0.2, 0.3]]
    }

    response = client.get("/search?query=test")

    assert response.status_code == 200
    data = response.json()

    assert data["query"] == "test"
    assert data["similarity_method"] == "cosine_similarity"

    assert len(data["results"]) == 3

    first = data["results"][0]
    assert "document" in first
    assert "similarity" in first
    assert first["similarity"] == 0.9


@patch("embeddings.ollama.embeddings")
def test_embed_text_success(mock_ollama):
    mock_ollama.return_value = {"embedding": [0.1, 0.2, 0.3]}

    embedding = embed_text("hello")

    assert isinstance(embedding, list)
    assert len(embedding) == 3


@patch("embeddings.ollama.embeddings")
def test_embed_text_failure(mock_ollama):
    mock_ollama.return_value = {}

    try:
        embed_text("fail")
        assert False
    except RuntimeError as e:
        assert "Embedding generation failed" in str(e)


@patch("database.collection")
@patch("database.embed_text")
def test_embed_and_store_policies(mock_embed, mock_collection):
    mock_collection.count.return_value = 0
    mock_embed.return_value = [0.1, 0.2, 0.3]

    embed_and_store_policies()

    assert mock_collection.add.called

@patch("routes.view_db.collection")
def test_view_db_endpoint(mock_collection):
    mock_collection.get.return_value = {
        "ids": ["id1"],
        "documents": ["Test policy"],
        "embeddings": [[0.1] * 50]
    }

    response = client.get("/db/view")

    assert response.status_code == 200
    data = response.json()

    assert data["total_documents"] == 1
    assert data["data"][0]["embedding_length"] == 50
