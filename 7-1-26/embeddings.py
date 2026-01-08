import ollama
import ast

def embed_text(text: str):
    response = ollama.embeddings(
        model="mxbai-embed-large",
        prompt=text
    )

    embedding = response.get("embedding")

    if embedding is None:
        raise RuntimeError("Embedding generation failed")

    if isinstance(embedding, str):
        embedding = ast.literal_eval(embedding)

    if not isinstance(embedding, list):
        raise RuntimeError("Invalid embedding format")

    return embedding
