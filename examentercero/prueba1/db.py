# db.py
import os
from pymongo import MongoClient

# TODO: pega aquí tu URI (Atlas/Compass)
MONGO_URI = "mongodb+srv://Steven:Steven2001@cluster0.mp8muds.mongodb.net/?appName=Cluster0"
DB_NAME = os.getenv("DB_NAME", "BillDB")  # cámbialo si tu base se llama diferente

_client = None

def get_db():
    global _client
    if _client is None:
        _client = MongoClient(MONGO_URI)
    return _client[DB_NAME]
