import os
import pytest
from Crud_op.database import collection

@pytest.fixture(autouse=True)
def clean_database():
    
    collection.delete_many({})
    yield
    
    collection.delete_many({})
