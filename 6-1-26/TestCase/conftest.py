import os
import pytest
from Crud_op.database import collection

@pytest.fixture(autouse=True)
def clean_database():
    # Runs before each test
    collection.delete_many({})
    yield
    # Runs after each test
    collection.delete_many({})
