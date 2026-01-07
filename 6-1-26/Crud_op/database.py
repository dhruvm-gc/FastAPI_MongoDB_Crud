from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
DB_NAME = os.getenv("MONGO_TEST_DB", "fastapi_db")


client = MongoClient(MONGO_URL)
db = client["fastapi_db"]
collection = db["users"]