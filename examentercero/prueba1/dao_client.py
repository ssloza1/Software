# dao_client.py
from datetime import datetime
from db import get_db

class ClientDAO:
    def __init__(self):
        self.col = get_db()["cliente"]

    def insert_client(self, name: str, phone: str, address: str, email: str):
        doc = {
            "name": name,
            "phone": phone,
            "address": address,
            "email": email,
            "createdAt": datetime.utcnow().isoformat()
        }
        self.col.insert_one(doc)
        return doc
