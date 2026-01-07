import chromadb

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