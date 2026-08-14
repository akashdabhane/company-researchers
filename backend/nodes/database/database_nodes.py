import os
from graph.state import CompanyState
from pymongo import MongoClient


def database_node(state: CompanyState):
    client = MongoClient(os.getenv("MONGODB_URI"))
    db = client["company_research_agent"]
    collection = db["company_data"]

    print(state)

    result = collection.insert_one(state)
    print("Inserted ID:", result.inserted_id)

    return state

