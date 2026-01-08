import chromadb
from numpy import append
from embeddings import embed_text
import pandas as pd

client = chromadb.Client()
collection = client.get_or_create_collection(name="facebook_policies")

FACEBOOK_POLICIES = [
    "Facebook Community Standards define what content is allowed or prohibited, including rules on violence, hate speech, and misinformation.",
    "Facebook Data Privacy Policy explains how user data is collected, stored, and used for personalization, security, and advertising purposes.",
    "Facebook Advertising Policy restricts misleading, deceptive, or harmful advertisements and enforces transparency for advertisers.",
    "Facebook Content Moderation Policy governs the removal of content that violates platform rules such as hate speech, nudity, or violent material.",
    "Facebook Intellectual Property Policy requires users to respect copyrights and trademarks and allows removal of infringing content.",
    "Facebook Account Integrity Policy prohibits fake accounts, impersonation, and coordinated inauthentic behavior."
]

def embed_and_store_policies():
    if collection.count() > 0:
        return

    rows = []
    ids = []
    embeddings = []
    documents = []

    for i, policy in enumerate(FACEBOOK_POLICIES):
        vec = embed_text(policy)
        policy_id = f"fb_policy_{i}"

        ids.append(policy_id)
        embeddings.append(vec)
        documents.append(policy)

        rows.append({
        "ids": policy_id,
        "embeddings": policy,
        "embedding_length": len(vec),
        "embedding_preview": ",".join(str(float(x)) for x in vec[:10])
        })


    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=documents
    )

    df = pd.DataFrame(rows)
    df.to_csv("facebook_policies_embeddings.csv", index=False)